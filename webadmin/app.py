"""
Flask web admin panel for managing applications and users
"""
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import wraps
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import (
    Flask, abort, flash, redirect, render_template,
    request, session, url_for
)
from sqlalchemy import create_engine, desc, func, select, text
from sqlalchemy.orm import selectinload, sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.config.settings import settings
from bot.database.models import (
    Application, ApplicationStatus, ApplicationStatusEnum,
    ServiceType, User
)

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

STATUS_LABELS = {
    ApplicationStatusEnum.NEW: "New",
    ApplicationStatusEnum.IN_PROGRESS: "In Progress",
    ApplicationStatusEnum.COMPLETED: "Completed",
    ApplicationStatusEnum.REJECTED: "Rejected",
}

# Simple in-memory TTL cache for dashboard stats
_dashboard_cache = {}
_DASHBOARD_TTL = 5  # seconds


def _db_url() -> str:
    if settings.is_sqlite:
        return f"sqlite:///{settings.SQLite_DB_PATH}"
    return (
        f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )


engine_kwargs = {"echo": False}
if settings.is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    })
engine = create_engine(_db_url(), **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def _create_indexes():
    """Create missing DB indexes (idempotent, safe on existing databases)"""
    try:
        with engine.connect() as conn:
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_applications_status "
                "ON applications (status)"
            ))
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_applications_user_id "
                "ON applications (user_id)"
            ))
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS ix_applications_created_at "
                "ON applications (created_at)"
            ))
            conn.commit()
    except Exception as e:
        app.logger.error(f"Error creating indexes: {e}")


_create_indexes()


def status_label(status) -> str:
    if status is None:
        return "-"
    return STATUS_LABELS.get(status, status.value)


def format_dt(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, str):
        return value
    return value.strftime("%Y-%m-%d %H:%M")


def _telegram_send_sync(chat_id, text) -> bool:
    """Send a Telegram message via the Bot API (blocking, returns success)"""
    token = settings.BOT_TOKEN
    if not token:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urlencode({"chat_id": chat_id, "text": text}).encode()
    req = Request(url, data=data)
    try:
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read()).get("ok", False)
    except Exception as e:
        app.logger.error(f"Telegram send to {chat_id} failed: {e}")
        return False


def telegram_send(chat_id, text) -> bool:
    """Send a Telegram message in a background thread (non-blocking)"""
    threading.Thread(
        target=_telegram_send_sync, args=(chat_id, text), daemon=True
    ).start()
    return True


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == settings.ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            flash("Logged in successfully", "success")
            next_page = request.args.get("next") or url_for("dashboard")
            return redirect(next_page)
        flash("Invalid password", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "success")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    now = time.monotonic()
    cached = _dashboard_cache.get("stats")
    if cached and now - cached[0] < _DASHBOARD_TTL:
        stats, recent_apps = cached[1]
    else:
        db = SessionLocal()
        try:
            def _count(sub_query):
                return sub_query.scalar_subquery()

            users_sub = _count(select(func.count(User.id)))
            apps_sub = _count(select(func.count(Application.id)))

            status_subs = {}
            for status in ApplicationStatusEnum:
                status_subs[status] = _count(
                    select(func.count(Application.id))
                    .where(Application.status == status)
                )

            row = db.execute(
                select(
                    users_sub.label("total_users"),
                    apps_sub.label("total_applications"),
                    *[status_subs[s].label(s.value) for s in ApplicationStatusEnum],
                )
            ).one()

            stats = {
                "total_users": row.total_users or 0,
                "total_applications": row.total_applications or 0,
                "status_counts": {
                    status: getattr(row, status.value) or 0
                    for status in ApplicationStatusEnum
                },
            }

            recent_apps = db.execute(
                select(Application)
                .options(selectinload(Application.service_type))
                .order_by(desc(Application.created_at))
                .limit(5)
            ).scalars().all()
        finally:
            db.close()

        _dashboard_cache["stats"] = (now, (stats, recent_apps))

    return render_template(
        "dashboard.html",
        total_users=stats["total_users"],
        total_applications=stats["total_applications"],
        status_counts=stats["status_counts"],
        status_labels=STATUS_LABELS,
        recent_apps=recent_apps,
        status_label=status_label,
        format_dt=format_dt,
    )


