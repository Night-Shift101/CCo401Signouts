import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.colors import BG_PRIMARY, LIGHT_GRAY, PRIMARY_BLUE, WHITE, GRAY_100, GRAY_200, GRAY_500, GRAY_600, GRAY_700, ONXY, BUTTON_PRIMARY, BUTTON_PRIMARY_HOVER, ERROR, SUCCESS
from Functions.data_manager import DataManager
from Functions.data_utils import DataUtils
from Security.pin_auth_dialog import PinAuthDialog

from newEntry import NewEntryWindow

class HomeWindow:
    def __init__(self, title="Solider Sign-in System"):
        self.root = tk.Tk()
        self.root.title(title)

        self.data_manager = DataManager()

        self.root.configure(bg=BG_PRIMARY)

        self.selected_row_idx = None
        self.row_frames = []  # Store all row frames for selection management
        self.row_data_list = []  # Store row data for selected row access

        self.current_ds = None  # Will be set during startup authentication
        
        self.root.state('zoomed')
        
        try:
            self.root.state('zoomed')
        except:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.create_top_bar()

        self.create_main_content()

        self.create_status_bar()

        self.setup_keyboard_bindings()

        self.startup_authentication()
    
    def create_top_bar(self):

        self.top_bar = tk.Frame(self.root, bg=ONXY, height=100)
        self.top_bar.pack(fill=tk.X, side=tk.TOP)
        self.top_bar.pack_propagate(False)  # Maintain fixed height

        try:

            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Assets", "CcoLogo.png")

            logo_image = Image.open(logo_path)

            logo_image = logo_image.resize((75, 75), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)

            self.logo_label = tk.Label(
                self.top_bar, 
                image=self.logo_photo, 
                bg=ONXY
            )
            self.logo_label.place(x=15, y=12)  # Position at left side, centered vertically
            
        except Exception as e:

            fallback_label = tk.Label(
                self.top_bar, 
                text="LOGO", 
                bg=ONXY, 
                fg=WHITE,
                font=("Arial", 12, "bold")
            )
            fallback_label.place(x=15, y=35)  # Position at left side, centered vertically
            print(f"Could not load logo: {e}")

        title_frame = tk.Frame(self.top_bar, bg=ONXY)
        title_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

        company_label = tk.Label(
            title_frame,
            text="Charlie Company, 401st Cyber Battalion",
            bg=ONXY,
            fg=WHITE,
            font=("Arial", 14)
        )
        company_label.pack()

        system_label = tk.Label(
            title_frame,
            text="SOLDIER SIGN-OUT SYSTEM",
            bg=ONXY,
            fg=WHITE,
            font=("Arial", 26, "bold")
        )
        system_label.pack()

        try:

            ccoe_logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Assets", "CcoeLogo.png")

            ccoe_logo_image = Image.open(ccoe_logo_path)

            ccoe_logo_image = ccoe_logo_image.resize((75, 75), Image.Resampling.LANCZOS)
            self.ccoe_logo_photo = ImageTk.PhotoImage(ccoe_logo_image)

            self.ccoe_logo_label = tk.Label(
                self.top_bar, 
                image=self.ccoe_logo_photo, 
                bg=ONXY
            )
            self.ccoe_logo_label.place(relx=1.0, x=-90, y=12, anchor='nw')  # Position at right side, centered vertically
            
        except Exception as e:

            ccoe_fallback_label = tk.Label(
                self.top_bar, 
                text="CCOE", 
                bg=ONXY, 
                fg=WHITE,
                font=("Arial", 12, "bold")
            )
            ccoe_fallback_label.place(relx=1.0, x=-75, y=35, anchor='nw')  # Position at right side, centered vertically
            print(f"Could not load CCOE logo: {e}")

    def create_main_content(self):

        self.main_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_section = tk.Frame(self.main_frame, bg=GRAY_100, width=350)
        self.left_section.pack(side=tk.LEFT, fill=tk.Y)
        self.left_section.pack_propagate(False)  # Maintain fixed width

        self.right_section = tk.Frame(self.main_frame, bg=WHITE)
        self.right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_left_buttons()

        self.create_spreadsheet_table()
        
    def create_spreadsheet_table(self):

        table_frame = tk.Frame(self.right_section, bg=WHITE)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        header_frame = tk.Frame(table_frame, bg=GRAY_600, height=50)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        columns = [
            ("ID", 0.05),               # 5% - Reduced from 8%
            ("Soldiers", 0.40),         # 40% - Increased from 35% for more chip space
            ("Destination", 0.20),      # 20% - Increased from 18%
            ("Phone Number", 0.15),     # 15% - Increased from 13%
            ("Sign-Out Time & Date", 0.20) # 20% - Increased from 15%
        ]

        for i, (header, width_ratio) in enumerate(columns):
            header_label = tk.Label(
                header_frame,
                text=header,
                bg=GRAY_600,
                fg=WHITE,
                font=("Arial", 12, "bold"),
                relief="flat",
                bd=0,
                anchor="w",
                padx=10
            )
            header_label.place(relx=sum(col[1] for col in columns[:i]), rely=0, 
                              relwidth=width_ratio, relheight=1)

        self.create_scrollable_data_area(table_frame, columns)
        
    def create_scrollable_data_area(self, parent, columns):

        canvas = tk.Canvas(parent, bg=WHITE, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=WHITE)

        canvas.configure(yscrollcommand=v_scrollbar.set)

        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        v_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_mousewheel(event):
            
            try:

                import platform
                system = platform.system()
                
                if system == "Darwin":  # macOS

                    if hasattr(event, 'delta') and event.delta != 0:

                        if event.delta > 0:
                            canvas.yview_scroll(-1, "units")  # Scroll up slowly
                        else:
                            canvas.yview_scroll(1, "units")   # Scroll down slowly
                    else:
                        canvas.yview_scroll(1, "units")
                elif system == "Windows":  # Windows

                    if hasattr(event, 'delta') and event.delta != 0:

                        delta = -1 if event.delta > 0 else 1
                    else:
                        delta = 1
                    canvas.yview_scroll(int(delta), "units")
                else:  # Linux and others

                    if hasattr(event, 'delta') and event.delta != 0:
                        delta = -1 if event.delta > 0 else 1
                    elif hasattr(event, 'num'):
                        delta = -1 if event.num == 4 else 1
                    else:
                        delta = 1
                    canvas.yview_scroll(int(delta), "units")
                
                return "break"
            except Exception as e:

                canvas.yview_scroll(1, "units")
                return "break"
        
        def _on_mousewheel_mac_specific(event):

            if hasattr(event, 'delta'):

                if event.delta > 0:
                    canvas.yview_scroll(-1, "units")  # Scroll up slowly
                else:
                    canvas.yview_scroll(1, "units")   # Scroll down slowly
            else:
                canvas.yview_scroll(1, "units")
            return "break"
        
        def _on_mousewheel_linux_up(event):
            
            canvas.yview_scroll(-1, "units")
            return "break"
        
        def _on_mousewheel_linux_down(event):
            
            canvas.yview_scroll(1, "units")
            return "break"

        import platform
        system = platform.system()
        
        if system == "Darwin":  # macOS

            canvas.bind("<MouseWheel>", _on_mousewheel_mac_specific)

            canvas.bind("<Button-4>", _on_mousewheel_linux_up)
            canvas.bind("<Button-5>", _on_mousewheel_linux_down)
        elif system == "Windows":  # Windows
            canvas.bind("<MouseWheel>", _on_mousewheel)
        else:  # Linux and others
            canvas.bind("<MouseWheel>", _on_mousewheel)
            canvas.bind("<Button-4>", _on_mousewheel_linux_up)
            canvas.bind("<Button-5>", _on_mousewheel_linux_down)

        def _bind_mousewheel(event):
            canvas.focus_set()

            if system == "Darwin":  # macOS
                self.root.bind_all("<MouseWheel>", _on_mousewheel_mac_specific)
                self.root.bind_all("<Button-4>", _on_mousewheel_linux_up)
                self.root.bind_all("<Button-5>", _on_mousewheel_linux_down)
            elif system == "Windows":  # Windows
                self.root.bind_all("<MouseWheel>", _on_mousewheel)
            else:  # Linux and others
                self.root.bind_all("<MouseWheel>", _on_mousewheel)
                self.root.bind_all("<Button-4>", _on_mousewheel_linux_up)
                self.root.bind_all("<Button-5>", _on_mousewheel_linux_down)
        
        def _unbind_mousewheel(event):

            self.root.unbind_all("<MouseWheel>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        scrollable_frame.bind("<Enter>", _bind_mousewheel)
        scrollable_frame.bind("<Leave>", _unbind_mousewheel)

        current_signouts = self.data_manager.get_current_signouts()

        sample_data = []
        for entry in current_signouts:
            display_data = DataUtils.convert_storage_to_display(entry)
            sample_data.append(display_data)

        self.row_frames = []  # Reset row frames list
        self.row_data_list = []  # Reset row data list
        
        for row_idx, row_data in enumerate(sample_data):

            self.row_data_list.append(row_data)

            if row_idx % 2 == 0:
                row_bg = WHITE
            else:
                row_bg = "#f8f9fa"  # Very light gray

            soldiers_data = row_data[1]  # Soldiers array is at index 1
            if isinstance(soldiers_data, list):

                num_soldiers = len(soldiers_data)
                chips_per_row = 3  # Updated to match the chip layout
                num_rows = (num_soldiers + chips_per_row - 1) // chips_per_row  # Ceiling division

                max_chip_rows = 2
                num_rows = min(num_rows, max_chip_rows)
                row_height = max(45, 25 + (num_rows * 25))  # Base height + chip rows
            else:
                row_height = 45  # Standard height for no-array data
            
            row_frame = tk.Frame(scrollable_frame, bg=row_bg, height=row_height, cursor="hand2")
            row_frame.pack(fill=tk.X)
            row_frame.pack_propagate(False)

            self.row_frames.append(row_frame)

            def create_row_click_handler(idx):
                def on_row_click(event):
                    self.select_row(idx)
                return on_row_click
            
            row_click_handler = create_row_click_handler(row_idx)
            row_frame.bind("<Button-1>", row_click_handler)
            
            for col_idx, (col_data, (header, width_ratio)) in enumerate(zip(row_data, columns)):

                text_color = "#2d3748"  # Dark gray for normal text
                font_weight = "normal"
                
                if col_idx == 0:  # ID column
                    font_weight = "bold"
                    text_color = PRIMARY_BLUE
                elif col_idx == 1:  # Soldiers column (array of soldiers displayed as chips)

                    if isinstance(col_data, list):
                        self.create_soldiers_chips(row_frame, col_data, columns, col_idx, row_bg, row_idx)
                        continue  # Skip the normal label creation for this column
                    else:

                        font_weight = "bold"
                        text_color = "#2d3748"
                elif col_idx == 2:  # Destination column
                    text_color = "#4a5568"  # Slightly lighter gray
                elif col_idx == 3:  # Phone Number column
                    text_color = "#718096"  # Light gray
                elif col_idx == 4:  # Sign-Out Time & Date column
                    font_weight = "bold"
                    text_color = "#e53e3e"  # Red to draw attention to time

                cell_label = tk.Label(
                    row_frame,
                    text=str(col_data),
                    bg=row_bg,
                    fg=text_color,
                    font=("Arial", 11, font_weight),
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=10,
                    pady=5,
                    cursor="hand2"
                )
                cell_label.place(relx=sum(col[1] for col in columns[:col_idx]), rely=0, 
                                relwidth=width_ratio, relheight=1)

                cell_label.bind("<Button-1>", row_click_handler)

                def on_enter(event, label=cell_label, original_bg=row_bg, r_idx=row_idx):

                    if self.selected_row_idx != r_idx:
                        if original_bg == WHITE:
                            label.configure(bg="#e2e8f0")  # Light blue-gray on hover
                        else:
                            label.configure(bg="#e2e8f0")
                
                def on_leave(event, label=cell_label, original_bg=row_bg, r_idx=row_idx):

                    if self.selected_row_idx != r_idx:
                        label.configure(bg=original_bg)
                    elif self.selected_row_idx == r_idx:
                        label.configure(bg="#dbeafe")  # Keep selection color
                
                cell_label.bind("<Enter>", on_enter)
                cell_label.bind("<Leave>", on_leave)

                if system == "Darwin":  # macOS
                    cell_label.bind("<MouseWheel>", _on_mousewheel_mac_specific)
                else:
                    cell_label.bind("<MouseWheel>", _on_mousewheel)
                cell_label.bind("<Button-4>", _on_mousewheel_linux_up)
                cell_label.bind("<Button-5>", _on_mousewheel_linux_down)

            if system == "Darwin":  # macOS
                row_frame.bind("<MouseWheel>", _on_mousewheel_mac_specific)
            else:
                row_frame.bind("<MouseWheel>", _on_mousewheel)
            row_frame.bind("<Button-4>", _on_mousewheel_linux_up)
            row_frame.bind("<Button-5>", _on_mousewheel_linux_down)

        def update_scroll_region():
            scrollable_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_window(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
            update_scroll_region()
        
        canvas.bind('<Configure>', configure_canvas_window)
        scrollable_frame.after(100, update_scroll_region)  # Initial update
    
    def create_soldiers_chips(self, parent_frame, soldiers_array, columns, col_idx, row_bg, row_idx=None):

        soldiers_frame = tk.Frame(parent_frame, bg=row_bg, cursor="hand2")
        width_ratio = columns[col_idx][1]  # Get width ratio for soldiers column
        soldiers_frame.place(relx=sum(col[1] for col in columns[:col_idx]), rely=0, 
                           relwidth=width_ratio, relheight=1)

        if row_idx is not None:
            def on_soldiers_frame_click(event):
                self.select_row(row_idx)
            soldiers_frame.bind("<Button-1>", on_soldiers_frame_click)

        chips_container = tk.Frame(soldiers_frame, bg=row_bg, cursor="hand2")
        chips_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        if row_idx is not None:
            chips_container.bind("<Button-1>", on_soldiers_frame_click)

        current_row = 0
        current_col = 0
        chips_per_row = 3  # Increased from 2 since we have more space now

        chip_bg = GRAY_100  # Light gray to match left sidebar
        chip_hover_bg = GRAY_200  # Slightly darker gray for hover
        chip_fg = GRAY_700  # Dark text for better contrast on light background

        def draw_rounded_chip(canvas, bg_color):
            canvas.delete("chip_bg")
            x1, y1, x2, y2 = 1, 1, 104, 17
            radius = 9  # Rounded corner radius

            canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                            start=90, extent=90, fill=bg_color, outline=bg_color, tags="chip_bg")
            canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                            start=0, extent=90, fill=bg_color, outline=bg_color, tags="chip_bg")
            canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                            start=180, extent=90, fill=bg_color, outline=bg_color, tags="chip_bg")
            canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                            start=270, extent=90, fill=bg_color, outline=bg_color, tags="chip_bg")

            canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                  fill=bg_color, outline=bg_color, tags="chip_bg")
            canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                                  fill=bg_color, outline=bg_color, tags="chip_bg")

        for i, soldier_name in enumerate(soldiers_array):

            chip_x = 5 + (current_col * 110)  # 110px per chip with spacing
            chip_y = 2 + (current_row * 22)   # 22px per row with spacing

            chip_canvas = tk.Canvas(
                chips_container,
                width=105,
                height=18,
                bg=row_bg,
                highlightthickness=0
            )
            chip_canvas.place(x=chip_x, y=chip_y)

            draw_rounded_chip(chip_canvas, chip_bg)

            text_id = chip_canvas.create_text(
                52, 9,  # Center of the chip
                text=soldier_name,
                fill=chip_fg,
                font=("Arial", 9, "bold"),
                tags="chip_text"
            )

            def create_hover_handlers(canvas, text_content, r_idx):
                def on_chip_enter(event):
                    draw_rounded_chip(canvas, chip_hover_bg)

                    canvas.delete("chip_text")
                    canvas.create_text(
                        52, 9,
                        text=text_content,
                        fill=GRAY_700,
                        font=("Arial", 9, "bold"),
                        tags="chip_text"
                    )
                
                def on_chip_leave(event):
                    draw_rounded_chip(canvas, chip_bg)

                    canvas.delete("chip_text")
                    canvas.create_text(
                        52, 9,
                        text=text_content,
                        fill=chip_fg,
                        font=("Arial", 9, "bold"),
                        tags="chip_text"
                    )
                
                def on_chip_click(event):

                    if r_idx is not None:
                        self.select_row(r_idx)
                    print(f"Clicked on soldier: {text_content} (Row {r_idx})")
                
                return on_chip_enter, on_chip_leave, on_chip_click
            
            enter_handler, leave_handler, click_handler = create_hover_handlers(chip_canvas, soldier_name, row_idx)
            chip_canvas.bind("<Enter>", enter_handler)
            chip_canvas.bind("<Leave>", leave_handler)
            chip_canvas.bind("<Button-1>", click_handler)

            current_col += 1
            if current_col >= chips_per_row:
                current_col = 0
                current_row += 1
    
    def darken_color(self, hex_color):

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
            return "#2d3748"  # Default dark color if parsing fails
        
    def create_left_buttons(self):

        top_spacer = tk.Frame(self.left_section, bg=GRAY_100, height=40)
        top_spacer.pack(fill=tk.X)

        self.btn_new_entry = self.create_rounded_button(
            self.left_section, 
            "NEW ENTRY", 
            lambda: self.on_button_click("NEW ENTRY"),
            button_color=SUCCESS
        )

        self.btn_edit = self.create_rounded_button(
            self.left_section, 
            "EDIT", 
            lambda: self.on_button_click("EDIT"),
            enabled=False
        )

        self.btn_sign_in = self.create_rounded_button(
            self.left_section, 
            "SIGN-IN", 
            lambda: self.on_button_click("SIGN-IN"),
            enabled=False
        )

        bottom_spacer = tk.Frame(self.left_section, bg=GRAY_100)
        bottom_spacer.pack(fill=tk.BOTH, expand=True)

        self.btn_admin = self.create_rounded_button(
            self.left_section, 
            "ADMIN", 
            lambda: self.on_button_click("ADMIN"),
            button_color=ERROR,
            is_small=True
        )
        
    def create_rounded_button(self, parent, text, command, button_color=BUTTON_PRIMARY, is_small=False, enabled=True):

        button_height = 40 if is_small else 60
        button_pady = 10 if is_small else 15
        button_padx = 50 if is_small else 30
        font_size = 14 if is_small else 16

        button_frame = tk.Frame(parent, bg=GRAY_100, height=button_height)
        button_frame.pack(fill=tk.X, padx=button_padx, pady=button_pady)
        button_frame.pack_propagate(False)

        canvas = tk.Canvas(
            button_frame, 
            height=button_height, 
            bg=GRAY_100, 
            highlightthickness=0
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        canvas.button_enabled = enabled
        canvas.button_color = button_color
        canvas.button_command = command
        canvas.button_text = text
        canvas.font_size = font_size

        def draw_rounded_rect(canvas, x1, y1, x2, y2, radius=15, fill_color=None):
            if fill_color is None:
                fill_color = button_color if canvas.button_enabled else GRAY_200

            canvas.delete("button_bg")

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

        def update_button_appearance():
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            button_y_center = button_height // 2
            button_bottom = button_height - 2
            
            if canvas_width > 1:  # Make sure canvas is rendered
                draw_rounded_rect(canvas, 2, 2, canvas_width-2, button_bottom)
            else:
                canvas.after(10, lambda: draw_rounded_rect(canvas, 2, 2, canvas.winfo_width()-2, button_bottom))

            text_color = WHITE if canvas.button_enabled else GRAY_500
            cursor_type = "hand2" if canvas.button_enabled else "arrow"

            canvas.delete("button_text")
            text_id = canvas.create_text(
                canvas_width//2 if canvas_width > 1 else 0, button_y_center, 
                text=canvas.button_text, 
                fill=text_color, 
                font=("Arial", canvas.font_size, "bold"),
                tags="button_text"
            )

            canvas.configure(cursor=cursor_type)
            
            return text_id

        text_id = update_button_appearance()

        def set_button_enabled(enabled):
            canvas.button_enabled = enabled
            update_button_appearance()

        canvas.set_enabled = set_button_enabled

        def on_click(event):
            if canvas.button_enabled:
                canvas.button_command()

        def on_enter(event):
            if canvas.button_enabled:
                hover_color = self.darken_color(canvas.button_color)
                canvas.update_idletasks()
                canvas_width = canvas.winfo_width()
                button_bottom = button_height - 2
                if canvas_width > 1:
                    draw_rounded_rect(canvas, 2, 2, canvas_width-2, button_bottom, fill_color=hover_color)

                canvas.delete("button_text")
                canvas.create_text(
                    canvas_width//2, button_height // 2,
                    text=canvas.button_text,
                    fill=WHITE,
                    font=("Arial", canvas.font_size, "bold"),
                    tags="button_text"
                )
        
        def on_leave(event):
            if canvas.button_enabled:
                update_button_appearance()

        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        
        return canvas

    def startup_authentication(self):
        
        while True:  # Keep trying until successful authentication or user closes app
            try:

                auth_dialog = PinAuthDialog(self.root, "access the Soldier Sign-in System")
                authenticated, ds_name = auth_dialog.show_and_wait()
                
                if authenticated:
                    self.current_ds = ds_name
                    print(f"Startup authentication successful. Current DS: {ds_name}")

                    self.root.title(f"Soldier Sign-in System - {ds_name}")
                    break
                else:

                    result = messagebox.askyesno(
                        "Authentication Required", 
                        "Authentication is required to use this system.\n\nWould you like to try again?",
                        icon="warning"
                    )
                    if not result:

                        print("User cancelled startup authentication. Exiting application.")
                        self.root.destroy()
                        sys.exit(0)
                        
            except Exception as e:
                print(f"Error during startup authentication: {e}")
                messagebox.showerror("Authentication Error", f"An error occurred during authentication: {str(e)}")

                result = messagebox.askyesno(
                    "Error", 
                    "An error occurred during authentication.\n\nWould you like to try again?",
                    icon="error"
                )
                if not result:
                    self.root.destroy()
                    sys.exit(0)

    def authenticate_ds_action(self, action_description):
        
        try:

            auth_dialog = PinAuthDialog(self.root, action_description, default_ds=self.current_ds)
            authenticated, ds_name = auth_dialog.show_and_wait()
            
            if authenticated:

                if ds_name != self.current_ds:
                    self.current_ds = ds_name

                    self.root.title(f"Soldier Sign-in System - {ds_name}")
                    print(f"Current DS changed to: {ds_name}")
                
                print(f"DS {ds_name} authenticated for action: {action_description}")
                return True
            else:
                print(f"Authentication failed or cancelled for action: {action_description}")
                return False
                
        except Exception as e:
            print(f"Error during authentication: {e}")
            messagebox.showerror("Authentication Error", f"An error occurred during authentication: {str(e)}")
            return False

    def on_button_click(self, button_name):
        
        print(f"{button_name} button clicked!")
        
        if button_name == "NEW ENTRY":

            new_entry_window = NewEntryWindow(
                parent=self.root, 
                data_manager=self.data_manager,
                on_close_callback=self.refresh_table_data
            )
        elif button_name == "EDIT":

            selected_data = self.get_selected_row_data()
            if selected_data:

                if self.authenticate_ds_action("edit a sign-out entry"):
                    print(f"Edit functionality for row: {selected_data[0]} - {selected_data[1]}")

                    edit_window = NewEntryWindow(
                        parent=self.root,
                        data_manager=self.data_manager,
                        on_close_callback=self.refresh_table_data,
                        edit_data=selected_data
                    )
            else:
                messagebox.showwarning("No Selection", "Please select a row to edit")
        elif button_name == "SIGN-IN":

            selected_data = self.get_selected_row_data()
            if selected_data:

                if self.authenticate_ds_action("sign in a soldier"):
                    self.sign_in_selected_entry()
            else:
                messagebox.showwarning("No Selection", "Please select a row to sign in")
        elif button_name == "ADMIN":

            print("Admin functionality not yet implemented")
    
    def sign_in_selected_entry(self):
        
        if self.selected_row_idx is not None and self.selected_row_idx < len(self.row_data_list):
            selected_data = self.row_data_list[self.selected_row_idx]
            entry_id = selected_data[0]  # ID is the first element

            soldiers_text = DataUtils.format_soldiers_for_display(selected_data[1])
            result = messagebox.askyesno(
                "Confirm Sign-In", 
                f"Sign in the following entry?\n\nID: {entry_id}\nSoldiers: {soldiers_text}\nDestination: {selected_data[2]}"
            )
            
            if result:
                try:

                    success = self.data_manager.remove_signout(entry_id)
                    
                    if success:
                        messagebox.showinfo("Success", f"Entry {entry_id} signed in successfully!")

                        self.refresh_table_data()

                        self.clear_selection()
                    else:
                        messagebox.showerror("Error", f"Failed to find entry {entry_id}")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to sign in entry: {str(e)}")
                    print(f"Error signing in entry: {e}")
    
    def refresh_table_data(self):
        
        try:

            self.clear_selection()

            self.right_section.destroy()

            self.right_section = tk.Frame(self.main_frame, bg=WHITE)
            self.right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            self.create_spreadsheet_table()
            print("Table refreshed successfully with current data")
            
        except Exception as e:
            print(f"Error refreshing table: {e}")

            try:
                if hasattr(self, 'right_section') and self.right_section.winfo_exists():
                    self.right_section.destroy()
                self.right_section = tk.Frame(self.main_frame, bg=WHITE)
                self.right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
                self.create_spreadsheet_table()
                print("Table recreated successfully after error")
            except Exception as e2:
                print(f"Failed to recreate table: {e2}")
    
    def select_row(self, row_idx):

        if self.selected_row_idx is not None and self.selected_row_idx < len(self.row_frames):
            self.deselect_current_row()

        self.selected_row_idx = row_idx
        if row_idx < len(self.row_frames):
            row_frame = self.row_frames[row_idx]

            self.update_row_selection_style(row_frame, True)
            self.update_status_bar(row_idx)  # Update status bar with selection info
            self.update_button_states()  # Update button states when selection changes
            print(f"Selected row {row_idx}: {self.row_data_list[row_idx][0]}")  # Print ID for debugging
    
    def deselect_current_row(self):
        
        if self.selected_row_idx is not None and self.selected_row_idx < len(self.row_frames):
            row_frame = self.row_frames[self.selected_row_idx]
            self.update_row_selection_style(row_frame, False)
    
    def update_row_selection_style(self, row_frame, is_selected):
        
        if is_selected:

            new_bg = "#dbeafe"  # Light blue background for selection
            selection_border = "#3b82f6"  # Blue border
            row_frame.configure(bg=new_bg, relief="solid", bd=2, highlightbackground=selection_border)
        else:

            row_idx = self.row_frames.index(row_frame)
            if row_idx % 2 == 0:
                original_bg = WHITE
            else:
                original_bg = "#f8f9fa"
            row_frame.configure(bg=original_bg, relief="flat", bd=0)

        self.update_row_children_style(row_frame, is_selected)
    
    def update_row_children_style(self, row_frame, is_selected):
        
        if is_selected:
            new_bg = "#dbeafe"  # Light blue background for selection
        else:
            row_idx = self.row_frames.index(row_frame)
            if row_idx % 2 == 0:
                new_bg = WHITE
            else:
                new_bg = "#f8f9fa"

        def update_widget_bg(widget):
            try:

                if not isinstance(widget, tk.Canvas):
                    widget.configure(bg=new_bg)
                for child in widget.winfo_children():
                    update_widget_bg(child)
            except tk.TclError:
                pass  # Skip widgets that don't support bg configuration
        
        update_widget_bg(row_frame)
    
    def get_selected_row_data(self):
        
        if self.selected_row_idx is not None and self.selected_row_idx < len(self.row_data_list):
            return self.row_data_list[self.selected_row_idx]
        return None
    
    def clear_selection(self):
        
        if self.selected_row_idx is not None:
            self.deselect_current_row()
            self.selected_row_idx = None
            self.update_status_bar()  # Update status bar to show no selection
            self.update_button_states()  # Update button states when selection is cleared
    
    def update_button_states(self):
        
        has_selection = self.selected_row_idx is not None

        if hasattr(self, 'btn_edit') and hasattr(self.btn_edit, 'set_enabled'):
            self.btn_edit.set_enabled(has_selection)

        if hasattr(self, 'btn_sign_in') and hasattr(self.btn_sign_in, 'set_enabled'):
            self.btn_sign_in.set_enabled(has_selection)

    def on_button_hover(self, button, is_entering):
        
        pass  # Now handled by canvas buttons

    def show(self):
        self.root.mainloop()
    
    def hide(self):
        self.root.withdraw()
    
    def destroy(self):
        self.root.destroy()

    def setup_keyboard_bindings(self):

        self.root.focus_set()

        self.root.bind("<Up>", self.select_previous_row)
        self.root.bind("<Down>", self.select_next_row)

        self.root.bind("<Home>", self.select_first_row)
        self.root.bind("<End>", self.select_last_row)

        self.root.bind("<Escape>", lambda e: self.clear_selection())

        self.root.bind("<Return>", self.on_enter_key)
    
    def select_previous_row(self, event=None):
        
        if self.selected_row_idx is None:
            if self.row_frames:
                self.select_row(0)
        elif self.selected_row_idx > 0:
            self.select_row(self.selected_row_idx - 1)
    
    def select_next_row(self, event=None):
        
        if self.selected_row_idx is None:
            if self.row_frames:
                self.select_row(0)
        elif self.selected_row_idx < len(self.row_frames) - 1:
            self.select_row(self.selected_row_idx + 1)
    
    def select_first_row(self, event=None):
        
        if self.row_frames:
            self.select_row(0)
    
    def select_last_row(self, event=None):
        
        if self.row_frames:
            self.select_row(len(self.row_frames) - 1)
    
    def on_enter_key(self, event=None):
        
        if self.selected_row_idx is not None:
            selected_data = self.get_selected_row_data()
            if selected_data:
                print(f"Enter pressed on row: {selected_data[0]} - {selected_data[1]}")

    def create_status_bar(self):
        
        self.status_bar = tk.Frame(self.root, bg=GRAY_100, height=30)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)

        self.status_label = tk.Label(
            self.status_bar,
            text="No row selected - Click on a row to select it",
            bg=GRAY_100,
            fg=GRAY_600,
            font=("Arial", 10),
            anchor="w",
            padx=20
        )
        self.status_label.pack(fill=tk.X, side=tk.LEFT)

        self.selection_info_label = tk.Label(
            self.status_bar,
            text="Use ↑↓ arrow keys to navigate, Esc to clear selection",
            bg=GRAY_100,
            fg=GRAY_500,
            font=("Arial", 9),
            anchor="e",
            padx=20
        )
        self.selection_info_label.pack(fill=tk.X, side=tk.RIGHT)
    
    def update_status_bar(self, row_idx=None):
        
        if row_idx is not None and row_idx < len(self.row_data_list):
            row_data = self.row_data_list[row_idx]
            soldiers_text = f"{len(row_data[1])} soldier(s)" if isinstance(row_data[1], list) else "1 soldier"
            status_text = f"Selected: Row {row_data[0]} - {soldiers_text} - {row_data[2]}"
            self.status_label.configure(text=status_text, fg=PRIMARY_BLUE)
        else:
            self.status_label.configure(text="No row selected - Click on a row to select it", fg=GRAY_600)

if __name__ == "__main__":

    window = HomeWindow("Solider Sign-Out System")
    window.show()
    window.show()