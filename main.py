#!/usr/bin/env python3
"""
Main entry point for the Soldier Sign-in System
"""

import sys
import os

# Add the Windows directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Windows'))

from Windows.HomeWindow import HomeWindow

def main():
    """Main function to start the application"""
    # Create and show the Tkinter window
    window = HomeWindow("Soldier Sign-in System")
    window.show()

if __name__ == "__main__":
    main()