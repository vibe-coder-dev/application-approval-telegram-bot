#!/usr/bin/env python3
"""
Main entry point for the web admin panel (Flask)
"""
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webadmin.app import app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=10000, debug=False)