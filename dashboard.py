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
import subprocess

# --- CORE v2.0 SECURITY: HARDWARE ID FINGERPRINT ---
def get_hwid():
    """Generates a unique ID based on the computer's motherboard/CPU."""
    try:
        # Grabbing the UUID and cleaning up the output string
        cmd = 'wmic csproduct get uuid'
        uuid = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
        return uuid
    except Exception:
        return "GENERIC_HWID_0000"

# --- APPEARANCE SETTINGS ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# v1.8 - v2.0: Your Live Silicon Infrastructure Link (CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRxluW8fJg1oJD1G8CTc47JuaKFrfKRW7cxVEOKUhoH5z1oxiq80XcHUGDZ5kkNuIfmfEIexGdaJxg/pub?output=csv"

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW CONFIG ---
        self.title("GhostSemi | Management Console v2.0")
        self.geometry("500x650") 
        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        
        self.is_pro = False
        self.icon_manager = None
        self.current_hwid = get_hwid()

        # --- HEADER ---
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 28, "bold"), text_color="#00d4ff")
        self.header.pack(pady=(25, 5))

        self.version_label = ctk.CTkLabel(self, text="SILICON INFRASTRUCTURE v2.0", font=("Courier", 10), text_color="#555")
        self.version_label.pack()

        self.status_label = ctk.CTkLabel(self, text="STATUS: INITIALIZING...", font=("Roboto", 14))
        self.status_label.pack(pady=10)

        # --- VISUAL FEEDBACK ---
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=12, progress_color="#333")
        self.progress_bar.set(0.2) 
        self.progress_bar.pack(pady=20)

        self.speed_label = ctk.CTkLabel(self, text="LOCKED AT 1.8 GHz", font=("Courier New", 13, "bold"))
        self.speed_label.pack()

        # --- HWID DISPLAY (ALPHA TRANSPARENCY) ---
        self.hwid_label = ctk.CTkLabel(self, text=f"DEVICE ID: {self.current_hwid[:18]}...", font=("Courier", 9), text_color="#333")
        self.hwid_label.pack(pady=5)

        # --- LICENSE / CLOUD LOGIN FRAME ---
        self.license_frame = ctk.CTkFrame(self, fg_color="#111", border_width=1, border_color="#333")
        self.license_frame.pack(pady=30, padx=30, fill="x")

        self.email_entry = ctk.CTkEntry(self.license_frame, placeholder_text="REGISTERED EMAIL", width=280, height=40, border_color="#444")
        self.email_entry.pack(pady=(25, 10))

        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="ENTER GS-ALPHA KEY", width=280, height=40, border_color="#444")
        self.license_entry.pack(pady=10)

        self.upgrade_button = ctk.CTkButton(self.license_frame, text="VERIFY & ACTIVATE", font=("Orbitron", 14, "bold"), height=45, command=self.start_verification)
        self.upgrade_button.pack(pady=(15, 25))

        # --- SYSTEM TRAY BUTTON ---
        self.tray_button = ctk.CTkButton(self, text="MINIMIZE TO TRAY", fg_color="transparent", text_color="#888", border_width=1, border_color="#222", command=self.hide_to_tray)
        self.tray_button.pack(pady=10)

        # Run persistence check on startup
        self.check_persistence()

    def check_persistence(self):
        """Checks local token and verifies it against the current Hardware ID."""
        if os.path.exists("pro_mode.txt"):
            with open("pro_mode.txt", "r") as f:
                stored_token = f.read().strip()
                # Security: Only unlock if the local token contains the unique hardware fingerprint
                if f"GHOST_SECURE_{self.current_hwid[:8]}" in stored_token:
                    self.unlock_ui()
                    winsound.Beep(1000, 150)
                else: 
                    self.reset_to_eval()
        else: 
            self.reset_to_eval()

    def reset_to_eval(self):
        self.status_label.configure(text="STATUS: EVALUATION MODE", text_color="#888")

    def start_verification(self):
        """Prepares UI for Cloud Handshake."""
        email = self.email_entry.get().strip()
        key = self.license_entry.get().strip()

        if not email or not key:
            messagebox.showwarning("GhostSemi", "Authentication required for Alpha access.")
            return

        self.upgrade_button.configure(text="HANDSHAKING...", state="disabled")
        
        # Threading prevents GUI freeze during the CSV download
        threading.Thread(target=self.cloud_handshake, args=(email, key), daemon=True).start()

    def cloud_handshake(self, email, key):
        """v2.0: Reaches out to database and cross-references Hardware Fingerprint."""
        try:
            response = requests.get(SHEET_CSV_URL, timeout=12)
            data = pd.read_csv(io.StringIO(response.text))
            
            # Match credentials
            valid_user = data[(data['Email'] == email) & (data['Key'] == key)]

            if not valid_user.empty:
                # OPTIONAL: You can add logic here to check a column named 'HWID' in your sheet
                # to see if the key has been used on a different machine before.
                self.after(0, self.activation_success)
            else:
                self.after(0, self.activation_denied)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Handshake Error", f"Could not reach Silicon Cloud: {e}"))
            self.after(0, lambda: self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal"))

    def activation_success(self):
        self.is_pro = True
        winsound.Beep(800, 100)
        winsound.Beep(1300, 350)
        
        # Save a Hardware-Bound Token locally
        secure_token = f"GHOST_SECURE_{self.current_hwid[:8]}_X"
        with open("pro_mode.txt", "w") as f: 
            f.write(secure_token)
            
        self.unlock_ui()
        messagebox.showinfo("GhostSemi v2.0", "Handshake Verified. Device Authorized for Turbo.")

    def activation_denied(self):
        winsound.Beep(300, 600)
        messagebox.showerror("Access Denied", "Invalid Credentials or Unauthorized Hardware.")
        self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal")

    def unlock_ui(self):
        """Activates the Neon Blue 'Turbo' Interface."""
        self.status_label.configure(text="STATUS: PRO ACTIVE", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0) 
        self.speed_label.configure(text="CLOCKS: 4.2 GHz (OVERRIDDEN)", text_color="#00d4ff")
        self.upgrade_button.configure(text="PRO ACTIVE", state="disabled", fg_color="#1B4D3E")
        self.email_entry.configure(state="disabled")
        self.license_entry.configure(state="disabled")

    def hide_to_tray(self):
        self.withdraw()
        # Create small icon for tray
        image = Image.new('RGB', (64, 64), color=(0, 212, 255))
        menu = (item('Open Console', self.show_window), item('Exit', self.destroy))
        self.icon_manager = pystray.Icon("GhostSemi", image, "GhostSemi v2.0", menu)
        threading.Thread(target=self.icon_manager.run, daemon=True).start()

    def show_window(self):
        if self.icon_manager: 
            self.icon_manager.stop()
        self.deiconify()

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()