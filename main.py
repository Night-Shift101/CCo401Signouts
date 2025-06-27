#!/usr/bin/env python3
"""
Main entry point for the Soldier Sign-in System
"""

import sys
import os

# Add the Windows directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Windows'))

from Windows.LoadingScreen import LoadingScreen
from Windows.HomeWindow import HomeWindow

def start_main_application():
    """Start the main application after loading is complete"""
    window = HomeWindow("Soldier Sign-in System")
    window.show()

def main():
    """Main function to start the application with loading screen"""
    # Show loading screen first, then start main application
    loading_screen = LoadingScreen(on_complete_callback=start_main_application)
    loading_screen.show()

if __name__ == "__main__":
    main()