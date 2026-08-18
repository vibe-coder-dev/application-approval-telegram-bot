"""
File handling utilities for uploads
"""
import os
import uuid
from datetime import datetime
from typing import Optional, Tuple
from pathlib import Path
from ..config.settings import settings
import logging

logger = logging.getLogger(__name__)


def ensure_upload_dir():
    """Ensure upload directory exists"""
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for different file types
    (upload_dir / "photos").mkdir(parents=True, exist_ok=True)
    (upload_dir / "documents").mkdir(parents=True, exist_ok=True)
    (upload_dir / "files").mkdir(parents=True, exist_ok=True)


def generate_filename(extension: str = "") -> str:
    """Generate unique filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    if extension:
        if not extension.startswith("."):
            extension = f".{extension}"
        return f"{timestamp}_{unique_id}{extension}"
    
    return f"{timestamp}_{unique_id}"


def save_file(
    file_data: bytes,
    file_name: str,
    file_type: str = "file"
) -> Tuple[str, str]:
    """
    Save uploaded file to disk
    
    Args:
        file_data: Binary file data
        file_name: Original file name
        file_type: Type of file (photo, document, file)
    
    Returns:
        Tuple of (saved_path, file_type)
    """
    ensure_upload_dir()
    
    # Determine file extension
    if file_name:
        extension = os.path.splitext(file_name)[1].lower()
    else:
        extension = ""
    
    # Generate unique filename
    unique_filename = generate_filename(extension)
    
    # Determine subdirectory based on file type
    if file_type == "photo":
        subdir = "photos"
    elif file_type == "document":
        subdir = "documents"
    else:
        subdir = "files"
    
    # Create full path
    upload_dir = Path(settings.UPLOAD_DIR) / subdir
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = str(upload_dir / unique_filename)
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    logger.info(f"File saved: {file_path}")
    
    return file_path, unique_filename


def delete_file(file_path: str) -> bool:
    """Delete a file from disk"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {e}")
        return False


def get_file_path(file_id: str) -> Optional[str]:
    """Get full path for a stored file"""
    upload_dir = Path(settings.UPLOAD_DIR)
    
    # Search in all subdirectories
    for subdir in ["photos", "documents", "files"]:
        path = upload_dir / subdir / file_id
        if path.exists():
            return str(path)
    
    # Check root upload directory
    path = upload_dir / file_id
    if path.exists():
        return str(path)
    
    return None


def get_file_info(file_path: str) -> dict:
    """Get file information"""
    if not file_path or not os.path.exists(file_path):
        return {"exists": False}
    
    stat = os.stat(file_path)
    return {
        "exists": True,
        "path": file_path,
        "name": os.path.basename(file_path),
        "size": stat.st_size,
        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "extension": os.path.splitext(file_path)[1].lower()
    }


def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> bool:
    """Validate file size"""
    return file_size <= max_size


def get_allowed_extensions() -> list:
    """Get list of allowed file extensions"""
    return [
        # Images
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
        # Documents
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.rtf',
        # Archives
        '.zip', '.rar', '.7z', '.tar', '.gz',
        # Other
        '.csv', '.json', '.xml'
    ]


def is_allowed_extension(extension: str) -> bool:
    """Check if file extension is allowed"""
    allowed = get_allowed_extensions()
    return extension.lower() in allowed
