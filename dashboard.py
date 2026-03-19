import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import winsound
import threading
import pystray
from pystray import MenuItem as item

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GhostSemi | Management Console v1.5")
        self.geometry("500x520")
        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        
        self.is_pro = False
        self.icon_manager = None

        # UI
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 26, "bold"), text_color="#00d4ff")
        self.header.pack(pady=(20, 10))

        self.status_label = ctk.CTkLabel(self, text="STATUS: INITIALIZING...", font=("Roboto", 14))
        self.status_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=15, progress_color="#333")
        self.progress_bar.set(0.4) 
        self.progress_bar.pack(pady=20)

        self.speed_label = ctk.CTkLabel(self, text="LOCKED AT 1.8 GHz", font=("Courier", 12))
        self.speed_label.pack()

        self.license_frame = ctk.CTkFrame(self)
        self.license_frame.pack(pady=20, padx=20, fill="x")

        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="ENTER PRO KEY", width=250)
        self.license_entry.pack(pady=20)

        self.upgrade_button = ctk.CTkButton(self.license_frame, text="ACTIVATE TURBO", command=self.activate_pro)
        self.upgrade_button.pack(pady=(0, 20))

        self.tray_button = ctk.CTkButton(self, text="MINIMIZE TO SYSTEM TRAY", fg_color="transparent", border_width=1, command=self.hide_to_tray)
        self.tray_button.pack(pady=10)

        self.check_persistence()

    def check_persistence(self):
        if os.path.exists("pro_mode.txt"):
            with open("pro_mode.txt", "r") as f:
                if f.read().strip() == "GHOST_SECURE_5592_X":
                    self.unlock_ui()
                    winsound.Beep(1000, 200)
                else: self.reset_to_eval()
        else: self.reset_to_eval()

    def reset_to_eval(self):
        self.status_label.configure(text="STATUS: EVALUATION MODE", text_color="white")
        winsound.Beep(600, 150)

    def activate_pro(self):
        if self.license_entry.get().strip() == "GHOST-PRO-2026":
            self.is_pro = True
            winsound.Beep(800, 100)
            winsound.Beep(1200, 300)
            self.unlock_ui()
            with open("pro_mode.txt", "w") as f: f.write("GHOST_SECURE_5592_X")
            messagebox.showinfo("Success", "Turbo Mode Enabled.")
        else:
            winsound.Beep(300, 500)
            messagebox.showerror("Denied", "Invalid Access Key")

    def unlock_ui(self):
        self.status_label.configure(text="STATUS: PRO ACTIVE", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0) 
        self.speed_label.configure(text="CLOCKS: 4.2 GHz (TURBO)", text_color="#00d4ff")
        self.upgrade_button.configure(text="PRO ACTIVE", state="disabled", fg_color="#228B22")

    def hide_to_tray(self):
        self.withdraw()
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