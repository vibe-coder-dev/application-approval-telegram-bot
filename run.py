#!/usr/bin/env python3
"""
Main entry point for running the Application Bot
"""
import asyncio
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.main import main

if __name__ == "__main__":
    asyncio.run(main())
