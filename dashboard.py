import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import winsound
import threading
import pystray
from pystray import MenuItem as item
import pandas as pd
import io
import requests
import sys

# --- APPEARANCE SETTINGS ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# v1.8: Your Live Silicon Infrastructure Link (CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRxluW8fJg1oJD1G8CTc47JuaKFrfKRW7cxVEOKUhoH5z1oxiq80XcHUGDZ5kkNuIfmfEIexGdaJxg/pub?output=csv"

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW CONFIG ---
        self.title("GhostSemi | Management Console v1.8")
        self.geometry("500x620") 
        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        
        self.is_pro = False
        self.icon_manager = None

        # --- HEADER ---
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 26, "bold"), text_color="#00d4ff")
        self.header.pack(pady=(20, 10))

        self.status_label = ctk.CTkLabel(self, text="STATUS: INITIALIZING...", font=("Roboto", 14))
        self.status_label.pack(pady=5)

        # --- VISUAL FEEDBACK ---
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=15, progress_color="#333")
        self.progress_bar.set(0.4) 
        self.progress_bar.pack(pady=20)

        self.speed_label = ctk.CTkLabel(self, text="LOCKED AT 1.8 GHz", font=("Courier", 12))
        self.speed_label.pack()

        # --- LICENSE / CLOUD LOGIN FRAME ---
        self.license_frame = ctk.CTkFrame(self)
        self.license_frame.pack(pady=20, padx=20, fill="x")

        self.email_entry = ctk.CTkEntry(self.license_frame, placeholder_text="REGISTERED EMAIL", width=250)
        self.email_entry.pack(pady=(20, 10))

        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="ENTER GS-ALPHA KEY", width=250)
        self.license_entry.pack(pady=10)

        self.upgrade_button = ctk.CTkButton(self.license_frame, text="VERIFY & ACTIVATE", command=self.start_verification)
        self.upgrade_button.pack(pady=(10, 20))

        # --- SYSTEM TRAY BUTTON ---
        self.tray_button = ctk.CTkButton(self, text="MINIMIZE TO SYSTEM TRAY", fg_color="transparent", border_width=1, command=self.hide_to_tray)
        self.tray_button.pack(pady=10)

        # Run persistence check on startup
        self.check_persistence()

    def check_persistence(self):
        """Checks if the user has already been verified locally."""
        if os.path.exists("pro_mode.txt"):
            with open("pro_mode.txt", "r") as f:
                if f.read().strip() == "GHOST_SECURE_5592_X":
                    self.unlock_ui()
                    winsound.Beep(1000, 200)
                else: self.reset_to_eval()
        else: self.reset_to_eval()

    def reset_to_eval(self):
        self.status_label.configure(text="STATUS: EVALUATION MODE", text_color="white")

    def start_verification(self):
        """Prepares the UI for the cloud handshake."""
        email = self.email_entry.get().strip()
        key = self.license_entry.get().strip()

        if not email or not key:
            messagebox.showwarning("GhostSemi", "Credentials required for Alpha access.")
            return

        self.upgrade_button.configure(text="VERIFYING...", state="disabled")
        
        # Start threading so the GUI doesn't 'Not Respond'
        threading.Thread(target=self.cloud_handshake, args=(email, key), daemon=True).start()

    def cloud_handshake(self, email, key):
        """The core v1.8 logic: Reaching out to the Google Sheet CSV."""
        try:
            response = requests.get(SHEET_CSV_URL, timeout=10)
            data = pd.read_csv(io.StringIO(response.text))
            
            # Logic: Check if Email and Key exist in the same row
            # Matches Column Headers: 'Email' and 'Key'
            valid = data[(data['Email'] == email) & (data['Key'] == key)]

            if not valid.empty:
                self.after(0, self.activation_success)
            else:
                self.after(0, self.activation_denied)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Connection Error", f"Database Unreachable: {e}"))
            self.after(0, lambda: self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal"))

    def activation_success(self):
        self.is_pro = True
        winsound.Beep(800, 100)
        winsound.Beep(1200, 300)
        self.unlock_ui()
        # Save a 'Token' so they don't have to verify every time
        with open("pro_mode.txt", "w") as f: f.write("GHOST_SECURE_5592_X")
        messagebox.showinfo("GhostSemi v1.8", "Cloud Handshake Successful. Turbo Mode Active.")

    def activation_denied(self):
        winsound.Beep(300, 500)
        messagebox.showerror("Access Denied", "Credentials not found in the Alpha Database.")
        self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal")

    def unlock_ui(self):
        """Changes the UI look to the Blue/Turbo mode."""
        self.status_label.configure(text="STATUS: PRO ACTIVE", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0) 
        self.speed_label.configure(text="CLOCKS: 4.2 GHz (TURBO)", text_color="#00d4ff")
        self.upgrade_button.configure(text="PRO ACTIVE", state="disabled", fg_color="#228B22")

    def hide_to_tray(self):
        self.withdraw()
        # Create a simple blue square icon for the tray
        image = Image.new('RGB', (64, 64), color=(0, 212, 255))
        menu = (item('Show Dashboard', self.show_window), item('Exit', self.destroy))
        self.icon_manager = pystray.Icon("GhostSemi", image, "GhostSemi", menu)
        threading.Thread(target=self.icon_manager.run, daemon=True).start()

    def show_window(self):
        if self.icon_manager: self.icon_manager.stop()
        self.deiconify()

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()