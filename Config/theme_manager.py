"""
Theme management system for the CCO 401 Sign-Out System
"""

import json
import os

class ThemeManager:
    def __init__(self):
        self.theme_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Config",
            "theme_settings.json"
        )
        self.current_theme = self.load_theme()
        self.theme_callbacks = []
    
    def load_theme(self):
        """Load theme from settings file"""
        try:
            if os.path.exists(self.theme_file):
                with open(self.theme_file, 'r') as f:
                    data = json.load(f)
                    return data.get('theme', 'light')
        except Exception as e:
            print(f"Error loading theme: {e}")
        return 'light'  # Default theme
    
    def save_theme(self, theme):
        """Save theme to settings file"""
        try:
            os.makedirs(os.path.dirname(self.theme_file), exist_ok=True)
            with open(self.theme_file, 'w') as f:
                json.dump({'theme': theme}, f)
        except Exception as e:
            print(f"Error saving theme: {e}")
    
    def set_theme(self, theme):
        """Set the current theme and notify all registered callbacks"""
        if theme in ['light', 'dark']:
            self.current_theme = theme
            self.save_theme(theme)
            # Notify all registered windows/components
            for callback in self.theme_callbacks:
                try:
                    callback(theme)
                except Exception as e:
                    print(f"Error in theme callback: {e}")
    
    def register_callback(self, callback):
        """Register a callback to be called when theme changes"""
        self.theme_callbacks.append(callback)
    
    def unregister_callback(self, callback):
        """Unregister a theme callback"""
        if callback in self.theme_callbacks:
            self.theme_callbacks.remove(callback)
    
    def get_current_theme(self):
        """Get the current theme"""
        return self.current_theme

# Global theme manager instance
theme_manager = ThemeManager()
