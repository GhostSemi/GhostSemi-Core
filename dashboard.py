import customtkinter as ctk
from tkinter import messagebox
import os
import winsound
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image

ctk.set_appearance_mode("dark")

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GhostSemi | Management Console v1.5")
        self.geometry("500x520")
        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        
        self.is_pro = False
        self.icon_manager = None

        # UI Elements
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE v1.5", font=("Orbitron", 24, "bold"), text_color="#00d4ff")
        self.header.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="STATUS: SCANNING...", font=("Roboto", 14))
        self.status_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=15)
        self.progress_bar.set(0.4)
        self.progress_bar.pack(pady=20)

        self.speed_label = ctk.CTkLabel(self, text="1.8 GHz EVALUATION", font=("Courier", 12))
        self.speed_label.pack()

        self.license_entry = ctk.CTkEntry(self, placeholder_text="ENTER ALPHA KEY", width=250)
        self.license_entry.pack(pady=20)

        self.upgrade_button = ctk.CTkButton(self, text="ACTIVATE TURBO", command=self.activate_pro)
        self.upgrade_button.pack(pady=10)

        # Persistence Check
        self.check_persistence()

    def check_persistence(self):
        if os.path.exists("pro_mode.txt"):
            with open("pro_mode.txt", "r") as f:
                if f.read().strip() == "GHOST_SECURE_5592_X":
                    self.unlock_ui()

    def activate_pro(self):
        if self.license_entry.get() == "GHOST-PRO-2026":
            with open("pro_mode.txt", "w") as f:
                f.write("GHOST_SECURE_5592_X")
            self.unlock_ui()
            winsound.Beep(1000, 400)
            messagebox.showinfo("Success", "Turbo Mode Enabled.")
        else:
            winsound.Beep(300, 500)
            messagebox.showerror("Error", "Invalid Key")

    def unlock_ui(self):
        self.is_pro = True
        self.status_label.configure(text="STATUS: PRO ACTIVE", text_color="#00d4ff")
        self.progress_bar.set(1.0)
        self.progress_bar.configure(progress_color="#00d4ff")
        self.speed_label.configure(text="4.2 GHz TURBO ENABLED", text_color="#00d4ff")
        self.upgrade_button.configure(state="disabled", text="PRO VERIFIED")

    def hide_to_tray(self):
        self.withdraw()
        image = Image.new('RGB', (64, 64), color=(0, 212, 255))
        menu = (item('Show', self.show_window), item('Exit', self.destroy))
        self.icon_manager = pystray.Icon("GhostSemi", image, "GhostSemi", menu)
        threading.Thread(target=self.icon_manager.run, daemon=True).start()

    def show_window(self):
        if self.icon_manager: self.icon_manager.stop()
        self.deiconify()

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()