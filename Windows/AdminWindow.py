import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime

# Try to import PIL, but handle gracefully if not available
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.colors import (
    BG_PRIMARY, WHITE, GRAY_700, ONXY, PRIMARY_BLUE, GRAY_200, 
    GRAY_100, SUCCESS, TEXT_PRIMARY, GRAY_600, BUTTON_PRIMARY, GRAY_300
)

class AdminWindow:
    def __init__(self, parent=None, current_ds=None):
        """
        Initialize the Admin Window
        
        Args:
            parent: Parent window (HomeWindow)
            current_ds: Currently authenticated drill sergeant
        """
        self.parent = parent
        self.current_ds = current_ds
        
        # Track unsaved changes
        self.has_unsaved_changes = False
        self.original_values = {}  # Store original values for comparison
        self.setting_vars = {}  # Store all setting variables
        
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("CCO 401 Admin Panel")
        self.root.configure(bg=BG_PRIMARY)
        self.root.geometry("1000x700")  # Made wider for better settings display
        self.root.resizable(True, True)
        
        if parent:
            self.root.transient(parent)
            self.root.grab_set()
        
        # Bind window close event to check for unsaved changes
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Apply current theme and register for changes
        self.apply_current_theme()
        self.register_for_theme_changes()
        
        self.center_window()
        self.create_ui()
    
    def center_window(self):
        """Center the admin window on the screen"""
        self.root.update_idletasks()
        
        if self.parent:
            # Center relative to parent
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            x = parent_x + (parent_width // 2) - (1000 // 2)
            y = parent_y + (parent_height // 2) - (700 // 2)
        else:
            # Center on screen
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width // 2) - (1000 // 2)
            y = (screen_height // 2) - (700 // 2)
        
        self.root.geometry(f"1000x700+{x}+{y}")
    
    def create_ui(self):
        """Create the admin panel UI"""
        # Create top bar
        self.create_top_bar()
        
        # Create main content area
        self.create_main_content()
        
        # Create bottom bar with close button
        self.create_bottom_bar()
    
    def create_top_bar(self):
        """Create the top bar with title and user info"""
        self.top_bar = tk.Frame(self.root, bg=ONXY, height=80)
        self.top_bar.pack(fill=tk.X, side=tk.TOP)
        self.top_bar.pack_propagate(False)
        
        # Try to load logo
        try:
            logo_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                "Assets", 
                "CcoLogo.png"
            )
            
            if PIL_AVAILABLE:
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(
                    self.top_bar,
                    image=self.logo_photo,
                    bg=ONXY
                )
                logo_label.place(x=15, y=10)
            else:
                self.create_fallback_logo()
                
        except Exception as e:
            self.create_fallback_logo()
            print(f"Could not load logo: {e}")
        
        # Title
        title_frame = tk.Frame(self.top_bar, bg=ONXY)
        title_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(
            title_frame,
            text="ADMIN PANEL",
            bg=ONXY,
            fg=WHITE,
            font=("Arial", 22, "bold")
        )
        title_label.pack()
        
        # Current user info
        if self.current_ds:
            user_label = tk.Label(
                self.top_bar,
                text=f"DS: {self.current_ds}",
                bg=ONXY,
                fg=WHITE,
                font=("Arial", 12)
            )
            user_label.place(relx=1.0, x=-15, y=30, anchor='ne')
    
    def create_fallback_logo(self):
        """Create fallback logo when image loading fails"""
        fallback_logo = tk.Label(
            self.top_bar,
            text="CCO",
            bg=ONXY,
            fg=WHITE,
            font=("Arial", 16, "bold")
        )
        fallback_logo.place(x=15, y=30)
    
    def create_main_content(self):
        """Create the main content area with tabbed settings panel"""
        # Main container
        main_container = tk.Frame(self.root, bg=BG_PRIMARY)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Content frame
        content_frame = tk.Frame(main_container, bg=WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs at the top
        self.create_tabs(content_frame)
        
        # Settings content area below tabs
        self.settings_content_frame = tk.Frame(content_frame, bg=WHITE)
        self.settings_content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        # Initialize with first tab (Appearance)
        self.current_tab = "My Account"
        self.show_tab_content(self.current_tab)
    
    def create_tabs(self, parent):
        """Create the tabs for settings sections"""
        # Tabs container
        tabs_frame = tk.Frame(parent, bg=WHITE)
        tabs_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        # Tab definitions
        self.tabs = ["My Account", "Accounts",]
        self.tab_buttons = []
        
        # Create tab buttons
        for i, tab in enumerate(self.tabs):
            tab_canvas = tk.Canvas(
                tabs_frame,
                width=150,
                height=40,
                bg=WHITE,
                highlightthickness=0,
                cursor="hand2"
            )
            tab_canvas.pack(side=tk.LEFT, padx=(0, 5))
            
            # Draw tab background
            def draw_tab_bg(canvas, is_active=False):
                canvas.delete("tab_bg")
                fill_color = PRIMARY_BLUE if is_active else GRAY_100
                radius = 8
                x1, y1, x2, y2 = 2, 2, 148, 38
                
                # Create rounded rectangle (only top corners)
                canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                                start=90, extent=90, fill=fill_color, outline=fill_color, tags="tab_bg")
                canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                                start=0, extent=90, fill=fill_color, outline=fill_color, tags="tab_bg")
                canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                      fill=fill_color, outline=fill_color, tags="tab_bg")
                canvas.create_rectangle(x1, y1 + radius, x2, y2, 
                                      fill=fill_color, outline=fill_color, tags="tab_bg")
            
            # Initial state
            is_active = (i == 0)  # First tab active by default
            draw_tab_bg(tab_canvas, is_active)
            
            # Tab text
            text_color = WHITE if is_active else GRAY_700
            font_weight = "bold" if is_active else "normal"
            tab_canvas.create_text(
                75, 20,
                text=tab,
                fill=text_color,
                font=("Arial", 11, font_weight),
                tags="text"
            )
            
            # Store tab button reference
            self.tab_buttons.append((tab_canvas, tab))
            
            # Create click handler
            def create_tab_click_handler(tab_name, canvas):
                def handler(event=None):
                    self.select_tab(tab_name)
                return handler
            
            click_handler = create_tab_click_handler(tab, tab_canvas)
            tab_canvas.bind("<Button-1>", click_handler)
            
            # Create hover handlers
            def create_tab_hover_handlers(canvas, tab_name):
                def on_enter(event):
                    if tab_name != self.current_tab:
                        draw_tab_bg(canvas, False)
                        canvas.itemconfig("text", fill=GRAY_600)
                        canvas.tag_raise("text")
                
                def on_leave(event):
                    if tab_name != self.current_tab:
                        draw_tab_bg(canvas, False)
                        canvas.itemconfig("text", fill=GRAY_700)
                        canvas.tag_raise("text")
                
                return on_enter, on_leave
            
            enter_handler, leave_handler = create_tab_hover_handlers(tab_canvas, tab)
            tab_canvas.bind("<Enter>", enter_handler)
            tab_canvas.bind("<Leave>", leave_handler)
    
    def select_tab(self, tab_name):
        """Select a tab and update the display"""
        self.current_tab = tab_name
        
        # Update visual states of tab buttons
        for canvas, tab in self.tab_buttons:
            is_active = (tab == tab_name)
            
            # Redraw tab background
            canvas.delete("tab_bg")
            fill_color = PRIMARY_BLUE if is_active else GRAY_100
            radius = 8
            x1, y1, x2, y2 = 2, 2, 148, 38
            
            canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                            start=90, extent=90, fill=fill_color, outline=fill_color, tags="tab_bg")
            canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                            start=0, extent=90, fill=fill_color, outline=fill_color, tags="tab_bg")
            canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                  fill=fill_color, outline=fill_color, tags="tab_bg")
            canvas.create_rectangle(x1, y1 + radius, x2, y2, 
                                  fill=fill_color, outline=fill_color, tags="tab_bg")
            
            # Update text
            text_color = WHITE if is_active else GRAY_700
            font_weight = "bold" if is_active else "normal"
            canvas.itemconfig("text", fill=text_color, font=("Arial", 11, font_weight))
            canvas.tag_raise("text")
        
        # Show the selected tab content
        self.show_tab_content(tab_name)
    
    def show_tab_content(self, tab_name):
        """Show the content for the selected tab"""
        # Clear the current content
        for widget in self.settings_content_frame.winfo_children():
            widget.destroy()
        
        # Create title for the settings area
        title_label = tk.Label(
            self.settings_content_frame,
            text=f"{tab_name} Settings",
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 18, "bold")
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Create scrollable frame for settings
        canvas = tk.Canvas(self.settings_content_frame, bg=WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.settings_content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Show content based on selected tab
        if tab_name == "Accounts":
            self.create_accounts_settings(scrollable_frame)
        elif tab_name == "My Account":
            self.create_my_account_settings(scrollable_frame)
    
    def create_appearance_settings(self, parent):
        """Create appearance settings with theme selection"""
        # Import theme manager
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from Config.theme_manager import theme_manager
        
        # Theme settings section
        self.create_settings_section(parent, "Theme Settings", [
            ("Application Theme", theme_manager.get_current_theme(), "theme_selector"),
            ("Window Transparency", False, "checkbox"),
            ("Animations", True, "checkbox"),
        ])
        
        # Display settings
        self.create_settings_section(parent, "Display Settings", [
            ("Font Size", "Medium", "dropdown", ["Small", "Medium", "Large"]),
            ("Button Style", "Rounded", "dropdown", ["Rounded", "Square"]),
            ("Show Tooltips", True, "checkbox"),
        ])
    
    def create_accounts_settings(self, parent):
        """Create accounts settings (placeholder for now)"""
        placeholder_label = tk.Label(
            parent,
            text="Accounts settings will be implemented in a future update.",
            bg=WHITE,
            fg=GRAY_600,
            font=("Arial", 14),
            justify=tk.CENTER
        )
        placeholder_label.pack(expand=True, pady=50)
    
    def create_my_account_settings(self, parent):
        """Create my account settings (placeholder for now)"""
        placeholder_label = tk.Label(
            parent,
            text="My Account settings will be implemented in a future update.",
            bg=WHITE,
            fg=GRAY_600,
            font=("Arial", 14),
            justify=tk.CENTER
        )
        placeholder_label.pack(expand=True, pady=50)
    
    def create_settings_section(self, parent, title, settings_list):
        """Create a settings section with title and setting items"""
        # Section container
        section_frame = tk.Frame(parent, bg=WHITE)
        section_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Section title
        title_label = tk.Label(
            section_frame,
            text=title,
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 14, "bold")
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Settings items
        for setting in settings_list:
            self.create_setting_item(section_frame, *setting)
            ("Failed Login Attempts", "3", "entry")
        
        
        # DS List
        ds_frame = tk.Frame(parent, bg=WHITE)
        ds_frame.pack(fill=tk.X, pady=(20, 0))
        
        ds_title = tk.Label(ds_frame, text="Registered Drill Sergeants", bg=WHITE, fg=GRAY_700, font=("Arial", 14, "bold"))
        ds_title.pack(anchor="w", pady=(0, 10))
        
        # Placeholder for DS list
        ds_placeholder = tk.Label(
            ds_frame, 
            text="• DS Management functionality will be implemented here\n• Add/Remove Drill Sergeants\n• Reset PINs\n• View Activity Logs",
            bg=GRAY_100, 
            fg=GRAY_600,
            font=("Arial", 10),
            justify=tk.LEFT,
            anchor="w"
        )
        ds_placeholder.pack(fill=tk.X, ipady=15, ipadx=15)
    
    def create_data_management(self, parent):
        """Create data management content"""
        self.create_settings_section(parent, "Data Storage Settings", [
            ("Auto-backup Enabled", True, "checkbox"),
            ("Backup Frequency", "Daily", "dropdown", ["Hourly", "Daily", "Weekly"]),
            ("Data Retention Days", "365", "entry"),
            ("Archive Old Records", True, "checkbox")
        ])
        
        # Action buttons
        actions_frame = tk.Frame(parent, bg=WHITE)
        actions_frame.pack(fill=tk.X, pady=(20, 0))
        
        actions_title = tk.Label(actions_frame, text="Data Actions", bg=WHITE, fg=GRAY_700, font=("Arial", 14, "bold"))
        actions_title.pack(anchor="w", pady=(0, 15))
        
        buttons_frame = tk.Frame(actions_frame, bg=WHITE)
        buttons_frame.pack(fill=tk.X)
        
        self.create_rounded_button(buttons_frame, "Export Data", lambda: self.show_placeholder("Export Data"), bg_color=SUCCESS, side="left", padx=(0, 10))
        self.create_rounded_button(buttons_frame, "Import Data", lambda: self.show_placeholder("Import Data"), bg_color=PRIMARY_BLUE, side="left", padx=(0, 10))
        self.create_rounded_button(buttons_frame, "Clear Old Data", lambda: self.show_placeholder("Clear Old Data"), bg_color=GRAY_600, side="left")
    
    def create_security_settings(self, parent):
        """Create security settings content"""
        self.create_settings_section(parent, "Authentication Settings", [
            ("Require PIN for All Actions", True, "checkbox"),
            ("PIN Complexity Required", True, "checkbox"),
            ("Two-Factor Authentication", False, "checkbox"),
            ("Session Auto-lock", True, "checkbox")
        ])
        
        self.create_settings_section(parent, "Access Control", [
            ("Admin PIN Required", True, "checkbox"),
            ("Audit All Actions", True, "checkbox"),
            ("Log Failed Attempts", True, "checkbox"),
            ("Alert on Suspicious Activity", False, "checkbox")
        ])
    
    def create_reports_analytics(self, parent):
        """Create reports and analytics content"""
        self.create_settings_section(parent, "Report Settings", [
            ("Auto-generate Daily Reports", False, "checkbox"),
            ("Include Personal Data", False, "checkbox"),
            ("Report Format", "PDF", "dropdown", ["PDF", "Excel", "CSV"]),
            ("Email Reports", False, "checkbox")
        ])
        
        # Report generation
        reports_frame = tk.Frame(parent, bg=WHITE)
        reports_frame.pack(fill=tk.X, pady=(20, 0))
        
        reports_title = tk.Label(reports_frame, text="Generate Reports", bg=WHITE, fg=GRAY_700, font=("Arial", 14, "bold"))
        reports_title.pack(anchor="w", pady=(0, 15))
        
        buttons_frame = tk.Frame(reports_frame, bg=WHITE)
        buttons_frame.pack(fill=tk.X)
        
        self.create_rounded_button(buttons_frame, "Daily Report", lambda: self.show_placeholder("Daily Report"), bg_color=PRIMARY_BLUE, side="left", padx=(0, 10))
        self.create_rounded_button(buttons_frame, "Weekly Summary", lambda: self.show_placeholder("Weekly Summary"), bg_color=SUCCESS, side="left", padx=(0, 10))
        self.create_rounded_button(buttons_frame, "Custom Report", lambda: self.show_placeholder("Custom Report"), bg_color=GRAY_600, side="left")
    
    def create_system_logs(self, parent):
        """Create system logs content"""
        self.create_settings_section(parent, "Logging Settings", [
            ("Enable System Logging", True, "checkbox"),
            ("Log Level", "INFO", "dropdown", ["DEBUG", "INFO", "WARNING", "ERROR"]),
            ("Max Log File Size", "10 MB", "dropdown", ["1 MB", "5 MB", "10 MB", "50 MB"]),
            ("Keep Log Files", "30 days", "dropdown", ["7 days", "30 days", "90 days", "1 year"])
        ])
        
        # Log viewer placeholder
        logs_frame = tk.Frame(parent, bg=WHITE)
        logs_frame.pack(fill=tk.X, pady=(20, 0))
        
        logs_title = tk.Label(logs_frame, text="Recent System Logs", bg=WHITE, fg=GRAY_700, font=("Arial", 14, "bold"))
        logs_title.pack(anchor="w", pady=(0, 10))
        
        logs_placeholder = tk.Label(
            logs_frame,
            text="System log viewer will be implemented here\n• View real-time logs\n• Filter by date/level\n• Export log files",
            bg=GRAY_100,
            fg=GRAY_600,
            font=("Arial", 10),
            justify=tk.LEFT,
            anchor="w"
        )
        logs_placeholder.pack(fill=tk.X, ipady=15, ipadx=15)
    
    def create_backup_restore(self, parent):
        """Create backup and restore content"""
        self.create_settings_section(parent, "Backup Configuration", [
            ("Automatic Backups", True, "checkbox"),
            ("Backup Location", "/backups", "entry"),
            ("Compress Backups", True, "checkbox"),
            ("Max Backup Files", "10", "entry")
        ])
        
        # Backup actions
        backup_frame = tk.Frame(parent, bg=WHITE)
        backup_frame.pack(fill=tk.X, pady=(20, 0))
        
        backup_title = tk.Label(backup_frame, text="Backup & Restore Actions", bg=WHITE, fg=GRAY_700, font=("Arial", 14, "bold"))
        backup_title.pack(anchor="w", pady=(0, 15))
        
        buttons_frame = tk.Frame(backup_frame, bg=WHITE)
        buttons_frame.pack(fill=tk.X)
        
        self.create_rounded_button(buttons_frame, "Create Backup", lambda: self.show_placeholder("Create Backup"), bg_color=SUCCESS, side="left", padx=(0, 10))
        self.create_rounded_button(buttons_frame, "Restore Data", lambda: self.show_placeholder("Restore Data"), bg_color=GRAY_600, side="left", padx=(0, 10))
        self.create_rounded_button(buttons_frame, "Schedule Backup", lambda: self.show_placeholder("Schedule Backup"), bg_color=PRIMARY_BLUE, side="left")
    
    def create_application_settings(self, parent):
        """Create application settings content"""
        self.create_settings_section(parent, "Application Behavior", [
            ("Start Minimized", False, "checkbox"),
            ("Check for Updates", True, "checkbox"),
            ("Enable Error Reporting", True, "checkbox"),
            ("Remember Window Position", True, "checkbox")
        ])
        
        self.create_settings_section(parent, "Performance Settings", [
            ("Enable Hardware Acceleration", True, "checkbox"),
            ("Cache Size", "50 MB", "dropdown", ["10 MB", "50 MB", "100 MB", "500 MB"]),
            ("Startup Optimization", True, "checkbox"),
            ("Background Processing", True, "checkbox")
        ])
    
    def create_settings_section(self, parent, title, settings_list):
        """Create a settings section with title and setting items"""
        # Section container
        section_frame = tk.Frame(parent, bg=WHITE)
        section_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Section title
        title_label = tk.Label(
            section_frame,
            text=title,
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 14, "bold")
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Settings items
        for setting in settings_list:
            self.create_setting_item(section_frame, *setting)
    
    def create_setting_item(self, parent, label_text, default_value, setting_type, options=None):
        """Create an individual setting item with full-width grey boxes and curved corners"""
        # Create a unique key for this setting
        setting_key = f"{label_text}_{setting_type}"
        
        # Main container - absolutely no padding
        item_frame = tk.Frame(parent, bg=WHITE)
        item_frame.pack(fill=tk.X, pady=8, padx=0)
        
        # Canvas for rounded background that fills completely to edges
        canvas = tk.Canvas(item_frame, height=80, bg=WHITE, highlightthickness=0, bd=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Draw rounded rectangle background that fills the entire available width
        def draw_setting_bg():
            canvas.delete("setting_bg")
            canvas.update_idletasks()
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Force update if canvas dimensions aren't ready
            if width <= 1 or height <= 1:
                canvas.after(50, draw_setting_bg)
                return
            
            # Ensure we have the actual parent width
            parent_width = canvas.master.winfo_width()
            if parent_width > width and parent_width > 1:
                width = parent_width
                
            radius = 12
            # Use entire available width with no margins
            x1, y1, x2, y2 = 0, 0, width, height
            
            # Create rounded rectangle that fills the entire available width
            canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                            start=90, extent=90, fill=GRAY_100, outline=GRAY_100, tags="setting_bg")
            canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                            start=0, extent=90, fill=GRAY_100, outline=GRAY_100, tags="setting_bg")
            canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                            start=180, extent=90, fill=GRAY_100, outline=GRAY_100, tags="setting_bg")
            canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                            start=270, extent=90, fill=GRAY_100, outline=GRAY_100, tags="setting_bg")
            canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                  fill=GRAY_100, outline=GRAY_100, tags="setting_bg")
            canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                                  fill=GRAY_100, outline=GRAY_100, tags="setting_bg")
        
        # Bind canvas resize to redraw background
        canvas.bind("<Configure>", lambda e: draw_setting_bg())
        
        # Initial draw with delay to ensure canvas is ready
        canvas.after(100, draw_setting_bg)
        
        # Frame for content inside the canvas
        content_frame = tk.Frame(canvas, bg=GRAY_100)
        canvas.create_window(20, 10, window=content_frame, anchor="nw")
        
        # Label
        label = tk.Label(
            content_frame,
            text=label_text,
            bg=GRAY_100,
            fg=GRAY_700,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        label.pack(anchor="w", pady=(5, 8))
        
        # Setting control based on type
        var = None
        if setting_type == "entry":
            var = tk.StringVar(value=default_value)
            entry = tk.Entry(
                content_frame,
                textvariable=var,
                font=("Arial", 11),
                bg=WHITE,
                fg=GRAY_700,
                relief="flat",
                bd=1,
                insertbackground=GRAY_700,
                width=35
            )
            entry.pack(anchor="w", ipady=6)
            
            # Bind change event
            var.trace('w', lambda *args: self.on_setting_changed(setting_key, var.get()))
            
        elif setting_type == "dropdown":
            var = tk.StringVar(value=default_value)
            
            dropdown = ttk.Combobox(
                content_frame,
                textvariable=var,
                values=options,
                state="readonly",
                font=("Arial", 11),
                width=32
            )
            dropdown.pack(anchor="w", ipady=2)
            
            # Bind change event
            var.trace('w', lambda *args: self.on_setting_changed(setting_key, var.get()))
            
        elif setting_type == "theme_selector":
            var = tk.StringVar(value=default_value)
            
            # Theme selector with light/dark toggle
            theme_frame = tk.Frame(content_frame, bg=GRAY_100)
            theme_frame.pack(anchor="w")
            
            # Light theme button
            light_canvas = tk.Canvas(
                theme_frame,
                width=80,
                height=30,
                bg=GRAY_100,
                highlightthickness=0,
                cursor="hand2"
            )
            light_canvas.pack(side=tk.LEFT, padx=(0, 10))
            
            # Dark theme button
            dark_canvas = tk.Canvas(
                theme_frame,
                width=80,
                height=30,
                bg=GRAY_100,
                highlightthickness=0,
                cursor="hand2"
            )
            dark_canvas.pack(side=tk.LEFT)
            
            def draw_theme_buttons():
                # Light theme button
                light_canvas.delete("all")
                light_bg = PRIMARY_BLUE if default_value == "light" else WHITE
                light_text_color = WHITE if default_value == "light" else GRAY_700
                light_canvas.create_rectangle(2, 2, 78, 28, fill=light_bg, outline=GRAY_300, width=1, tags="light_bg")
                light_canvas.create_text(40, 15, text="Light", fill=light_text_color, font=("Arial", 10, "bold"))
                
                # Dark theme button
                dark_canvas.delete("all")
                dark_bg = PRIMARY_BLUE if default_value == "dark" else WHITE
                dark_text_color = WHITE if default_value == "dark" else GRAY_700
                dark_canvas.create_rectangle(2, 2, 78, 28, fill=dark_bg, outline=GRAY_300, width=1, tags="dark_bg")
                dark_canvas.create_text(40, 15, text="Dark", fill=dark_text_color, font=("Arial", 10, "bold"))
            
            draw_theme_buttons()
            
            def select_light_theme():
                nonlocal default_value
                default_value = "light"
                var.set("light")
                draw_theme_buttons()
                self.apply_theme("light")
                self.on_setting_changed(setting_key, "light")
            
            def select_dark_theme():
                nonlocal default_value
                default_value = "dark"
                var.set("dark")
                draw_theme_buttons()
                self.apply_theme("dark")
                self.on_setting_changed(setting_key, "dark")
            
            light_canvas.bind("<Button-1>", lambda e: select_light_theme())
            dark_canvas.bind("<Button-1>", lambda e: select_dark_theme())
            
        elif setting_type == "checkbox":
            var = tk.BooleanVar(value=default_value)
            
            # Create custom checkbox using Canvas for consistency
            checkbox_frame = tk.Frame(content_frame, bg=GRAY_100)
            checkbox_frame.pack(anchor="w")
            
            checkbox_canvas = tk.Canvas(
                checkbox_frame,
                width=20,
                height=20,
                bg=GRAY_100,
                highlightthickness=0,
                cursor="hand2"
            )
            checkbox_canvas.pack(side=tk.LEFT, padx=(0, 10))
            
            # Draw checkbox background
            checkbox_canvas.create_rectangle(
                2, 2, 18, 18,
                outline=GRAY_700,
                fill=WHITE,
                width=2,
                tags="checkbox_bg"
            )
            
            # Add checkmark if default is True
            if default_value:
                checkbox_canvas.create_line(6, 10, 9, 13, fill=SUCCESS, width=3, tags="checkmark")
                checkbox_canvas.create_line(9, 13, 14, 8, fill=SUCCESS, width=3, tags="checkmark")
                checkbox_canvas.itemconfig("checkbox_bg", fill=GRAY_200)
            
            # Status label
            status_label = tk.Label(
                checkbox_frame,
                text="Enabled" if default_value else "Disabled",
                bg=GRAY_100,
                fg=SUCCESS if default_value else GRAY_600,
                font=("Arial", 10, "bold"),
                cursor="hand2"
            )
            status_label.pack(side=tk.LEFT)
            
            # Toggle functionality
            def toggle_checkbox():
                current_value = var.get()
                var.set(not current_value)
                new_value = var.get()
                
                checkbox_canvas.delete("checkmark")
                if new_value:
                    checkbox_canvas.create_line(6, 10, 9, 13, fill=SUCCESS, width=3, tags="checkmark")
                    checkbox_canvas.create_line(9, 13, 14, 8, fill=SUCCESS, width=3, tags="checkmark")
                    checkbox_canvas.itemconfig("checkbox_bg", fill=GRAY_200)
                    status_label.config(text="Enabled", fg=SUCCESS)
                else:
                    checkbox_canvas.itemconfig("checkbox_bg", fill=WHITE)
                    status_label.config(text="Disabled", fg=GRAY_600)
                
                # Trigger change tracking
                self.on_setting_changed(setting_key, new_value)
            
            checkbox_canvas.bind("<Button-1>", lambda e: toggle_checkbox())
            status_label.bind("<Button-1>", lambda e: toggle_checkbox())
        
        # Store the variable and original value
        if var:
            self.setting_vars[setting_key] = var
            self.original_values[setting_key] = default_value
        
        # Draw background after everything is set up
        canvas.after(10, draw_setting_bg)
    
    def create_bottom_bar(self):
        """Create the bottom bar with save and close buttons"""
        bottom_bar = tk.Frame(self.root, bg=WHITE)
        bottom_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=10)
        
        # Cancel/Close button
        self.create_rounded_button(
            bottom_bar,
            "Cancel",
            self.on_cancel_click,
            bg_color=GRAY_200,
            text_color=GRAY_700,
            side="right",
            padx=(10, 0)
        )
        
        # Save button (initially disabled)
        self.save_button = self.create_rounded_button(
            bottom_bar,
            "Save Changes",
            self.save_settings,
            bg_color=SUCCESS,
            text_color=WHITE,
            side="right"
        )

    
    def create_rounded_button(self, parent, text, command, bg_color=BUTTON_PRIMARY, text_color=WHITE, side="left", padx=(0, 0)):
        """Create a rounded button with hover effects"""
        button_frame = tk.Frame(parent, bg=WHITE)
        button_frame.pack(side=side, padx=padx)

        canvas = tk.Canvas(
            button_frame,
            width=140,  # Slightly wider for admin buttons
            height=40,
            bg=WHITE,
            highlightthickness=0
        )
        canvas.pack()

        def draw_rounded_rect(fill_color=bg_color):
            canvas.delete("button_bg")
            radius = 15
            x1, y1, x2, y2 = 2, 2, 138, 38

            canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                            start=90, extent=90, fill=fill_color, outline=fill_color, tags="button_bg")
            canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                            start=0, extent=90, fill=fill_color, outline=fill_color, tags="button_bg")
            canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                            start=180, extent=90, fill=fill_color, outline=fill_color, tags="button_bg")
            canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                            start=270, extent=90, fill=fill_color, outline=fill_color, tags="button_bg")

            canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                  fill=fill_color, outline=fill_color, tags="button_bg")
            canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                                  fill=fill_color, outline=fill_color, tags="button_bg")

        draw_rounded_rect()

        text_id = canvas.create_text(
            70, 20,  # Centered in wider button
            text=text,
            fill=text_color,
            font=("Arial", 11, "bold"),
            tags="button_text"
        )

        def on_enter(event):
            hover_color = self.darken_color(bg_color)
            draw_rounded_rect(hover_color)
            canvas.tag_raise("button_text")
            canvas.itemconfig("button_text", fill=text_color)
        
        def on_leave(event):
            draw_rounded_rect(bg_color)
            canvas.tag_raise("button_text")
            canvas.itemconfig("button_text", fill=text_color)

        canvas.bind("<Button-1>", lambda e: command())
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.configure(cursor="hand2")

        return canvas
    
    def darken_color(self, hex_color):
        """Darken a hex color by reducing RGB values"""
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return "#2d3748"
    
    def show_placeholder(self, function_name):
        """Show placeholder message for admin functions"""
        messagebox.showinfo(
            "Admin Function", 
            f"{function_name} functionality is currently under development.\n\nThis will be implemented in a future update."
        )
    
    def close_window(self):
        """Close the admin window"""
        # Unregister from theme manager
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from Config.theme_manager import theme_manager
            if hasattr(self, 'theme_callback'):
                theme_manager.unregister_callback(self.theme_callback)
        except:
            pass
            
        if self.parent:
            self.root.destroy()
        else:
            self.root.quit()
    
    def show(self):
        """Show the admin window"""
        self.register_for_theme_changes()
        self.root.mainloop()
    
    def apply_theme(self, theme):
        """Apply the selected theme to the AdminWindow and propagate to the entire system"""
        # Import theme manager and colors
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from Config.theme_manager import theme_manager
        from Config.colors import get_theme_colors
        
        # Set the theme globally
        theme_manager.set_theme(theme)
        
        # Get theme colors
        colors = get_theme_colors(theme)
        
        # Update AdminWindow colors
        self.root.configure(bg=colors['BG_PRIMARY'])
        
        # Update top bar
        if hasattr(self, 'top_bar'):
            self.top_bar.configure(bg=colors['ONXY'])
        
        # Update main content areas
        if hasattr(self, 'settings_content_frame'):
            self.settings_content_frame.configure(bg=colors['WHITE'])
        
        print(f"Theme applied: {theme}")
    
    def register_for_theme_changes(self):
        """Register this window for theme change notifications"""
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from Config.theme_manager import theme_manager
        
        def on_theme_change(new_theme):
            """Callback when theme changes"""
            try:
                from Config.colors import get_theme_colors
                colors = get_theme_colors(new_theme)
                
                # Update this window's colors
                self.root.configure(bg=colors['BG_PRIMARY'])
                
                if hasattr(self, 'top_bar'):
                    self.top_bar.configure(bg=colors['ONXY'])
                
                if hasattr(self, 'settings_content_frame'):
                    self.settings_content_frame.configure(bg=colors['WHITE'])
                    
            except Exception as e:
                print(f"Error updating AdminWindow theme: {e}")
        
        # Store the callback for later unregistration
        self.theme_callback = on_theme_change
        theme_manager.register_callback(on_theme_change)
    
    def set_save_button_state(self, enabled):
        """Enable or disable the save button"""
        if hasattr(self, 'save_button'):
            # Enable button - make it fully opaque
            self.save_button.configure(state='normal')
            # Redraw with full color
            self.save_button.delete("button_bg")
            self.draw_save_button_bg(self.save_button, SUCCESS, 1.0)
    
    def draw_save_button_bg(self, canvas, fill_color, opacity=1.0):
        """Draw the save button background with optional opacity"""
        radius = 15
        x1, y1, x2, y2 = 2, 2, 138, 38

        canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                        start=90, extent=90, fill=fill_color, outline=fill_color, tags="button_bg")
        canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                        start=0, extent=90, fill=fill_color, outline=fill_color, tags="button_bg")
        canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                        start=180, extent=90, fill=fill_color, outline=fill_color, tags="button_bg")
        canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                        start=270, extent=90, fill=fill_color, outline=fill_color, tags="button_bg")
        canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                              fill=fill_color, outline=fill_color, tags="button_bg")
        canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                              fill=fill_color, outline=fill_color, tags="button_bg")
    
    def apply_current_theme(self):
        """Apply the current theme to the AdminWindow"""
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from Config.theme_manager import theme_manager
            from Config.colors import get_theme_colors
            
            current_theme = theme_manager.get_current_theme()
            colors = get_theme_colors(current_theme)
            
            # Update AdminWindow colors
            self.root.configure(bg=colors['BG_PRIMARY'])
                
        except Exception as e:
            print(f"Error applying current theme to AdminWindow: {e}")
    
    def on_setting_changed(self, setting_key, new_value):
       return
    
    def save_settings(self):
        """Save all settings changes"""
        try:
            # Here you would implement actual saving logic
            # For now, just update the original values and reset the state
            for key, var in self.setting_vars.items():
                current_val = var.get() if hasattr(var, 'get') else var
                self.original_values[key] = current_val
            
            self.has_unsaved_changes = False
            self.set_save_button_state(False)
            
            messagebox.showinfo("Settings Saved", "All settings have been saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save settings: {str(e)}")
    
    def on_cancel_click(self):
        """Handle cancel button click"""
        if self.has_unsaved_changes:
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them before closing?",
                icon="warning"
            )
            if result is True:  # Yes - save and close
                self.save_settings()
                self.close_window()
            elif result is False:  # No - close without saving
                self.close_window()
            # None/Cancel - do nothing, stay open
        else:
            self.close_window()
    
    def on_window_close(self):
        """Handle window close event (X button)"""
        self.on_cancel_click()  # Same logic as cancel button

if __name__ == "__main__":
    # Test the admin window
    admin = AdminWindow(current_ds="Test DS")
    admin.show()
