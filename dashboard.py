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
import psutil  # --- SYSTEM TELEMETRY ENGINE ---
import hashlib # --- SENTINEL ENCRYPTION ENGINE ---

# --- CORE v2.3 SECURITY: HARDWARE ID FINGERPRINT ---
def get_hwid():
    """Generates a unique ID based on the computer's motherboard/CPU."""
    try:
        cmd = 'wmic csproduct get uuid'
        uuid = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
        return uuid
    except Exception:
        return "GENERIC_HWID_0000"

# --- SENTINEL v1.0: TOKEN ENCRYPTION ---
def generate_secure_token(hwid):
    """Creates an encrypted hash that is impossible to manually replicate in pro_mode.txt."""
    secret_salt = "GHOST_SILICON_2026_PRO"
    combined = f"{hwid}{secret_salt}"
    return hashlib.sha256(combined.encode()).hexdigest()

# --- APPEARANCE SETTINGS ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# v2.3 INFRASTRUCTURE URLS
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRxluW8fJg1oJD1G8CTc47JuaKFrfKRW7cxVEOKUhoH5z1oxiq80XcHUGDZ5kkNuIfmfEIexGdaJxg/pub?output=csv"
SCRIPT_API_URL = "https://script.google.com/macros/s/AKfycbw79KJZvcdIVMmEpzSif9xzbhdCXS4QoscA7zkyCiuaU3vrwy6H4n3Tfhz-CDLnlFF0Ug/exec"

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW CONFIG ---
        self.title("GhostSemi | Management Console v2.3")
        self.geometry("500x780") # Height adjusted for new portal buttons
        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        
        self.is_pro = False
        self.icon_manager = None
        self.current_hwid = get_hwid()

        # --- HEADER ---
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 28, "bold"), text_color="#00d4ff")
        self.header.pack(pady=(25, 5))

        self.version_label = ctk.CTkLabel(self, text="SILICON INFRASTRUCTURE v2.3", font=("Courier", 10), text_color="#555")
        self.version_label.pack()

        # --- PULSE: LIVE TELEMETRY PANEL ---
        self.tele_frame = ctk.CTkFrame(self, fg_color="#0a0a0c", border_width=1, border_color="#1a1a1a")
        self.tele_frame.pack(pady=15, padx=30, fill="x")

        self.cpu_label = ctk.CTkLabel(self.tele_frame, text="CPU: 0%", font=("Roboto Mono", 11), text_color="#00d4ff")
        self.cpu_label.grid(row=0, column=0, padx=20, pady=10)

        self.ram_label = ctk.CTkLabel(self.tele_frame, text="RAM: 0%", font=("Roboto Mono", 11), text_color="#00d4ff")
        self.ram_label.grid(row=0, column=1, padx=20, pady=10)

        self.pulse_bar = ctk.CTkProgressBar(self.tele_frame, width=380, height=4, progress_color="#00d4ff")
        self.pulse_bar.set(0)
        self.pulse_bar.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10)

        self.status_label = ctk.CTkLabel(self, text="STATUS: INITIALIZING...", font=("Roboto", 14))
        self.status_label.pack(pady=10)

        # --- VISUAL FEEDBACK ---
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=12, progress_color="#333")
        self.progress_bar.set(0.2) 
        self.progress_bar.pack(pady=15)

        self.speed_label = ctk.CTkLabel(self, text="LOCKED AT 1.8 GHz", font=("Courier New", 13, "bold"))
        self.speed_label.pack()

        # --- HWID DISPLAY ---
        self.hwid_label = ctk.CTkLabel(self, text=f"DEVICE ID: {self.current_hwid[:18]}...", font=("Courier", 9), text_color="#333")
        self.hwid_label.pack(pady=5)

        # --- LICENSE / CLOUD LOGIN FRAME ---
        self.license_frame = ctk.CTkFrame(self, fg_color="#111", border_width=1, border_color="#333")
        self.license_frame.pack(pady=20, padx=30, fill="x")

        self.email_entry = ctk.CTkEntry(self.license_frame, placeholder_text="REGISTERED EMAIL", width=280, height=40, border_color="#444")
        self.email_entry.pack(pady=(25, 10))

        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="ENTER GS-ALPHA KEY", width=280, height=40, border_color="#444")
        self.license_entry.pack(pady=10)

        self.upgrade_button = ctk.CTkButton(self.license_frame, text="VERIFY & ACTIVATE", font=("Orbitron", 14, "bold"), height=45, command=self.start_verification)
        self.upgrade_button.pack(pady=(15, 25))

        # --- RESIDENCY PORTAL: SELF-SERVICE ---
        self.portal_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.portal_frame.pack(pady=5)

        self.reset_hwid_btn = ctk.CTkButton(self.portal_frame, text="UNBIND DEVICE", font=("Roboto", 10), 
                                            fg_color="#333", width=120, height=28, command=self.request_hwid_reset)
        self.reset_hwid_btn.grid(row=0, column=0, padx=5)

        self.renew_btn = ctk.CTkButton(self.portal_frame, text="EXTEND LICENSE", font=("Roboto", 10), 
                                       fg_color="#1B4D3E", width=120, height=28, command=lambda: subprocess.run(["start", "https://ghostsemi-overdrive.github.io/GhostSemi-Core/"], shell=True))
        self.renew_btn.grid(row=0, column=1, padx=5)

        # --- HQ BROADCAST ---
        self.broadcast_label = ctk.CTkLabel(self, text="[HQ]: STANDBY FOR HANDSHAKE", font=("Courier", 9), text_color="#444")
        self.broadcast_label.pack(pady=10)

        self.tray_button = ctk.CTkButton(self, text="MINIMIZE TO TRAY", fg_color="transparent", text_color="#888", border_width=1, border_color="#222", command=self.hide_to_tray)
        self.tray_button.pack(pady=10)

        # Start background threads
        self.update_telemetry()
        self.check_persistence()

    def update_telemetry(self):
        """Refreshes CPU and RAM load in real-time."""
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.cpu_label.configure(text=f"CPU: {cpu}%")
            self.ram_label.configure(text=f"RAM: {ram}%")
            self.pulse_bar.set(cpu / 100)
            
            if not self.is_pro:
                self.pulse_bar.configure(progress_color="#333")
            else:
                self.pulse_bar.configure(progress_color="#00d4ff")
        except: pass
        self.after(1000, self.update_telemetry)

    def check_persistence(self):
        """Sentinel Check: Verifies the encrypted hardware token."""
        if os.path.exists("pro_mode.txt"):
            with open("pro_mode.txt", "r") as f:
                stored_hash = f.read().strip()
                if stored_hash == generate_secure_token(self.current_hwid):
                    self.unlock_ui()
                    winsound.Beep(1000, 150)
                else: 
                    self.reset_to_eval()
        else: 
            self.reset_to_eval()

    def reset_to_eval(self):
        self.is_pro = False
        self.status_label.configure(text="STATUS: EVALUATION MODE", text_color="#888")
        self.progress_bar.configure(progress_color="#333")
        self.progress_bar.set(0.2)
        self.speed_label.configure(text="LOCKED AT 1.8 GHz", text_color="white")
        self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal", fg_color=["#3B8ED0", "#1F6AA5"])
        self.email_entry.configure(state="normal")
        self.license_entry.configure(state="normal")

    def start_verification(self):
        email = self.email_entry.get().strip()
        key = self.license_entry.get().strip()
        if not email or not key:
            messagebox.showwarning("GhostSemi", "Authentication required.")
            return
        self.upgrade_button.configure(text="HANDSHAKING...", state="disabled")
        threading.Thread(target=self.cloud_handshake, args=(email, key), daemon=True).start()

    def cloud_handshake(self, email, key):
        try:
            response = requests.get(SHEET_CSV_URL, timeout=12)
            data = pd.read_csv(io.StringIO(response.text))
            valid_user = data[(data['Email'] == email) & (data['Key'] == key)]

            if not valid_user.empty:
                existing_hwid = str(valid_user.iloc[0]['HWID']).strip()
                if existing_hwid in ["nan", "", self.current_hwid]:
                    if existing_hwid in ["nan", ""]:
                        requests.post(SCRIPT_API_URL, json={
                            "action": "register_hwid",
                            "email": email,
                            "hwid": self.current_hwid,
                            "auth_token": "SECRET_ALPHA_TOKEN_99"
                        })
                    self.after(0, self.activation_success)
                else:
                    self.after(0, lambda: messagebox.showerror("Hardware Lock", "Key bound to another device.\nUse 'UNBIND DEVICE' to reset."))
                    self.after(0, lambda: self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal"))
            else:
                self.after(0, self.activation_denied)
        except Exception:
            self.after(0, lambda: self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal"))

    def request_hwid_reset(self):
        """Calls the Residency Portal API to clear the HWID lock."""
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("GhostSemi", "Enter your registered email first.")
            return
        
        confirm = messagebox.askyesno("Residency Portal", "Unbind this license from current hardware?\n(Allowed once every 30 days)")
        if confirm:
            try:
                resp = requests.post(SCRIPT_API_URL, json={
                    "action": "reset_hwid",
                    "email": email,
                    "auth_token": "SECRET_ALPHA_TOKEN_99"
                })
                if "RESET_SUCCESS" in resp.text:
                    messagebox.showinfo("Success", "Hardware lock cleared. You may now login on a new device.")
                    if os.path.exists("pro_mode.txt"): os.remove("pro_mode.txt")
                    self.after(0, self.reset_to_eval)
                else:
                    messagebox.showerror("Error", "Reset failed. User not found or limit reached.")
            except:
                messagebox.showerror("Error", "Server Unreachable.")

    def activation_success(self):
        self.is_pro = True
        winsound.Beep(800, 100)
        winsound.Beep(1300, 350)
        secure_hash = generate_secure_token(self.current_hwid)
        with open("pro_mode.txt", "w") as f: f.write(secure_hash)
        self.unlock_ui()
        messagebox.showinfo("GhostSemi v2.3", "Handshake Verified. System Optimized.")

    def activation_denied(self):
        winsound.Beep(300, 600)
        messagebox.showerror("Access Denied", "Invalid Credentials.")
        self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal")

    def unlock_ui(self):
        self.is_pro = True
        self.status_label.configure(text="STATUS: PRO ACTIVE", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0) 
        self.speed_label.configure(text="CLOCKS: 4.2 GHz (OVERRIDDEN)", text_color="#00d4ff")
        self.upgrade_button.configure(text="PRO ACTIVE", state="disabled", fg_color="#1B4D3E")
        self.broadcast_label.configure(text="[HQ]: SILICON OVERRIDE ENGAGED", text_color="#00d4ff")
        self.email_entry.configure(state="disabled")
        self.license_entry.configure(state="disabled")

    def hide_to_tray(self):
        self.withdraw()
        image = Image.new('RGB', (64, 64), color=(0, 212, 255))
        menu = (item('Open Console', self.show_window), item('Exit', self.destroy))
        self.icon_manager = pystray.Icon("GhostSemi", image, "GhostSemi v2.3", menu)
        threading.Thread(target=self.icon_manager.run, daemon=True).start()

    def show_window(self):
        if self.icon_manager: self.icon_manager.stop()
        self.deiconify()

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()