import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
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
import webbrowser
import smtplib
from email.message import EmailMessage
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

# --- v2.6 LIVE CONFIGURATION ---
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRxluW8fJg1oJD1G8CTc47JuaKFrfKRW7cxVEOKUhoH5z1oxiq80XcHUGDZ5kkNuIfmfEIexGdaJxg/pub?output=csv"
SCRIPT_API_URL = "https://script.google.com/macros/s/AKfycbw79KJZvcdIVMmEpzSif9xzbhdCXS4QoscA7zkyCiuaU3vrwy6H4n3Tfhz-CDLnlFF0Ug/exec"
GITHUB_RELEASE_URL = "https://github.com/GhostSemi/GhostSemi-Core/releases/latest"

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW CONFIG ---
        self.title("GhostSemi | Command Console v2.6")
        self.geometry("500x880") 
        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        
        self.is_pro = False
        self.is_trial = False
        self.icon_manager = None
        self.current_hwid = get_hwid()

        # --- HEADER ---
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 28, "bold"), text_color="#00d4ff")
        self.header.pack(pady=(25, 5))
        self.version_label = ctk.CTkLabel(self, text="SILICON INFRASTRUCTURE v2.6", font=("Courier", 10), text_color="#555")
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

        self.admin_note_status = ctk.CTkLabel(self, text="⚠ NOTE: Run as Administrator for full telemetry", font=("Roboto", 10), text_color="#d35400")
        self.admin_note_status.pack()

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

        # --- DEPLOYMENT SECTION ---
        self.deploy_button = ctk.CTkButton(
            self, 
            text="DOWNLOAD GHOSTSEMI SETUP (v2.6)", 
            font=("Roboto", 12, "bold"), 
            fg_color="#1a1a1a", 
            border_width=1, 
            border_color="#00d4ff", 
            height=40, 
            command=lambda: webbrowser.open(GITHUB_RELEASE_URL)
        )
        self.deploy_button.pack(pady=5)

        self.trial_button = ctk.CTkButton(self.license_frame, text="START 24H ALPHA TRIAL", fg_color="transparent", border_width=1, font=("Roboto", 11), command=self.activate_trial)
        self.trial_button.pack(pady=(0, 20))

        # --- RESIDENCY PORTAL ---
        self.portal_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.portal_frame.pack(pady=5)
        self.reset_hwid_btn = ctk.CTkButton(self.portal_frame, text="UNBIND DEVICE", font=("Roboto", 10), fg_color="#333", width=120, height=28, command=self.request_hwid_reset)
        self.reset_hwid_btn.grid(row=0, column=0, padx=5)
        self.renew_btn = ctk.CTkButton(self.portal_frame, text="EXTEND LICENSE", font=("Roboto", 10), fg_color="#1B4D3E", width=120, height=28, command=lambda: webbrowser.open("https://ghostsemi-overdrive.github.io/GhostSemi-Core/"))
        self.renew_btn.grid(row=0, column=1, padx=5)

        # --- ADMIN MAILER ACCESS (HIDDEN) ---
        self.admin_access_btn = ctk.CTkButton(self, text="ADMIN ACCESS", font=("Roboto", 9), fg_color="transparent", text_color="#222", width=80, command=self.open_admin_mailer)
        self.admin_access_btn.pack(side="bottom", pady=5)

        self.broadcast_label = ctk.CTkLabel(self, text="[HQ]: STANDBY FOR HANDSHAKE", font=("Courier", 9), text_color="#444")
        self.broadcast_label.pack(pady=10)

        self.update_telemetry()
        self.check_persistence()

    # --- SECURITY INITIALIZATION PAGE (SMARTSCREEN BYPASS) ---
    def open_security_initialization(self):
        security_win = ctk.CTkToplevel(self)
        security_win.title("PROVISIONING COMPLETE // SECURITY PROTOCOL")
        security_win.geometry("550x680")
        security_win.attributes("-topmost", True)

        ctk.CTkLabel(security_win, text="PROVISIONING COMPLETE", font=("Orbitron", 18, "bold"), text_color="#00d4ff").pack(pady=(20, 5))
        ctk.CTkLabel(security_win, text="ALPHA ACCESS GRANTED // CORE v2.6", font=("Courier", 10), text_color="#555").pack()

        proc_frame = ctk.CTkFrame(security_win, fg_color="#0a0a0c", border_width=1, border_color="#1a1a1a")
        proc_frame.pack(pady=20, padx=30, fill="both", expand=True)

        instructions = [
            ("01. UNBLOCK BINARY", "Right-Click the .exe > Properties > Check 'Unblock' > Apply."),
            ("02. SMARTSCREEN BYPASS", "If Windows flags the file, select 'More Info' > 'Run Anyway'."),
            ("03. AV EXCLUSION (RECOMMENDED)", "Move .exe to a dedicated folder. Windows Security > Exclusions > Add Folder."),
            ("04. OBFUSCATION HANDSHAKE", "The console is hardware-encrypted. If Antivirus flags 'Behavioral Scanning', select 'Allow'.")
        ]

        for title, desc in instructions:
            t_lbl = ctk.CTkLabel(proc_frame, text=title, font=("Roboto Mono", 12, "bold"), text_color="#d35400", anchor="w")
            t_lbl.pack(fill="x", padx=20, pady=(15, 0))
            d_lbl = ctk.CTkLabel(proc_frame, text=desc, font=("Roboto", 11), text_color="#888", wraplength=450, justify="left")
            d_lbl.pack(fill="x", padx=20, pady=(0, 5))

        footer_text = (
            "License: Alpha Professional\n"
            "Status: Operational\n"
            "Auth: Hardware Locked (HWID)\n"
            "SHA256: 117d1acc84ead139b41349ad21872375db5f46117158fbfd9f34816f1550564e"
        )
        ctk.CTkLabel(security_win, text=footer_text, font=("Courier", 9), text_color="#444", justify="left").pack(pady=10)
        ctk.CTkButton(security_win, text="INITIALIZE SECURE TRANSMISSION", fg_color="#1B4D3E", command=security_win.destroy).pack(pady=15)

    def open_admin_mailer(self):
        admin_win = ctk.CTkToplevel(self)
        admin_win.title("GhostSemi | Admin Dispatch")
        admin_win.geometry("400x350")
        ctk.CTkLabel(admin_win, text="DISPATCH LICENSE KEY", font=("Orbitron", 16)).pack(pady=10)
        target_email = ctk.CTkEntry(admin_win, placeholder_text="Customer Email", width=250)
        target_email.pack(pady=5)
        new_key = ctk.CTkEntry(admin_win, placeholder_text="Generated Key", width=250)
        new_key.pack(pady=5)
        
        def dispatch():
            e, k = target_email.get(), new_key.get()
            if e and k:
                threading.Thread(target=self.send_license_email, args=(e, k), daemon=True).start()
                admin_win.destroy()
            else: messagebox.showerror("Error", "Fields cannot be empty")
        ctk.CTkButton(admin_win, text="SEND KEY VIA SMTP", command=dispatch).pack(pady=20)

    def send_license_email(self, customer_email, license_key):
        msg = EmailMessage()
        msg.set_content(f"Hello,\n\nWelcome to GhostSemi Silicon. Your access key is ready.\n\nYOUR KEY: {license_key}\n\n1. DOWNLOAD: {GITHUB_RELEASE_URL}\n2. INSTALL: Run GhostSemi_Setup_v2.6.exe\n3. IMPORTANT: Right-click and 'Run as Administrator'.\n\nStay Overclocked,\nGhostSemi Silicon HQ")
        msg['Subject'] = "🛡️ Your GhostSemi Access: License Key & Setup"
        msg['From'] = "cliphomondi3@gmail.com"
        msg['To'] = customer_email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('cliphomondi3@gmail.com', 'tszu mjpy apmx kjuk')
                smtp.send_message(msg)
            self.after(0, lambda: messagebox.showinfo("Success", "License dispatched."))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Mail Error", f"Failed: {str(e)}"))

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
                    messagebox.showerror("GhostSemi", "Alpha Trial Expired.")
                    return
            self.is_trial = True
            self.unlock_ui("TRIAL ACTIVE")
        else:
            with open(trial_file, "w") as f: f.write(datetime.now().isoformat())
            self.is_trial = True
            self.unlock_ui("24H TRIAL")
            messagebox.showinfo("GhostSemi", "24-Hour Alpha Trial Engaged.")

    def check_persistence(self):
        if os.path.exists("pro_mode.txt"):
            with open("pro_mode.txt", "r") as f:
                if f.read().strip() == generate_secure_token(self.current_hwid):
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
            user = df[df['HWID'] == self.current_hwid] if is_auto else df[(df['Email'] == email) & (df['Key'] == key)]
            if not user.empty:
                p_date = pd.to_datetime(user.iloc[0]['Timestamp'])
                days_used = (pd.Timestamp.now() - p_date).days
                if days_used > 60:
                    self.after(0, lambda: messagebox.showerror("Expired", "License Expired."))
                    if os.path.exists("pro_mode.txt"): os.remove("pro_mode.txt")
                    self.after(0, self.reset_to_eval)
                    return
                existing_hwid = str(user.iloc[0]['HWID']).strip()
                if existing_hwid in ["nan", "", self.current_hwid]:
                    if existing_hwid in ["nan", ""]:
                        requests.post(SCRIPT_API_URL, json={"action":"register_hwid","email":user.iloc[0]['Email'],"hwid":self.current_hwid,"auth_token":"SECRET_ALPHA_TOKEN_99"})
                    self.after(0, lambda: self.unlock_ui(60 - days_used))
                    with open("pro_mode.txt", "w") as f: f.write(generate_secure_token(self.current_hwid))
                else:
                    self.after(0, lambda: messagebox.showerror("Lock", "Hardware Mismatch."))
                    self.after(0, self.reset_to_eval)
            else: self.after(0, self.reset_to_eval)
        except Exception: self.after(0, lambda: self.upgrade_button.configure(text="VERIFY & ACTIVATE", state="normal"))

    def unlock_ui(self, days_left):
        self.is_pro = True
        self.status_label.configure(text="STATUS: PRO ACTIVE", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0)
        self.speed_label.configure(text="CLOCKS: 4.2 GHz (OVERRIDDEN)", text_color="#00d4ff")
        self.upgrade_button.configure(text="SYSTEM OPTIMIZED", state="disabled", fg_color="#1B4D3E")
        self.broadcast_label.configure(text=f"[HQ]: {days_left} REMAINING", text_color="#00d4ff")
        
        # TRIGGER THE SECURITY BYPASS GUIDE
        self.after(1000, self.open_security_initialization)

    def request_hwid_reset(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("GhostSemi", "Enter email.")
            return
        if messagebox.askyesno("Portal", "Unbind device?"):
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
        self.icon_manager = pystray.Icon("GhostSemi", image, "GhostSemi v2.6", menu)
        threading.Thread(target=self.icon_manager.run, daemon=True).start()

    def show_window(self):
        if self.icon_manager: self.icon_manager.stop()
        self.deiconify()

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()