import tkinter as tk
from tkinter import ttk
import os
import sys
import threading
import time

# Try to import PIL, but handle gracefully if not available
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow not available - using fallback for images")

# Add parent directory to path to import colors
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.colors import (
    BG_PRIMARY, WHITE, GRAY_700, ONXY, PRIMARY_BLUE, GRAY_200, 
    GRAY_100, SUCCESS, TEXT_PRIMARY, get_theme_colors
)
from Config.theme_manager import theme_manager

class LoadingScreen:
    def __init__(self, on_complete_callback=None):
        """
        Initialize the loading screen
        
        Args:
            on_complete_callback: Function to call when loading is complete
        """
        self.on_complete_callback = on_complete_callback
        self.root = tk.Tk()
        self.root.title("CCO 401 Sign-Out System")
        self.root.configure(bg=WHITE)
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Remove window decorations for a cleaner loading screen look
        self.root.overrideredirect(True)
        
        # Center the window
        self.center_window()
        
        # Variables for progress tracking
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Initializing...")
        
        # Create the UI
        self.create_ui()
        
        # Apply current theme
        self.apply_current_theme()
        
        # Start the loading process
        self.start_loading()
    
    def center_window(self):
        """Center the loading screen on the display"""
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (400 // 2)
        
        self.root.geometry(f"600x400+{x}+{y}")
    
    def create_ui(self):
        """Create the loading screen UI elements"""
        # Main container with border
        self.main_container = tk.Frame(
            self.root, 
            bg=WHITE, 
            relief="solid", 
            bd=2, 
            highlightbackground=GRAY_200,
            highlightthickness=1
        )
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Top section with logo and title
        top_section = tk.Frame(self.main_container, bg=WHITE, height=250)
        top_section.pack(fill=tk.X, padx=40, pady=(40, 20))
        top_section.pack_propagate(False)
        
        # Logo container
        logo_container = tk.Frame(top_section, bg=WHITE)
        logo_container.pack(pady=(0, 20))
        
        # Try to load and display the CCO logo
        if PIL_AVAILABLE:
            try:
                logo_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                    "Assets", 
                    "CcoLogo.png"
                )
                
                logo_image = Image.open(logo_path)
                # Make the logo larger for the loading screen
                logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(
                    logo_container,
                    image=self.logo_photo,
                    bg=WHITE
                )
                logo_label.pack()
                
            except Exception as e:
                # Fallback if logo can't be loaded
                self.create_fallback_logo(logo_container)
                print(f"Could not load logo: {e}")
        else:
            # Fallback if PIL is not available
            self.create_fallback_logo(logo_container)
        
        # Title
        title_label = tk.Label(
            top_section,
            text="CCO 401 SIGN-OUT SYSTEM",
            bg=WHITE,
            fg=ONXY,
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            top_section,
            text="Loading Application...",
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 14)
        )
        subtitle_label.pack()
        
        # Progress section
        progress_section = tk.Frame(self.main_container, bg=WHITE)
        progress_section.pack(fill=tk.X, padx=40, pady=(0, 40))
        
        # Status label
        self.status_label = tk.Label(
            progress_section,
            textvariable=self.status_var,
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 12)
        )
        self.status_label.pack(pady=(0, 15))
        
        # Progress bar container for custom styling
        progress_container = tk.Frame(progress_section, bg=WHITE)
        progress_container.pack(fill=tk.X, pady=(0, 10))
        
        # Create custom progress bar using Canvas
        self.progress_canvas = tk.Canvas(
            progress_container,
            width=400,
            height=20,
            bg=WHITE,
            highlightthickness=0
        )
        self.progress_canvas.pack()
        
        # Draw progress bar background
        self.progress_bg = self.progress_canvas.create_rectangle(
            0, 0, 400, 20,
            fill=GRAY_100,
            outline=GRAY_200,
            width=1
        )
        
        # Draw progress bar fill (initially empty)
        self.progress_fill = self.progress_canvas.create_rectangle(
            0, 0, 0, 20,
            fill=PRIMARY_BLUE,
            outline=""
        )
        
        # Progress percentage label
        self.progress_label = tk.Label(
            progress_section,
            text="0%",
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 10)
        )
        self.progress_label.pack()
    
    def create_fallback_logo(self, parent):
        """Create a fallback logo when image loading isn't available"""
        fallback_logo = tk.Label(
            parent,
            text="CCO",
            bg=WHITE,
            fg=ONXY,
            font=("Arial", 36, "bold")
        )
        fallback_logo.pack()
    
    def update_progress(self, progress, status):
        """
        Update the progress bar and status
        
        Args:
            progress: Progress value (0-100)
            status: Status message string
        """
        # Update progress bar
        fill_width = (progress / 100) * 400
        self.progress_canvas.coords(self.progress_fill, 0, 0, fill_width, 20)
        
        # Update status and percentage
        self.status_var.set(status)
        self.progress_label.config(text=f"{int(progress)}%")
        
        # Update the display
        self.root.update()
    
    def start_loading(self):
        """Start the loading process in a separate thread"""
        def loading_process():
            loading_steps = [
                (15, "Initializing system..."),
                (30, "Loading security modules..."),
                (45, "Connecting to data management..."),
                (60, "Setting up user interface..."),
                (75, "Preparing authentication..."),
                (90, "Finalizing setup..."),
                (100, "Ready to launch!")
            ]
            
            for progress, status in loading_steps:
                self.update_progress(progress, status)
                time.sleep(0.6)  # Slightly longer for better visual effect
            
            # Wait a moment on completion
            time.sleep(0.8)
            
            # Close loading screen and call completion callback
            self.root.after(0, self.complete_loading)
        
        # Start loading in a separate thread to prevent UI freezing
        loading_thread = threading.Thread(target=loading_process, daemon=True)
        loading_thread.start()
    
    def complete_loading(self):
        """Complete the loading process and close the screen"""
        self.root.destroy()
        
        if self.on_complete_callback:
            self.on_complete_callback()
    
    def show(self):
        """Display the loading screen"""
        # Bring window to front
        self.root.lift()
        self.root.focus_force()
        
        # Start the main loop
        self.root.mainloop()
    
    def apply_current_theme(self):
        """Apply the current theme to the loading screen"""
        try:
            current_theme = theme_manager.get_current_theme()
            colors = get_theme_colors(current_theme)
            
            # Update window background
            self.root.configure(bg=colors['WHITE'])
            
            # Update main container if it exists
            if hasattr(self, 'main_container'):
                self.main_container.configure(bg=colors['WHITE'])
                
        except Exception as e:
            print(f"Error applying theme to LoadingScreen: {e}")

if __name__ == "__main__":
    # Test the loading screen
    def on_complete():
        print("Loading completed!")
    
    loading = LoadingScreen(on_complete)
    loading.show()
