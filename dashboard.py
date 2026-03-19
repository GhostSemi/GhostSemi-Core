import customtkinter as ctk
from tkinter import messagebox
import os

# --- Configuration ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GhostDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GhostSemi | Software-Defined Silicon v1.1")
        self.geometry("500x450")
        self.is_pro = False

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)

        # Header
        self.header = ctk.CTkLabel(self, text="GHOSTSEMI CORE", font=("Orbitron", 24, "bold"), text_color="#00d4ff")
        self.header.grid(row=0, column=0, pady=(20, 10))

        # Status Indicator
        self.status_label = ctk.CTkLabel(self, text="STATUS: EVALUATION MODE", font=("Roboto", 14))
        self.status_label.grid(row=1, column=0, pady=5)

        # Performance Meter
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=15, progress_color="#555")
        self.progress_bar.set(0.4) # Base 40% performance
        self.progress_bar.grid(row=2, column=0, pady=20)

        self.speed_label = ctk.CTkLabel(self, text="CLKS: 1.8 GHz (LOCKED)", font=("Courier", 12))
        self.speed_label.grid(row=3, column=0)

        # --- LICENSE SECTION ---
        self.license_frame = ctk.CTkFrame(self)
        self.license_frame.grid(row=4, column=0, pady=30, padx=20, sticky="nsew")
        self.license_frame.grid_columnconfigure(0, weight=1)

        self.entry_label = ctk.CTkLabel(self.license_frame, text="ENTER PRO LICENSE KEY:")
        self.entry_label.grid(row=0, column=0, pady=(10, 0))

        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="GHOST-XXXX-XXXX", width=250)
        self.license_entry.grid(row=1, column=0, pady=10)

        self.upgrade_button = ctk.CTkButton(self.license_frame, text="ACTIVATE PRO FEATURES", 
                                            command=self.activate_pro, fg_color="#1f538d", hover_color="#00d4ff")
        self.upgrade_button.grid(row=2, column=0, pady=(0, 10))

        # Bottom Branding
        self.footer = ctk.CTkLabel(self, text="© 2026 GHOSTSEMI INFRASTRUCTURE", font=("Roboto", 10), text_color="gray")
        self.footer.grid(row=5, column=0, pady=20)

    def activate_pro(self):
        key = self.license_entry.get().strip()
        
        # The Secret Founder Key
        if key == "GHOST-PRO-2026":
            self.is_pro = True
            self.unlock_ui()
            self.create_pro_flag()
            messagebox.showinfo("Success", "GhostSemi Pro Activated!\nC++ Engine Unlocked.")
        else:
            messagebox.showerror("Invalid Key", "Please check your license key and try again.")

    def unlock_ui(self):
        """Transforms the UI to the Pro state"""
        self.status_label.configure(text="STATUS: PRO ACTIVE (FULL SILICON ACCESS)", text_color="#00d4ff")
        self.progress_bar.configure(progress_color="#00d4ff")
        self.progress_bar.set(1.0) # Full power
        self.speed_label.configure(text="CLKS: 4.2 GHz (TURBO ENABLED)", text_color="#00d4ff")
        self.upgrade_button.configure(text="PRO ACTIVE", state="disabled", fg_color="green")
        self.header.configure(text_color="white")

    def create_pro_flag(self):
        """Creates a hidden file the C++ engine can detect"""
        with open("pro_mode.txt", "w") as f:
            f.write("LICENSE_ACTIVE=TRUE")

if __name__ == "__main__":
    app = GhostDashboard()
    app.mainloop()