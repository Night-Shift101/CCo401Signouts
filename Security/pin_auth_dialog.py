#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.colors import BG_PRIMARY, WHITE, GRAY_100, GRAY_200, GRAY_500, GRAY_600, GRAY_700, ONXY, SUCCESS, ERROR, PRIMARY_BLUE, PRIMARY_DARK
from Functions.pin_manager import PinManager

class PinAuthDialog:
    def __init__(self, parent=None, action_name="perform this action", default_ds=None):
        self.parent = parent
        self.action_name = action_name
        self.default_ds = default_ds
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

        # Button frame with guaranteed visible buttons
        button_frame = tk.Frame(inner_frame, bg=WHITE)
        button_frame.pack(fill=tk.X, pady=(30, 0))

        # Simple but visible buttons
        tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            bg="#e2e8f0",  # GRAY_200
            fg="#334155",  # GRAY_700  
            font=("Arial", 12, "bold"),
            width=10,
            height=2,
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=(10, 0))

        tk.Button(
            button_frame,
            text="Verify",
            command=self.verify_pin,
            bg="#2563eb",  # PRIMARY_BLUE
            fg="white",
            font=("Arial", 12, "bold"),
            width=10,
            height=2,
            cursor="hand2"
        ).pack(side=tk.RIGHT)

        def on_ds_select(event=None):
            self.pin_entry.focus_set()
        
        ds_combo.bind("<<ComboboxSelected>>", on_ds_select)
    
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
