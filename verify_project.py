#!/usr/bin/env python3
"""
Project verification script for Application Bot
Checks that all necessary files and configurations are in place before publishing to GitHub
"""
import os
import sys
from pathlib import Path


def check_file_exists(filepath, description=""):
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        print(f"✅ {description or filepath}")
        return True
    else:
        print(f"❌ Missing: {description or filepath}")
        return False


def check_directory_exists(dirpath, description=""):
    """Check if a directory exists"""
    path = Path(dirpath)
    if path.exists() and path.is_dir():
        print(f"✅ {description or dirpath}")
        return True
    else:
        print(f"❌ Missing directory: {description or dirpath}")
        return False


def check_file_content(filepath, required_content):
    """Check if file contains required content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for required in required_content:
                if required not in content:
                    print(f"❌ {filepath} missing: {required}")
                    return False
        print(f"✅ {filepath} content validated")
        return True
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False


def main():
    """Main verification function"""
    print("=" * 60)
    print("Application Bot - Pre-Publishing Verification")
    print("=" * 60)
    print()
    
    results = []
    
    # Check project structure
    print("📁 Checking Project Structure...")
    results.append(check_directory_exists("bot", "Bot package directory"))
    results.append(check_directory_exists("bot/config", "Config directory"))
    results.append(check_directory_exists("bot/database", "Database directory"))
    results.append(check_directory_exists("bot/handlers", "Handlers directory"))
    results.append(check_directory_exists("bot/states", "States directory"))
    results.append(check_directory_exists("bot/utils", "Utils directory"))
    results.append(check_directory_exists("webadmin", "Web admin panel directory"))
    results.append(check_directory_exists("webadmin/templates", "Web admin templates directory"))
    results.append(check_directory_exists("webadmin/static", "Web admin static directory"))
    results.append(check_directory_exists("tests", "Tests directory"))
    results.append(check_directory_exists(".github", "GitHub directory"))
    results.append(check_directory_exists(".github/workflows", "GitHub workflows directory"))
    results.append(check_directory_exists(".github/ISSUE_TEMPLATE", "Issue templates directory"))
    print()
    
    # Check essential files
    print("📄 Checking Essential Files...")
    results.append(check_file_exists("README.md", "README.md (bilingual documentation)"))
    results.append(check_file_exists("LICENSE", "LICENSE file"))
    results.append(check_file_exists("CODE_OF_CONDUCT.md", "Code of Conduct"))
    results.append(check_file_exists("CONTRIBUTING.md", "Contributing Guide"))
    results.append(check_file_exists("PUBLISHING_GUIDE.md", "Publishing Guide"))
    results.append(check_file_exists("requirements.txt", "Requirements file"))
    results.append(check_file_exists("Dockerfile", "Dockerfile"))
    results.append(check_file_exists("docker-compose.yml", "Docker Compose file"))
    results.append(check_file_exists(".env.example", "Environment example file"))
    results.append(check_file_exists(".gitignore", "Git ignore file"))
    results.append(check_file_exists(".gitattributes", "Git attributes file"))
    results.append(check_file_exists(".editorconfig", "Editor config file"))
    results.append(check_file_exists("pytest.ini", "Pytest configuration"))
    results.append(check_file_exists("run.py", "Run script"))
    results.append(check_file_exists("run_admin.py", "Web admin panel run script"))
    results.append(check_file_exists("bot/__init__.py", "Bot package init"))
    results.append(check_file_exists("bot/main.py", "Main entry point"))
    results.append(check_file_exists("tests/__init__.py", "Tests package init"))
    print()
    
    # Check GitHub workflows
    print("🚀 Checking GitHub Workflows...")
    results.append(check_file_exists(".github/workflows/python-test.yml", "Python test workflow"))
    results.append(check_file_exists(".github/workflows/docker-build.yml", "Docker build workflow"))
    results.append(check_file_exists(".github/workflows/code-quality.yml", "Code quality workflow"))
    print()
    
    # Check issue templates
    print("📝 Checking Issue Templates...")
    results.append(check_file_exists(".github/ISSUE_TEMPLATE/bug_report.md", "Bug report template"))
    results.append(check_file_exists(".github/ISSUE_TEMPLATE/feature_request.md", "Feature request template"))
    results.append(check_file_exists(".github/PULL_REQUEST_TEMPLATE.md", "Pull request template"))
    print()
    
    # Check bot files
    print("🤖 Checking Bot Files...")
    results.append(check_file_exists("bot/config/settings.py", "Settings configuration"))
    results.append(check_file_exists("bot/config/bot.py", "Bot configuration"))
    results.append(check_file_exists("bot/database/models.py", "Database models"))
    results.append(check_file_exists("bot/database/database.py", "Database connection"))
    results.append(check_file_exists("bot/handlers/start.py", "Start handler"))
    results.append(check_file_exists("bot/handlers/registration.py", "Registration handler"))
    results.append(check_file_exists("bot/handlers/application.py", "Application handler"))
    results.append(check_file_exists("bot/handlers/language.py", "Language handler"))
    results.append(check_file_exists("bot/handlers/common.py", "Common handler"))
    results.append(check_file_exists("bot/states/application.py", "Application states"))
    results.append(check_file_exists("bot/states/registration.py", "Registration states"))
    results.append(check_file_exists("bot/utils/translations.py", "Translations utility"))
    results.append(check_file_exists("bot/utils/keyboards.py", "Keyboards utility"))
    results.append(check_file_exists("bot/utils/file_handler.py", "File handler utility"))
    results.append(check_file_exists("bot/utils/validators.py", "Validators utility"))
    results.append(check_file_exists("webadmin/app.py", "Web admin panel app"))
    results.append(check_file_exists("webadmin/templates/base.html", "Web admin base template"))
    results.append(check_file_exists("webadmin/templates/login.html", "Web admin login template"))
    results.append(check_file_exists("webadmin/templates/dashboard.html", "Web admin dashboard template"))
    results.append(check_file_exists("webadmin/templates/applications.html", "Web admin applications template"))
    results.append(check_file_exists("webadmin/templates/application_detail.html", "Web admin application detail template"))
    results.append(check_file_exists("webadmin/templates/users.html", "Web admin users template"))
    results.append(check_file_exists("webadmin/static/style.css", "Web admin stylesheet"))
    print()
    
    # Check test files
    print("🧪 Checking Test Files...")
    results.append(check_file_exists("tests/conftest.py", "Test configuration"))
    results.append(check_file_exists("tests/test_translations.py", "Translation tests"))
    results.append(check_file_exists("tests/test_validators.py", "Validator tests"))
    results.append(check_file_exists("tests/test_database.py", "Database tests"))
    results.append(check_file_exists("tests/test_file_handler.py", "File handler tests"))
    results.append(check_file_exists("tests/test_keyboards.py", "Keyboard tests"))
    results.append(check_file_exists("tests/test_settings_simple.py", "Settings tests"))
    results.append(check_file_exists("tests/run_tests.py", "Test runner"))
    results.append(check_file_exists("tests/SUMMARY.md", "Test summary"))
    print()
    
    # Check content of key files
    print("📖 Checking File Content...")
    results.append(check_file_content("README.md", ["Application Bot", "Telegram bot", "Features", "Installation"]))
    results.append(check_file_content("LICENSE", ["MIT License", "Copyright"]))
    results.append(check_file_content("requirements.txt", ["aiogram", "SQLAlchemy", "pydantic"]))
    results.append(check_file_content("Dockerfile", ["FROM python", "WORKDIR /app", "CMD"]))
    results.append(check_file_content("docker-compose.yml", ["version", "services", "bot", "postgres"]))
    print()
    
    # Summary
    print("=" * 60)
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    if failed == 0:
        print(f"🎉 All checks passed! ({passed}/{total})")
        print("✅ Project is ready for publishing to GitHub!")
    else:
        print(f"⚠️  {failed} checks failed, {passed} passed ({passed}/{total})")
        print("❌ Please fix the issues above before publishing.")
    
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
