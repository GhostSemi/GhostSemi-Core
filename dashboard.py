import customtkinter as ctk
import subprocess
import threading
import webbrowser
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GhostApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GHOSTSEMI | Enterprise Control")
        self.geometry("450x480")

        # Header
        self.label = ctk.CTkLabel(self, text="GHOST-AI ACCELERATOR", font=("Orbitron", 22, "bold"))
        self.label.pack(pady=20)

        # License Frame
        self.license_frame = ctk.CTkFrame(self)
        self.license_frame.pack(pady=10, padx=20, fill="x")

        self.license_entry = ctk.CTkEntry(self.license_frame, placeholder_text="Enter License Key")
        self.license_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        self.verify_btn = ctk.CTkButton(self.license_frame, text="Verify", width=80, command=self.check_license)
        self.verify_btn.pack(side="right", padx=10)

        # Telemetry Display
        self.status_label = ctk.CTkLabel(self, text="SYSTEM STATUS: IDLE", text_color="gray", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=15)

        self.mips_display = ctk.CTkLabel(self, text="0.00 MIPS", font=("Consolas", 32), text_color="#00d4ff")
        self.mips_display.pack(pady=5)

        # The Main "Turbo" Button
        self.turbo_button = ctk.CTkButton(self, text="ACTIVATE GHOST LOGIC", height=50, 
                                         fg_color="#0055ff", hover_color="#00d4ff",
                                         command=self.start_engine)
        self.turbo_button.pack(pady=20)

        # Monetization Link
        self.buy_link = ctk.CTkLabel(self, text="Get Ghost Pro (41% Boost)", 
                                    text_color="#00d4ff", cursor="hand2")
        self.buy_link.pack(pady=10)
        self.buy_link.bind("<Button-1>", lambda e: webbrowser.open("https://ghostsemi.com/buy"))

    def check_license(self):
        if self.license_entry.get() == "GHOST-PRO-2026":
            self.status_label.configure(text="MODE: PRO ACTIVE", text_color="gold")
            self.turbo_button.configure(fg_color="gold", text_color="black", text="ACTIVATE PRO ENGINE")
        else:
            self.status_label.configure(text="INVALID KEY: BASIC MODE", text_color="red")

    def start_engine(self):
        self.status_label.configure(text="ENGINE FIRING...", text_color="#00d4ff")
        threading.Thread(target=self.run_backend).start()

    def run_backend(self):
        try:
            # Run the C++ Software Chip
            subprocess.run(["./GhostAI.exe"], capture_output=True)
            
            # Read Telemetry from the Socket
            if os.path.exists("stats.ghost"):
                with open("stats.ghost", "r") as f:
                    mips_value = f.read()
                
                self.after(0, lambda: self.update_ui(mips_value))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text="ENGINE ERROR", text_color="red"))

    def update_ui(self, val):
        self.mips_display.configure(text=f"{float(val):.2f} MIPS")
        self.status_label.configure(text="OPTIMIZATION SUCCESSFUL", text_color="green")

if __name__ == "__main__":
    app = GhostApp()
    app.mainloop()