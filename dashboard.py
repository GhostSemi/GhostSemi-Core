import customtkinter as ctk
from tkinter import messagebox
import os
import winsound  # Built-in Windows library for audio

# --- Configuration ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Startup Audio (Option B)
        winsound.Beep(600, 150) # A quick "Wake up" chirp

        self.title("GhostSemi | Infrastructure Dashboard v1.2")
        self.geometry("500x480")
        self.is_pro = False

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 26, "bold"), text_color="#00d4ff")
        self.header.grid(row=0, column=0, pady=(20, 10))

        self.status_label = ctk.CTkLabel(self, text="STATUS: SYSTEM IDLE", font=("Roboto", 14))
        self.status_label.grid(row=1, column=0, pady=5)

        # Performance Meter
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=15, progress_color="#333")
        self.progress_bar.set(0.4) 
        self.progress_bar.grid(row=2, column=0, pady=20)

        self.speed_label = ctk.CTkLabel(self, text="LOCKED AT 1.8 GHz", font=("Courier", 12))
        self.speed_label.grid(row=3, column=0)

        # --- LICENSE SECTION ---
        self.license_frame = ctk.CTkFrame(self)
        self.license_frame.grid(row=4, column=0, pady=30, padx=20, sticky="nsew")
        self.license_frame.grid_columnconfigure(0, weight=1)

        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="ENTER PRO KEY", width=250)
        self.license_entry.grid(row=0, column=0, pady=20)

        self.upgrade_button = ctk.CTkButton(self.license_frame, text="ACTIVATE TURBO", 
                                            command=self.activate_pro, fg_color="#1f538d")
        self.upgrade_button.grid(row=1, column=0, pady=(0, 20))

        # Branding
        self.footer = ctk.CTkLabel(self, text="TELEMETRY ACTIVE: stats.ghost", font=("Roboto", 10), text_color="gray")
        self.footer.grid(row=5, column=0)

    def activate_pro(self):
        key = self.license_entry.get().strip()
        
        if key == "GHOST-PRO-2026":
            self.is_pro = True
            
            # Success Audio (Option B)
            winsound.Beep(800, 100)
            winsound.Beep(1200, 300) # "Level Up" sound
            
            self.unlock_ui()
            self.create_pro_flag()
            messagebox.showinfo("Success", "Turbo Mode Enabled!")
        else:
            winsound.Beep(300, 500) # "Error" low tone
            messagebox.showerror("Denied", "Invalid Access Key")

    def unlock_ui(self):
        self.status_label.configure(text="STATUS: TURBO ACTIVE", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0) 
        self.speed_label.configure(text="CLOCKS: 4.2 GHz (MAX)", text_color="#00d4ff")
        self.upgrade_button.configure(text="PRO ACTIVE", state="disabled", fg_color="#228B22")

    def create_pro_flag(self):
        with open("pro_mode.txt", "w") as f:
            f.write("PRO_STATUS=ENABLED")

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()