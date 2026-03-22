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
import psutil
import hashlib
from datetime import datetime, timedelta

# --- CORE SECURITY: HARDWARE ID & ENCRYPTION ---
def get_hwid():
    try:
        cmd = 'wmic csproduct get uuid'
        uuid = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
        return uuid
    except Exception:
        return "GENERIC_HWID_0000"

def generate_secure_token(hwid):
    secret_salt = "GHOST_SILICON_2026_PRO"
    combined = f"{hwid}{secret_salt}"
    return hashlib.sha256(combined.encode()).hexdigest()

# --- APPEARANCE SETTINGS ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# v2.5 INFRASTRUCTURE
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRxluW8fJg1oJD1G8CTc47JuaKFrfKRW7cxVEOKUhoH5z1oxiq80XcHUGDZ5kkNuIfmfEIexGdaJxg/pub?output=csv"
SCRIPT_API_URL = "https://script.google.com/macros/s/AKfycbw79KJZvcdIVMmEpzSif9xzbhdCXS4QoscA7zkyCiuaU3vrwy6H4n3Tfhz-CDLnlFF0Ug/exec"

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW CONFIG ---
        self.title("GhostSemi | Command Console v2.5")
        self.geometry("500x820") 
        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        
        self.is_pro = False
        self.is_trial = False
        self.icon_manager = None
        self.current_hwid = get_hwid()

        # --- HEADER ---
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 28, "bold"), text_color="#00d4ff")
        self.header.pack(pady=(25, 5))
        self.version_label = ctk.CTkLabel(self, text="SILICON INFRASTRUCTURE v2.5", font=("Courier", 10), text_color="#555")
        self.version_label.pack()

        # --- PULSE: LIVE TELEMETRY ---
        self.tele_frame = ctk.CTkFrame(self, fg_color="#0a0a0c", border_width=1, border_color="#1a1a1a")
        self.tele_frame.pack(pady=15, padx=30, fill="x")
        self.cpu_label = ctk.CTkLabel(self.tele_frame, text="CPU: 0%", font=("Roboto Mono", 11), text_color="#00d4ff")
        self.cpu_label.grid(row=0, column=0, padx=20, pady=10)
        self.ram_label = ctk.CTkLabel(self.tele_frame, text="RAM: 0%", font=("Roboto Mono", 11), text_color="#00d4ff")
        self.ram_label.grid(row=0, column=1, padx=20, pady=10)
        self.pulse_bar = ctk.CTkProgressBar(self.tele_frame, width=380, height=4)
        self.pulse_bar.set(0)
        self.pulse_bar.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10)

        self.status_label = ctk.CTkLabel(self, text="STATUS: INITIALIZING...", font=("Roboto", 14))
        self.status_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=12)
        self.progress_bar.set(0.2) 
        self.progress_bar.pack(pady=15)

        self.speed_label = ctk.CTkLabel(self, text="LOCKED AT 1.8 GHz", font=("Courier New", 13, "bold"))
        self.speed_label.pack()

        # --- LOGIN / LICENSE FRAME ---
        self.license_frame = ctk.CTkFrame(self, fg_color="#111", border_width=1, border_color="#333")
        self.license_frame.pack(pady=20, padx=30, fill="x")
        self.email_entry = ctk.CTkEntry(self.license_frame, placeholder_text="REGISTERED EMAIL", width=280, height=40)
        self.email_entry.pack(pady=(20, 10))
        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="ENTER GS-ALPHA KEY", width=280, height=40)
        self.license_entry.pack(pady=10)
        self.upgrade_button = ctk.CTkButton(self.license_frame, text="VERIFY & ACTIVATE", font=("Orbitron", 14, "bold"), height=45, command=self.start_verification)
        self.upgrade_button.pack(pady=(15, 10))

        # --- TRIAL MODE BUTTON ---
        self.trial_button = ctk.CTkButton(self.license_frame, text="START 24H ALPHA TRIAL", fg_color="transparent", border_width=1, font=("Roboto", 11), command=self.activate_trial)
        self.trial_button.pack(pady=(0, 20))

        # --- RESIDENCY PORTAL ---
        self.portal_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.portal_frame.pack(pady=5)
        self.reset_hwid_btn = ctk.CTkButton(self.portal_frame, text="UNBIND DEVICE", font=("Roboto", 10), fg_color="#333", width=120, height=28, command=self.request_hwid_reset)
        self.reset_hwid_btn.grid(row=0, column=0, padx=5)
        self.renew_btn = ctk.CTkButton(self.portal_frame, text="EXTEND LICENSE", font=("Roboto", 10), fg_color="#1B4D3E", width=120, height=28, command=lambda: subprocess.run(["start", "https://ghostsemi-overdrive.github.io/GhostSemi-Core/"], shell=True))
        self.renew_btn.grid(row=0, column=1, padx=5)

        self.broadcast_label = ctk.CTkLabel(self, text="[HQ]: STANDBY FOR HANDSHAKE", font=("Courier", 9), text_color="#444")
        self.broadcast_label.pack(pady=10)

        # Start background threads
        self.update_telemetry()
        self.check_persistence()

    def update_telemetry(self):
        try:
            cpu, ram = psutil.cpu_percent(), psutil.virtual_memory().percent
            self.cpu_label.configure(text=f"CPU: {cpu}%")
            self.ram_label.configure(text=f"RAM: {ram}%")
            self.pulse_bar.set(cpu / 100)
            color = "#00d4ff" if (self.is_pro or self.is_trial) else "#333"
            self.pulse_bar.configure(progress_color=color)
        except: pass
        self.after(1000, self.update_telemetry)

    def activate_trial(self):
        trial_file = "trial_lock.bin"
        if os.path.exists(trial_file):
            with open(trial_file, "r") as f:
                start_date = datetime.fromisoformat(f.read().strip())
                if datetime.now() > start_date + timedelta(hours=24):
                    messagebox.showerror("GhostSemi", "Alpha Trial Expired. Key Required.")
                    return
            self.is_trial = True
            self.unlock_ui(days_left="TRIAL ACTIVE")
        else:
            with open(trial_file, "w") as f: f.write(datetime.now().isoformat())
            self.is_trial = True
            self.unlock_ui(days_left="24H TRIAL")
            messagebox.showinfo("GhostSemi", "24-Hour Alpha Trial Engaged.")

    def check_persistence(self):
        if os.path.exists("pro_mode.txt"):
            with open("pro_mode.txt", "r") as f:
                if f.read().strip() == generate_secure_token(self.current_hwid):
                    # Attempt silent background cloud check to verify 60-day expiry
                    threading.Thread(target=self.cloud_handshake, args=("", "", True), daemon=True).start()
                    return
        self.reset_to_eval()

    def reset_to_eval(self):
        self.is_pro = self.is_trial = False
        self.status_label.configure(text="STATUS: EVALUATION MODE", text_color="#888")
        self.progress_bar.configure(progress_color="#333")
        self.progress_bar.set(0.2)
        self.speed_label.configure(text="LOCKED AT 1.8 GHz", text_color="white")
        self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal")

    def start_verification(self):
        email, key = self.email_entry.get().strip(), self.license_entry.get().strip()
        if not email or not key:
            messagebox.showwarning("GhostSemi", "Authentication required.")
            return
        self.upgrade_button.configure(text="SYNCHING...", state="disabled")
        threading.Thread(target=self.cloud_handshake, args=(email, key, False), daemon=True).start()

    def cloud_handshake(self, email, key, is_auto):
        try:
            resp = requests.get(SHEET_CSV_URL, timeout=12)
            df = pd.read_csv(io.StringIO(resp.text))
            
            # Match by HWID if auto-loading, otherwise by email/key
            user = df[df['HWID'] == self.current_hwid] if is_auto else df[(df['Email'] == email) & (df['Key'] == key)]

            if not user.empty:
                # 1. AUTO-EXPIRY CHECK (60 DAYS)
                p_date = pd.to_datetime(user.iloc[0]['Timestamp'])
                days_used = (pd.Timestamp.now() - p_date).days
                if days_used > 60:
                    self.after(0, lambda: messagebox.showerror("Expired", "License Expired. Renew at HQ."))
                    if os.path.exists("pro_mode.txt"): os.remove("pro_mode.txt")
                    self.after(0, self.reset_to_eval)
                    return

                # 2. HWID BINDING CHECK
                existing_hwid = str(user.iloc[0]['HWID']).strip()
                if existing_hwid in ["nan", "", self.current_hwid]:
                    if existing_hwid in ["nan", ""]:
                        requests.post(SCRIPT_API_URL, json={"action":"register_hwid","email":user.iloc[0]['Email'],"hwid":self.current_hwid,"auth_token":"SECRET_ALPHA_TOKEN_99"})
                    
                    self.after(0, lambda: self.unlock_ui(60 - days_used))
                    with open("pro_mode.txt", "w") as f: f.write(generate_secure_token(self.current_hwid))
                else:
                    self.after(0, lambda: messagebox.showerror("Lock", "Hardware Mismatch. Unbind first."))
                    self.after(0, self.reset_to_eval)
            else:
                self.after(0, self.reset_to_eval)
        except Exception:
            self.after(0, lambda: self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal"))

    def unlock_ui(self, days_left):
        self.is_pro = True
        self.status_label.configure(text="STATUS: PRO ACTIVE", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0)
        self.speed_label.configure(text="CLOCKS: 4.2 GHz (OVERRIDDEN)", text_color="#00d4ff")
        self.upgrade_button.configure(text="SYSTEM OPTIMIZED", state="disabled", fg_color="#1B4D3E")
        self.broadcast_label.configure(text=f"[HQ]: {days_left} DAYS REMAINING", text_color="#00d4ff")

    def request_hwid_reset(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("GhostSemi", "Enter registered email.")
            return
        if messagebox.askyesno("Portal", "Unbind this device?"):
            try:
                resp = requests.post(SCRIPT_API_URL, json={"action":"reset_hwid","email":email,"auth_token":"SECRET_ALPHA_TOKEN_99"})
                if "RESET_SUCCESS" in resp.text:
                    if os.path.exists("pro_mode.txt"): os.remove("pro_mode.txt")
                    self.after(0, self.reset_to_eval)
                    messagebox.showinfo("Success", "Hardware lock cleared.")
            except: pass

    def hide_to_tray(self):
        self.withdraw()
        image = Image.new('RGB', (64, 64), color=(0, 212, 255))
        menu = (item('Open Console', self.show_window), item('Exit', self.destroy))
        self.icon_manager = pystray.Icon("GhostSemi", image, "GhostSemi v2.5", menu)
        threading.Thread(target=self.icon_manager.run, daemon=True).start()

    def show_window(self):
        if self.icon_manager: self.icon_manager.stop()
        self.deiconify()

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()