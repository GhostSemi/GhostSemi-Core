import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import winsound
import threading
import pystray
from pystray import MenuItem as item

# --- Configuration ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("GhostSemi | Management Console v1.3")
        self.geometry("500x520")
        self.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        
        self.is_pro = False
        self.icon_manager = None

        # Startup Audio
        winsound.Beep(600, 150)

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)

        # Header
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 26, "bold"), text_color="#00d4ff")
        self.header.grid(row=0, column=0, pady=(20, 10))

        self.status_label = ctk.CTkLabel(self, text="STATUS: EVALUATION MODE", font=("Roboto", 14))
        self.status_label.grid(row=1, column=0, pady=5)

        # Performance Meter
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=15, progress_color="#333")
        self.progress_bar.set(0.4) 
        self.progress_bar.grid(row=2, column=0, pady=20)

        self.speed_label = ctk.CTkLabel(self, text="CLOCKS: 1.8 GHz (LOCKED)", font=("Courier", 12))
        self.speed_label.grid(row=3, column=0)

        # --- LICENSE SECTION ---
        self.license_frame = ctk.CTkFrame(self)
        self.license_frame.grid(row=4, column=0, pady=20, padx=20, sticky="nsew")
        self.license_frame.grid_columnconfigure(0, weight=1)

        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="ENTER PRO KEY", width=250)
        self.license_entry.grid(row=0, column=0, pady=20)

        self.upgrade_button = ctk.CTkButton(self.license_frame, text="ACTIVATE TURBO", 
                                            command=self.activate_pro, fg_color="#1f538d")
        self.upgrade_button.grid(row=1, column=0, pady=(0, 20))

        # --- UTILITY BUTTONS ---
        self.tray_button = ctk.CTkButton(self, text="MINIMIZE TO SYSTEM TRAY", 
                                         fg_color="transparent", border_width=1, command=self.hide_to_tray)
        self.tray_button.grid(row=5, column=0, pady=10)

        # Footer
        self.footer = ctk.CTkLabel(self, text="© 2026 GHOSTSEMI INFRASTRUCTURE", font=("Roboto", 10), text_color="gray")
        self.footer.grid(row=6, column=0, pady=20)

    # --- CORE LOGIC ---

    def activate_pro(self):
        """Validates key and triggers the Secure Handshake"""
        key = self.license_entry.get().strip()
        
        if key == "GHOST-PRO-2026":
            self.is_pro = True
            winsound.Beep(800, 100)
            winsound.Beep(1200, 300)
            
            self.unlock_ui()
            self.create_pro_flag() # The Key Maker
            messagebox.showinfo("Success", "Turbo Mode Enabled!\nBatch Processing Unlocked.")
        else:
            winsound.Beep(300, 500)
            messagebox.showerror("Denied", "Invalid Access Key")

    def create_pro_flag(self):
        """The 'Key Maker' - Writes the secure handshake for C++"""
        secure_key = "GHOST_SECURE_5592_X" 
        try:
            with open("pro_mode.txt", "w") as f:
                f.write(secure_key)
        except Exception as e:
            print(f"Error creating handshake: {e}")

    def unlock_ui(self):
        self.status_label.configure(text="STATUS: PRO ACTIVE (BATCH MODE)", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0) 
        self.speed_label.configure(text="CLOCKS: 4.2 GHz (TURBO ENABLED)", text_color="#00d4ff")
        self.upgrade_button.configure(text="PRO ACTIVE", state="disabled", fg_color="#228B22")

    # --- SYSTEM TRAY LOGIC ---

    def hide_to_tray(self):
        """Hides window and creates tray icon with failsafe"""
        self.withdraw()
        
        # Failsafe: Create blue square if favicon.ico is missing
        if os.path.exists("favicon.ico"):
            image = Image.open("favicon.ico")
        else:
            image = Image.new('RGB', (64, 64), color=(0, 212, 255))
        
        menu = (item('Show Dashboard', self.show_window), item('Exit', self.exit_action))
        self.icon_manager = pystray.Icon("GhostSemi", image, "GhostSemi Engine", menu)
        
        threading.Thread(target=self.icon_manager.run, daemon=True).start()

    def show_window(self):
        if self.icon_manager:
            self.icon_manager.stop()
        self.deiconify()

    def exit_action(self):
        if self.icon_manager:
            self.icon_manager.stop()
        self.destroy()

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()