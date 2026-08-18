#!/usr/bin/env python3
"""
Test runner script for Application Bot
"""
import subprocess
import sys
import os


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Application Bot - Test Runner")
    print("=" * 60)
    
    # Set test environment variables
    env = os.environ.copy()
    env.update({
        'BOT_TOKEN': 'test_token_for_testing',
        'ADMIN_ID': '123456789',
        'DB_TYPE': 'sqlite',
        'SQLite_DB_PATH': 'data/test_bot.db',
        'UPLOAD_DIR': 'uploads_test',
        'DEFAULT_LANGUAGE': 'en',
        'AVAILABLE_LANGUAGES': 'en,ru'
    })
    
    # Run pytest
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=short'],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=env,
            capture_output=False
        )
        
        print("=" * 60)
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
        print("=" * 60)
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
