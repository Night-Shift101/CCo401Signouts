#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.colors import BG_PRIMARY, WHITE, GRAY_100, GRAY_200, GRAY_500, GRAY_600, GRAY_700, ONXY, SUCCESS, ERROR, PRIMARY_BLUE, PRIMARY_DARK, BUTTON_PRIMARY, get_theme_colors
from Config.theme_manager import theme_manager
from Functions.pin_manager import PinManager


def getDefaultDrill():
    with open("Security/last_ds.txt", "r") as f:
        return f.read()

class PinAuthDialog:
    def __init__(self, parent=None, action_name="perform this action", default_ds=None):
        self.parent = parent
        self.action_name = action_name
        self.default_ds = getDefaultDrill()
        self.pin_manager = PinManager()
        self.authenticated = False
        self.ds_name = None

        self.dialog = tk.Toplevel(parent) if parent else tk.Tk()
        self.dialog.title("Drill Sergeant Authentication")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg=BG_PRIMARY)
        self.dialog.resizable(False, False)

        if parent:
            self.dialog.transient(parent)
            self.dialog.grab_set()

        self.center_dialog()
        self.create_ui()
        
        # Apply current theme
        self.apply_current_theme()

        if self.default_ds and self.default_ds in self.pin_manager.list_ds_names():
            self.ds_var.set(self.default_ds)
            self.dialog.after(100, lambda: self.pin_entry.focus_set())
        else:
            self.ds_var.set("Select Drill Sergeant")
    
    def center_dialog(self):
        self.dialog.update_idletasks()
        
        if self.parent:
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            x = parent_x + (parent_width // 2) - (600 // 2)
            y = parent_y + (parent_height // 2) - (500 // 2)
        else:
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width // 2) - (600 // 2)
            y = (screen_height // 2) - (500 // 2)
        
        self.dialog.geometry(f"600x500+{x}+{y}")
    
    def create_ui(self):
        main_frame = tk.Frame(self.dialog, bg=BG_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        content_frame = tk.Frame(main_frame, bg=WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True)

        inner_frame = tk.Frame(content_frame, bg=WHITE)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        title_label = tk.Label(
            inner_frame,
            text="DRILL SERGEANT\nAUTHENTICATION",
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 16, "bold"),
            justify=tk.CENTER
        )
        title_label.pack(pady=(0, 10))

        action_label = tk.Label(
            inner_frame,
            text=f"Authentication required to {self.action_name}",
            bg=WHITE,
            fg=GRAY_600,
            font=("Arial", 11),
            justify=tk.CENTER,
            wraplength=300
        )
        action_label.pack(pady=(0, 20))

        ds_label = tk.Label(
            inner_frame,
            text="Drill Sergeant:",
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        ds_label.pack(fill=tk.X, pady=(0, 5))

        ds_names = self.pin_manager.list_ds_names()
        self.ds_var = tk.StringVar()
        
        ds_combo = ttk.Combobox(
            inner_frame,
            textvariable=self.ds_var,
            values=ds_names,
            state="readonly",
            font=("Arial", 11),
            height=6
        )
        ds_combo.pack(fill=tk.X, pady=(0, 15))

        pin_label = tk.Label(
            inner_frame,
            text="PIN:",
            bg=WHITE,
            fg=GRAY_700,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        pin_label.pack(fill=tk.X, pady=(0, 5))
        
        self.pin_var = tk.StringVar()
        self.pin_entry = tk.Entry(
            inner_frame,
            textvariable=self.pin_var,
            font=("Arial", 14),
            show="*",
            bg=GRAY_100,
            fg=GRAY_700,
            relief="flat",
            bd=0,
            insertbackground=GRAY_700
        )
        self.pin_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)

        self.pin_entry.bind("<Return>", lambda e: self.verify_pin())

        # Button frame with rounded buttons
        button_frame = tk.Frame(inner_frame, bg=WHITE)
        button_frame.pack(fill=tk.X, pady=(30, 0))

        # Create rounded buttons using the same logic as other screens
        self.create_rounded_button(
            button_frame,
            "Cancel",
            self.cancel,
            bg_color=GRAY_200,
            text_color=GRAY_700,
            side="right",
            padx=(10, 0)
        )

        self.create_rounded_button(
            button_frame,
            "Verify",
            self.verify_pin,
            bg_color=PRIMARY_BLUE,
            text_color=WHITE,
            side="right"
        )

        def on_ds_select(event=None):
            self.pin_entry.focus_set()
        
        ds_combo.bind("<<ComboboxSelected>>", on_ds_select)
    def write_last_drill(self, lastdrill):
        with open("Security/last_ds.txt", "w") as f:
            f.write(lastdrill)
    
    def verify_pin(self):
        ds_name = self.ds_var.get()
        pin = self.pin_var.get()

        if not ds_name or ds_name == "Select Drill Sergeant":
            messagebox.showerror("Error", "Please select a Drill Sergeant")
            return
        
        if not pin:
            messagebox.showerror("Error", "Please enter your PIN")
            return

        if self.pin_manager.verify_pin(ds_name, pin):
            self.authenticated = True
            self.ds_name = ds_name
            self.write_last_drill(ds_name)
            self.close()
        else:
            messagebox.showerror("Authentication Failed", "Invalid PIN. Please try again.")
            self.pin_var.set("")
    
    def cancel(self):
        self.authenticated = False
        self.close()
    
    def close(self):
        if self.parent:
            self.dialog.grab_release()
        self.dialog.destroy()
    
    def show_and_wait(self):
        self.center_dialog()
        self.dialog.wait_window()
        return self.authenticated, self.ds_name

    def create_rounded_button(self, parent, text, command, bg_color=PRIMARY_BLUE, text_color=WHITE, side="left", padx=(0, 0)):
        """Create a rounded button with hover effects"""
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

    def apply_current_theme(self):
        """Apply the current theme to the pin auth dialog"""
        try:
            current_theme = theme_manager.get_current_theme()
            colors = get_theme_colors(current_theme)
            
            # Update dialog background
            self.dialog.configure(bg=colors['BG_PRIMARY'])
            
            # Update any frames and widgets that might have been created
            if hasattr(self, 'main_frame'):
                self.main_frame.configure(bg=colors['BG_PRIMARY'])
                
        except Exception as e:
            print(f"Error applying theme to PinAuthDialog: {e}")

def test_pin_dialog():
    root = tk.Tk()
    root.withdraw()
    
    dialog = PinAuthDialog(root, "edit a sign-out entry")
    authenticated, ds_name = dialog.show_and_wait()
    
    if authenticated:
        print(f"Authentication successful! DS: {ds_name}")
    else:
        print("Authentication cancelled or failed")
    
    root.destroy()

if __name__ == "__main__":
    test_pin_dialog()