@app.route("/applications")
@login_required
def applications():
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = 20
    status_filter = request.args.get("status", "").strip().lower()

    db = SessionLocal()
    try:
        query = select(Application)

        selected_status = None
        if status_filter:
            selected_status = ApplicationStatusEnum(status_filter)
            query = query.where(Application.status == selected_status)

        count_query = select(func.count(Application.id))
        if selected_status:
            count_query = count_query.where(Application.status == selected_status)
        total = db.scalar(count_query) or 0
        total_pages = max((total + per_page - 1) // per_page, 1)
        page = min(page, total_pages)

        apps = db.execute(
            query
            .options(selectinload(Application.service_type))
            .order_by(desc(Application.created_at))
            .offset((page - 1) * per_page)
            .limit(per_page)
        ).scalars().all()
    finally:
        db.close()

    return render_template(
        "applications.html",
        applications=apps,
        page=page,
        total_pages=total_pages,
        total=total,
        status_filter=status_filter,
        status_labels=STATUS_LABELS,
        status_label=status_label,
        format_dt=format_dt,
    )


@app.route("/applications/<int:application_id>")
@login_required
def application_detail(application_id):
    db = SessionLocal()
    try:
        app_obj = db.execute(
            select(Application)
            .options(selectinload(Application.service_type), selectinload(Application.user))
            .where(Application.id == application_id)
        ).scalar_one_or_none()
        if not app_obj:
            abort(404)

        history = db.execute(
            select(ApplicationStatus)
            .where(ApplicationStatus.application_id == application_id)
            .order_by(desc(ApplicationStatus.created_at))
        ).scalars().all()
    finally:
        db.close()

    return render_template(
        "application_detail.html",
        app=app_obj,
        history=history,
        status_labels=STATUS_LABELS,
        status_label=status_label,
        format_dt=format_dt,
    )


@app.route("/applications/<int:application_id>/status", methods=["POST"])
@login_required
def application_change_status(application_id):
    new_status_value = request.form.get("status", "").strip().lower()
    notes = request.form.get("notes", "").strip() or None

    try:
        new_status = ApplicationStatusEnum(new_status_value)
    except ValueError:
        flash("Invalid status", "error")
        return redirect(url_for("application_detail", application_id=application_id))

    db = SessionLocal()
    try:
        app_obj = db.execute(
            select(Application)
            .options(selectinload(Application.service_type), selectinload(Application.user))
            .where(Application.id == application_id)
        ).scalar_one_or_none()
        if not app_obj:
            abort(404)

        app_obj.status = new_status
        history = ApplicationStatus(
            application_id=application_id,
            status=new_status,
            changed_by=settings.ADMIN_ID,
            notes=notes,
        )
        db.add(history)
        db.commit()
        db.refresh(app_obj)

        user = db.get(User, app_obj.user_id)
        user_lang = user.language if user else "en"
    finally:
        db.close()

    label = status_label(new_status)
    flash(f"Application #{application_id} status changed to {label}", "success")

    if user:
        status_text = {
            "en": {"new": "New", "in_progress": "In Progress", "completed": "Completed", "rejected": "Rejected"},
            "ru": {"new": "Новая", "in_progress": "В обработке", "completed": "Завершена", "rejected": "Отклонена"},
        }.get(user_lang, {})[new_status.value]

        message = (
            f"✅ Status of application #{application_id} changed to {status_text}"
            if user_lang == "en"
            else f"✅ Статус заявки #{application_id} изменен на {status_text}"
        )
        if notes:
            message += f"\nNotes: {notes}" if user_lang == "en" else f"\nКомментарий: {notes}"

        telegram_send(user.telegram_id, message)

    return redirect(url_for("application_detail", application_id=application_id))


@app.route("/applications/<int:application_id>/delete", methods=["POST"])
@login_required
def application_delete(application_id):
    db = SessionLocal()
    user_telegram_id = None
    user_lang = "en"
    try:
        app_obj = db.execute(
            select(Application)
            .options(selectinload(Application.service_type), selectinload(Application.user))
            .where(Application.id == application_id)
        ).scalar_one_or_none()
        if not app_obj:
            abort(404)

        if app_obj.user:
            user_telegram_id = app_obj.user.telegram_id
            user_lang = app_obj.user.language or "en"

        # Delete attached file from disk if any
        if app_obj.file_path:
            try:
                if os.path.exists(app_obj.file_path):
                    os.remove(app_obj.file_path)
            except OSError as e:
                app.logger.error(f"Error deleting file {app_obj.file_path}: {e}")

        # Delete status history rows (SQLite may not enforce FK cascade)
        db.execute(
            ApplicationStatus.__table__.delete()
            .where(ApplicationStatus.application_id == application_id)
        )
        db.delete(app_obj)
        db.commit()
    finally:
        db.close()

    flash(f"Application #{application_id} deleted", "success")

    if user_telegram_id:
        message = (
            f"🗑 Application #{application_id} was deleted by the admin"
            if user_lang == "en"
            else f"🗑 Заявка #{application_id} была удалена администратором"
        )
        telegram_send(user_telegram_id, message)

    return redirect(url_for("applications"))


@app.route("/users")
@login_required
def users():
    db = SessionLocal()
    try:
        user_list = db.execute(
            select(User).order_by(desc(User.created_at))
        ).scalars().all()

        # Single GROUP BY query instead of N+1 per-user counts
        count_rows = db.execute(
            select(Application.user_id, func.count(Application.id).label("cnt"))
            .group_by(Application.user_id)
        ).all()
        app_counts = {user_id: cnt for user_id, cnt in count_rows}
    finally:
        db.close()

    return render_template(
        "users.html",
        users=user_list,
        app_counts=app_counts,
        session_admin_id=settings.ADMIN_ID,
        format_dt=format_dt,
    )


@app.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def user_delete(user_id):
    db = SessionLocal()
    try:
        user_obj = db.execute(
            select(User)
            .options(selectinload(User.applications))
            .where(User.id == user_id)
        ).scalar_one_or_none()
        if not user_obj:
            abort(404)

        if user_obj.telegram_id == settings.ADMIN_ID:
            flash("Cannot delete the admin user", "error")
            return redirect(url_for("users"))

        # Delete attached files of the user's applications
        for app_obj in user_obj.applications:
            if app_obj.file_path:
                try:
                    if os.path.exists(app_obj.file_path):
                        os.remove(app_obj.file_path)
                except OSError as e:
                    app.logger.error(f"Error deleting file {app_obj.file_path}: {e}")

        # Delete status history rows for all applications
        app_ids = [a.id for a in user_obj.applications]
        if app_ids:
            db.execute(
                ApplicationStatus.__table__.delete()
                .where(ApplicationStatus.application_id.in_(app_ids))
            )

        # Deleting the user cascades to their applications via the ORM relationship
        db.delete(user_obj)
        db.commit()
    finally:
        db.close()

    flash(f"User #{user_id} deleted", "success")
    return redirect(url_for("users"))


@app.route("/broadcast", methods=["POST"])
@login_required
def broadcast():
    text = request.form.get("message", "").strip()
    if not text:
        flash("Message is empty", "error")
        return redirect(url_for("dashboard"))

    db = SessionLocal()
    try:
        telegram_ids = db.execute(
            select(User.telegram_id).where(User.telegram_id.isnot(None))
        ).scalars().all()
    finally:
        db.close()

    sent = 0
    if telegram_ids:
        with ThreadPoolExecutor(max_workers=10) as pool:
            sent = sum(pool.map(
                lambda chat_id: _telegram_send_sync(chat_id, text), telegram_ids
            ))

    flash(f"Broadcast sent to {sent} of {len(telegram_ids)} users", "success")
    return redirect(url_for("dashboard"))


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


__all__ = ["app"]