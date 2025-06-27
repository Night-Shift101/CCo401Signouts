import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime
from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.colors import BG_PRIMARY, LIGHT_GRAY, PRIMARY_BLUE, WHITE, GRAY_100, GRAY_200, GRAY_700, ONXY, BUTTON_PRIMARY, BUTTON_PRIMARY_HOVER, ERROR, SUCCESS
from Functions.data_manager import DataManager
from Functions.data_utils import DataUtils
from Security.pin_auth_dialog import PinAuthDialog

class NewEntryWindow:
    def __init__(self, parent=None, data_manager=None, on_close_callback=None, edit_data=None):
        self.parent = parent
        self.data_manager = data_manager or DataManager()
        self.on_close_callback = on_close_callback
        self.edit_data = edit_data  # Data for editing existing entry
        self.is_editing = edit_data is not None
        
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("Edit Sign-Out Entry" if self.is_editing else "New Sign-Out Entry")

        self.root.configure(bg=BG_PRIMARY)
        self.root.geometry("800x800")  # Increased height to accommodate checkboxes
        self.root.resizable(True, True)

        if parent:
            self.root.transient(parent)
            self.root.grab_set()

        self.center_window()

        self.scanned_soldiers = []

        self.destination_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        self.family_var = tk.BooleanVar()
        self.leave_var = tk.BooleanVar()
        self.phase_v_escort_var = tk.BooleanVar()
        self.off_post_var = tk.BooleanVar()

        self.create_top_bar()

        self.create_form()

        if self.is_editing:
            self.populate_form_with_data()
    
    def center_window(self):
        
        self.root.update_idletasks()
        
        if self.parent:

            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            x = parent_x + (parent_width // 2) - (800 // 2)
            y = parent_y + (parent_height // 2) - (800 // 2)  # Updated for new height
        else:

            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width // 2) - (800 // 2)
            y = (screen_height // 2) - (800 // 2)  # Updated for new height
        
        self.root.geometry(f"800x800+{x}+{y}")  # Updated geometry string
    
    def create_top_bar(self):

        self.top_bar = tk.Frame(self.root, bg=ONXY, height=80)
        self.top_bar.pack(fill=tk.X, side=tk.TOP)
        self.top_bar.pack_propagate(False)  # Maintain fixed height

        try:

            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Assets", "CcoLogo.png")

            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)

            self.logo_label = tk.Label(
                self.top_bar, 
                image=self.logo_photo, 
                bg=ONXY
            )
            self.logo_label.place(x=15, y=10)
            
        except Exception as e:

            fallback_label = tk.Label(
                self.top_bar, 
                text="LOGO", 
                bg=ONXY, 
                fg=WHITE,
                font=("Arial", 12, "bold")
            )
            fallback_label.place(x=15, y=30)
            print(f"Could not load logo: {e}")

        title_frame = tk.Frame(self.top_bar, bg=ONXY)
        title_frame.place(relx=0.5, rely=0.5, anchor='center')

        title_text = "EDIT SIGN-OUT ENTRY" if self.is_editing else "NEW SIGN-OUT ENTRY"
        system_label = tk.Label(
            title_frame,
            text=title_text,
            bg=ONXY,
            fg=WHITE,
            font=("Arial", 22, "bold")
        )
        system_label.pack()

        try:

            ccoe_logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Assets", "CcoeLogo.png")

            ccoe_logo_image = Image.open(ccoe_logo_path)
            ccoe_logo_image = ccoe_logo_image.resize((60, 60), Image.Resampling.LANCZOS)
            self.ccoe_logo_photo = ImageTk.PhotoImage(ccoe_logo_image)

            self.ccoe_logo_label = tk.Label(
                self.top_bar, 
                image=self.ccoe_logo_photo, 
                bg=ONXY
            )
            self.ccoe_logo_label.place(relx=1.0, x=-75, y=10, anchor='nw')
            
        except Exception as e:

            ccoe_fallback_label = tk.Label(
                self.top_bar, 
                text="CCOE", 
                bg=ONXY, 
                fg=WHITE,
                font=("Arial", 12, "bold")
            )
            ccoe_fallback_label.place(relx=1.0, x=-60, y=30, anchor='nw')
            print(f"Could not load CCOE logo: {e}")
    
    def create_form(self):

        main_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        form_frame = tk.Frame(main_frame, bg=WHITE)
        form_frame.pack(fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(form_frame, bg=WHITE)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 0))

        self.create_cac_scanning_area()

        separator = tk.Frame(self.content_frame, bg=GRAY_200, height=1)
        separator.pack(fill=tk.X, pady=(30, 20))

        self.create_form_field(self.content_frame, "Destination:", self.destination_var, "Fort Liberty")

        self.create_form_field(self.content_frame, "Contact Phone Number:", self.phone_var, "(555) 123-4567")

        self.create_checkboxes(self.content_frame)

        self.create_buttons(form_frame)
    
    def create_cac_scanning_area(self):

        cac_label = tk.Label(
            self.content_frame,
            text="CAC Scanning",
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 14, "bold")
        )
        cac_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.cac_frame = tk.Frame(self.content_frame, bg=GRAY_100, height=150, cursor="hand2")
        self.cac_frame.pack(fill=tk.X, padx=20, pady=10)
        self.cac_frame.pack_propagate(False)

        self.cac_instruction_label = tk.Label(
            self.cac_frame,
            text="Click here and scan CACs",
            bg=GRAY_100,
            fg=GRAY_700,
            font=("Arial", 16, "bold"),
            cursor="hand2"
        )
        self.cac_instruction_label.pack(expand=True)

        self.soldiers_display_frame = tk.Frame(self.cac_frame, bg=GRAY_100, cursor="hand2")

        self.cac_frame.bind("<Button-1>", self.simulate_cac_scan)
        self.cac_instruction_label.bind("<Button-1>", self.simulate_cac_scan)

        self.soldiers_display_frame.bind("<Button-1>", self.simulate_cac_scan)

        def on_cac_enter(event):
            if self.cac_instruction_label.winfo_viewable():  # Only if instruction is still visible
                self.cac_frame.configure(bg=GRAY_200)
                self.cac_instruction_label.configure(bg=GRAY_200)
        
        def on_cac_leave(event):
            if self.cac_instruction_label.winfo_viewable():  # Only if instruction is still visible
                self.cac_frame.configure(bg=GRAY_100)
                self.cac_instruction_label.configure(bg=GRAY_100)
        
        self.cac_frame.bind("<Enter>", on_cac_enter)
        self.cac_frame.bind("<Leave>", on_cac_leave)
        self.cac_instruction_label.bind("<Enter>", on_cac_enter)
        self.cac_instruction_label.bind("<Leave>", on_cac_leave)
    
    def simulate_cac_scan(self, event=None):

        if self.cac_instruction_label.winfo_viewable():
            self.cac_instruction_label.pack_forget()

            self.soldiers_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            def on_scan_area_enter(event):
                if self.cac_frame.cget('bg') == 'white':  # Only if background is white (after first scan)
                    self.cac_frame.configure(bg=GRAY_100)
                    self.soldiers_display_frame.configure(bg=GRAY_100)
            
            def on_scan_area_leave(event):
                if self.cac_frame.cget('bg') != 'white':  # Only if background was changed to gray
                    self.cac_frame.configure(bg=WHITE)
                    self.soldiers_display_frame.configure(bg=WHITE)

            self.cac_frame.bind("<Enter>", on_scan_area_enter)
            self.cac_frame.bind("<Leave>", on_scan_area_leave)

            self.cac_frame.configure(bg=WHITE)
            self.soldiers_display_frame.configure(bg=WHITE)

        self.refresh_click_bindings()

        sample_soldiers = [
            "SGT Johnson, M.", "SPC Williams, A.", "PFC Brown, D.", "CPL Davis, R.",
            "SSG Garcia, L.", "PV2 Martinez, C.", "SFC Rodriguez, J.", "PFC Anderson, K.",
            "CPL Thompson, B.", "PFC Wilson, S.", "SPC Adams, T.", "SGT Miller, R."
        ]

        if len(self.scanned_soldiers) < len(sample_soldiers):
            new_soldier = sample_soldiers[len(self.scanned_soldiers)]
            self.scanned_soldiers.append(new_soldier)
            self.update_soldiers_display()
            print(f"Scanned: {new_soldier}")
        else:
            messagebox.showinfo("CAC Scanner", "All sample soldiers have been scanned.\nMaximum capacity reached.")
    
    def refresh_click_bindings(self):

        self.cac_frame.bind("<Button-1>", self.simulate_cac_scan)
        self.soldiers_display_frame.bind("<Button-1>", self.simulate_cac_scan)
    
    def update_soldiers_display(self):

        for widget in self.soldiers_display_frame.winfo_children():
            widget.destroy()
        
        if not self.scanned_soldiers:

            empty_label = tk.Label(
                self.soldiers_display_frame,
                text="Click anywhere to scan more CACs",
                bg=WHITE,
                fg=GRAY_200,
                font=("Arial", 12),
                cursor="hand2"
            )
            empty_label.pack(expand=True)
            empty_label.bind("<Button-1>", self.simulate_cac_scan)
            return

        chips_frame = tk.Frame(self.soldiers_display_frame, bg=WHITE, cursor="hand2")
        chips_frame.pack(fill=tk.X, pady=(10, 0))

        chips_frame.bind("<Button-1>", self.simulate_cac_scan)
        
        current_row = 0
        current_col = 0
        chips_per_row = 3
        
        for i, soldier_name in enumerate(self.scanned_soldiers):

            chip_x = current_col * 190  # Increased spacing to accommodate wider chips
            chip_y = current_row * 35   # Increased vertical spacing
            
            chip_canvas = tk.Canvas(
                chips_frame,
                width=180,  # Increased width to fit X button inside
                height=30,  # Increased height
                bg=WHITE,
                highlightthickness=0,
                cursor="hand2"  # Make sure cursor shows it's clickable
            )
            chip_canvas.place(x=chip_x, y=chip_y)

            def create_chip_click_handler():
                def chip_click_handler(event):

                    if event.x < 150:  # Left side of the chip (not the X button area)
                        self.simulate_cac_scan(event)
                return chip_click_handler
            
            chip_canvas.bind("<Button-1>", create_chip_click_handler())

            self.draw_rounded_chip(chip_canvas, SUCCESS, 180, 30)

            chip_canvas.create_text(
                75, 15,  # Moved left to make room for X button
                text=soldier_name,
                fill=WHITE,
                font=("Arial", 10, "bold"),
                anchor="center"
            )

            x_button = chip_canvas.create_text(
                160, 15,  # Positioned inside the chip on the right
                text="×",
                fill=WHITE,
                font=("Arial", 14, "bold"),
                tags=f"remove_{i}"
            )

            x_button_area = chip_canvas.create_rectangle(
                150, 5, 170, 25,  # Click area around the X
                fill="",
                outline="",
                tags=f"remove_area_{i}"
            )

            def create_remove_handler(idx):
                def remove_handler(event):
                    self.remove_soldier(idx)
                return remove_handler
            
            chip_canvas.tag_bind(f"remove_{i}", "<Button-1>", create_remove_handler(i))
            chip_canvas.tag_bind(f"remove_area_{i}", "<Button-1>", create_remove_handler(i))

            def create_hover_handlers(idx):
                def on_x_enter(event):
                    chip_canvas.itemconfig(f"remove_{idx}", fill="#ff4444")  # Red on hover
                    chip_canvas.configure(cursor="hand2")
                
                def on_x_leave(event):
                    chip_canvas.itemconfig(f"remove_{idx}", fill=WHITE)  # White normally
                    chip_canvas.configure(cursor="")
                
                return on_x_enter, on_x_leave
            
            enter_handler, leave_handler = create_hover_handlers(i)
            chip_canvas.tag_bind(f"remove_{i}", "<Enter>", enter_handler)
            chip_canvas.tag_bind(f"remove_{i}", "<Leave>", leave_handler)
            chip_canvas.tag_bind(f"remove_area_{i}", "<Enter>", enter_handler)
            chip_canvas.tag_bind(f"remove_area_{i}", "<Leave>", leave_handler)

            current_col += 1
            if current_col >= chips_per_row:
                current_col = 0
                current_row += 1

        total_height = (current_row + 1) * 35 + 10  # Adjusted for new chip height
        chips_frame.configure(height=total_height)

        add_more_frame = tk.Frame(self.soldiers_display_frame, bg=WHITE, height=30, cursor="hand2")
        add_more_frame.pack(fill=tk.X, pady=(5, 0))
        add_more_frame.pack_propagate(False)
        
        add_more_label = tk.Label(
            add_more_frame,
            text="+ Click here to scan more CACs",
            bg=WHITE,
            fg=GRAY_200,
            font=("Arial", 10, "italic"),
            cursor="hand2"
        )
        add_more_label.pack(expand=True)

        add_more_frame.bind("<Button-1>", self.simulate_cac_scan)
        add_more_label.bind("<Button-1>", self.simulate_cac_scan)

        self.refresh_click_bindings()
    
    def draw_rounded_chip(self, canvas, color, width, height):
        
        radius = 12
        x1, y1, x2, y2 = 1, 1, width-1, height-1

        canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                        start=90, extent=90, fill=color, outline=color)
        canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                        start=0, extent=90, fill=color, outline=color)
        canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                        start=180, extent=90, fill=color, outline=color)
        canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                        start=270, extent=90, fill=color, outline=color)

        canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                              fill=color, outline=color)
        canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                              fill=color, outline=color)
    
    def remove_soldier(self, index):
        
        if 0 <= index < len(self.scanned_soldiers):
            removed_soldier = self.scanned_soldiers.pop(index)
            self.update_soldiers_display()
            print(f"Removed soldier: {removed_soldier}")
    
    def create_form_field(self, parent, label_text, text_var, placeholder=""):

        label = tk.Label(
            parent,
            text=label_text,
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, 8))

        entry = tk.Entry(
            parent,
            textvariable=text_var,
            font=("Arial", 14),
            bg=GRAY_100,
            fg=GRAY_700,
            relief="flat",
            bd=0,
            insertbackground=GRAY_700
        )
        entry.pack(fill=tk.X, pady=(0, 20), ipady=12)

        if placeholder:
            self.add_placeholder(entry, placeholder)
        
        return entry
    
    def add_placeholder(self, entry, placeholder_text):
        
        entry.insert(0, placeholder_text)
        entry.configure(fg=GRAY_200)
        
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.configure(fg=GRAY_700)
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.configure(fg=GRAY_200)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    
    def create_checkboxes(self, parent):

        self.checkbox_canvases = []

        checkbox_label = tk.Label(
            parent,
            text="Sign-Out Category:",
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        checkbox_label.pack(anchor="w", pady=(20, 8))

        checkbox_frame = tk.Frame(parent, bg=WHITE)
        checkbox_frame.pack(fill=tk.X, pady=(0, 20))

        checkbox_options = [
            ("Family", self.family_var),
            ("Leave", self.leave_var),
            ("Phase V Escort", self.phase_v_escort_var),
            ("Off Post", self.off_post_var)
        ]

        for i, (text, var) in enumerate(checkbox_options):

            row = i // 2
            col = i % 2

            checkbox_container = tk.Frame(checkbox_frame, bg=WHITE)
            checkbox_container.grid(row=row, column=col, sticky="w", padx=(0, 30), pady=5)

            checkbox_canvas = tk.Canvas(
                checkbox_container,
                width=20,
                height=20,
                bg=WHITE,
                highlightthickness=0,
                cursor="hand2"
            )
            checkbox_canvas.pack(side=tk.LEFT, padx=(0, 10))

            self.checkbox_canvases.append(checkbox_canvas)

            checkbox_canvas.create_rectangle(
                2, 2, 18, 18,
                outline=GRAY_700,
                fill=WHITE,
                width=2,
                tags="checkbox_bg"
            )

            checkbox_label = tk.Label(
                checkbox_container,
                text=text,
                bg=WHITE,
                fg=GRAY_700,
                font=("Arial", 12),
                cursor="hand2"
            )
            checkbox_label.pack(side=tk.LEFT)

            def create_update_display(canvas, variable):
                def update_checkbox_display():
                    canvas.delete("checkmark")
                    if variable.get():

                        canvas.create_line(6, 10, 9, 13, fill=SUCCESS, width=3, tags="checkmark")
                        canvas.create_line(9, 13, 14, 8, fill=SUCCESS, width=3, tags="checkmark")

                        canvas.itemconfig("checkbox_bg", fill=GRAY_100)
                    else:
                        canvas.itemconfig("checkbox_bg", fill=WHITE)
                return update_checkbox_display

            def create_toggle_handler(canvas, variable, update_func):
                def toggle_checkbox():
                    current_value = variable.get()
                    variable.set(not current_value)
                    update_func()
                return toggle_checkbox

            update_display = create_update_display(checkbox_canvas, var)

            toggle_handler = create_toggle_handler(checkbox_canvas, var, update_display)

            checkbox_canvas.bind("<Button-1>", lambda e, handler=toggle_handler: handler())
            checkbox_label.bind("<Button-1>", lambda e, handler=toggle_handler: handler())

            def create_hover_handlers(canvas, variable):
                def on_enter(event):
                    if not variable.get():  # Only change if not checked
                        canvas.itemconfig("checkbox_bg", fill=GRAY_100)
                
                def on_leave(event):
                    if not variable.get():  # Only change if not checked
                        canvas.itemconfig("checkbox_bg", fill=WHITE)
                
                return on_enter, on_leave
            
            enter_handler, leave_handler = create_hover_handlers(checkbox_canvas, var)
            checkbox_canvas.bind("<Enter>", enter_handler)
            checkbox_canvas.bind("<Leave>", leave_handler)
            checkbox_label.bind("<Enter>", enter_handler)
            checkbox_label.bind("<Leave>", leave_handler)
    
    def create_buttons(self, parent):
        
        button_frame = tk.Frame(parent, bg=WHITE)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=40, pady=10)

        cancel_btn = self.create_rounded_button(
            button_frame,
            "Cancel",
            self.cancel,
            bg_color=GRAY_200,
            text_color=GRAY_700,
            side="right",
            padx=(10, 0)
        )

        button_text = "Update Entry" if self.is_editing else "Create Entry"
        save_btn = self.create_rounded_button(
            button_frame,
            button_text,
            self.save_entry,
            bg_color=SUCCESS,
            text_color=WHITE,
            side="right"
        )
    
    def create_rounded_button(self, parent, text, command, bg_color=BUTTON_PRIMARY, text_color=WHITE, side="left", padx=(0, 0)):
        
        button_frame = tk.Frame(parent, bg=WHITE)
        button_frame.pack(side=side, padx=padx)

        canvas = tk.Canvas(
            button_frame,
            width=120,
            height=40,
            bg=WHITE,
            highlightthickness=0
        )
        canvas.pack()

        def draw_rounded_rect(fill_color=bg_color):
            canvas.delete("button_bg")
            radius = 15
            x1, y1, x2, y2 = 2, 2, 118, 38

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
            60, 20,
            text=text,
            fill=text_color,
            font=("Arial", 12, "bold"),
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
    
    def validate_form(self):
        
        errors = []

        if not self.scanned_soldiers:
            errors.append("Please scan at least one CAC card")

        destination = self.destination_var.get().strip()
        if not destination or destination == "Fort Liberty":
            errors.append("Please enter a destination")

        phone = self.phone_var.get().strip()
        if not phone or phone == "(555) 123-4567":
            errors.append("Please enter a phone number")
        elif not phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "").isdigit():
            errors.append("Phone number should contain only digits, parentheses, hyphens, and spaces")
        
        return errors
    
    def save_entry(self):

        action_description = "update a sign-out entry" if self.is_editing else "create a new sign-out entry"
        
        try:
            auth_dialog = PinAuthDialog(self.root, action_description)
            authenticated, ds_name = auth_dialog.show_and_wait()
            
            if not authenticated:
                print(f"Authentication failed or cancelled for: {action_description}")
                return  # Don't proceed with save if authentication failed
                
            print(f"DS {ds_name} authenticated for: {action_description}")
            
        except Exception as e:
            print(f"Error during authentication: {e}")
            messagebox.showerror("Authentication Error", f"An error occurred during authentication: {str(e)}")
            return

        selected_categories = []
        if self.family_var.get():
            selected_categories.append("Family")
        if self.leave_var.get():
            selected_categories.append("Leave")
        if self.phase_v_escort_var.get():
            selected_categories.append("Phase V Escort")
        if self.off_post_var.get():
            selected_categories.append("Off Post")

        form_data = {
            'soldiers': self.scanned_soldiers,
            'destination': self.destination_var.get(),
            'phone': self.phone_var.get(),
            'categories': selected_categories,
            'ds': ds_name  # Can be extended later
        }

        print(f"Form data: {form_data}")
        if selected_categories:
            print(f"Selected categories: {selected_categories}")

        errors = DataUtils.validate_signout_data(form_data)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        
        try:
            if self.is_editing:

                entry_id = self.edit_data[0]
                all_signouts = self.data_manager.get_current_signouts()
                original_entry = None
                
                for signout in all_signouts:
                    if signout.get('id') == entry_id:
                        original_entry = signout
                        break
                
                if original_entry:

                    storage_data = DataUtils.convert_ui_to_storage(form_data)
                    storage_data['datetime'] = original_entry['datetime']  # Preserve original
                    storage_data['id'] = entry_id  # Preserve the original ID

                    success = self.data_manager.update_signout(entry_id, storage_data)
                    
                    if success:
                        messagebox.showinfo("Success", f"Sign-out entry {entry_id} updated successfully!")
                        self.close(success=True)
                    else:
                        messagebox.showerror("Error", f"Failed to update entry {entry_id}")
                else:
                    messagebox.showerror("Error", "Original entry not found")
            else:

                storage_data = DataUtils.convert_ui_to_storage(form_data)
                entry_id = self.data_manager.add_signout(storage_data)
                messagebox.showinfo("Success", f"Sign-out entry {entry_id} created successfully!")
                self.close(success=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entry: {str(e)}")
            print(f"Error saving entry: {e}")
    
    def cancel(self):
        
        self.close(success=False)
    
    def close(self, success=False):
        
        if self.parent:
            self.root.grab_release()

        if success and self.on_close_callback:
            self.on_close_callback()
            
        self.root.destroy()
    
    def show(self):
        
        if not self.parent:
            self.root.mainloop()
    
    def populate_form_with_data(self):
        
        if not self.edit_data:
            return

        entry_id = self.edit_data[0]  # First element is the ID
        
        try:

            all_signouts = self.data_manager.get_current_signouts()
            entry_data = None
            
            for signout in all_signouts:
                if signout.get('id') == entry_id:
                    entry_data = signout
                    break
            
            if entry_data:

                self.scanned_soldiers = entry_data.get('soldiers', [])

                destination = entry_data.get('destination', '')
                if destination:
                    self.destination_var.set(destination)

                phone = entry_data.get('phone', '')
                if phone:
                    self.phone_var.set(phone)

                categories = entry_data.get('categories', [])

                if not isinstance(categories, list):
                    categories = []
                
                self.family_var.set('Family' in categories)
                self.leave_var.set('Leave' in categories)
                self.phase_v_escort_var.set('Phase V Escort' in categories)
                self.off_post_var.set('Off Post' in categories)

                self.update_checkbox_visuals()

                if self.scanned_soldiers:

                    self.cac_instruction_label.pack_forget()
                    self.soldiers_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                    self.cac_frame.configure(bg=WHITE)
                    self.soldiers_display_frame.configure(bg=WHITE)

                    self.update_soldiers_display()

                    self.refresh_click_bindings()
                
        except Exception as e:
            print(f"Error populating form data: {e}")
    
    def update_checkbox_visuals(self):
        
        if not hasattr(self, 'checkbox_canvases'):
            return
            
        checkbox_vars = [
            self.family_var,
            self.leave_var,
            self.phase_v_escort_var,
            self.off_post_var
        ]
        
        for i, var in enumerate(checkbox_vars):
            if i < len(self.checkbox_canvases):
                canvas = self.checkbox_canvases[i]
                canvas.delete("checkmark")
                if var.get():

                    canvas.create_line(6, 10, 9, 13, fill=SUCCESS, width=3, tags="checkmark")
                    canvas.create_line(9, 13, 14, 8, fill=SUCCESS, width=3, tags="checkmark")

                    canvas.itemconfig("checkbox_bg", fill=GRAY_100)
                else:
                    canvas.itemconfig("checkbox_bg", fill=WHITE)

if __name__ == "__main__":

    window = NewEntryWindow()
    window.show()