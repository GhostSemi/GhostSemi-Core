# 👻 GhostSemi Core | Software-Defined Silicon v2.6-Stable

**GhostSemi** is a high-performance virtual semiconductor infrastructure. It allows developers and engineers to deploy simulated silicon cycles directly on a host OS, bridging the gap between hardware abstraction and software execution.

---

## 🚀 System Architecture
GhostSemi operates on a dual-layer architecture:
1.  **Management Console (Python/CustomTkinter):** A real-time dashboard for frequency control, license validation, and system monitoring.
2.  **Silicon Engine (C++):** A high-speed execution core capable of 4.2 GHz Turbo Batch processing.

---

## 🛡️ Pro Features (Unlocked)
- **Turbo Frequency:** Unlock 4.2 GHz simulated clock speeds.
- **Batch Processor:** Queue and execute up to 5 concurrent silicon tasks.
- **Secure Handshake:** Encrypted license validation between the GUI and the Core Engine.
- **Telemetry:** Automated performance logging to `stats.ghost`.
- **HWID Locking:** Advanced hardware-level security to prevent unauthorized license sharing.

---

## 🛠️ Installation & Setup

### 1. Requirements
- **Windows 10/11** (X64 Architecture)
- **Admin Privileges** (Required for hardware handshake and telemetry)
- **Stable Internet Connection** (For license validation via GhostSemi Core Protocol)

### 2. Deployment Instructions
To deploy the management console on your local machine:
1. Download the latest **GhostSemi_Setup_v2.6.exe** from the [Releases](https://github.com/GhostSemi/GhostSemi-Core/releases) section.
2. Run the installer. If Windows SmartScreen appears, select **"More Info"** > **"Run Anyway"**.
3. Launch the console and enter your **Alpha Key** to initialize the silicon core.

---

## 🧪 Development & Compilation
If you are contributing to the core engine or UI:
- **UI:** Developed with `CustomTkinter` (Python 3.14+).
- **Build Tool:** `PyInstaller` for binary executable generation.
- **Installer:** `Inno Setup` for secure distribution packaging.

---

## 🏁 Security Protocol
GhostSemi uses hardware-encrypted layers (HWID). If your Antivirus flags the binary, please add an exclusion to your installation folder. This is a common "false positive" caused by the obfuscation layer used to protect the GhostSemi Core Protocol.

**Current Stable Build:** v2.6-Stable  
**Auth:** Hardware Locked (HWID)