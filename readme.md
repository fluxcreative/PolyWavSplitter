# 🎧 PolyWav Splitter Pro (macOS)

A professional batch-processing utility to split multi-track (polyphonic) WAV files into individual mono tracks. Optimized for location sound recordists and live engineers using hardware like **Sound Devices (MixPre/8-Series)**, **Zoom**, or **Scorpio**.

## Two Ways to Use

### Option A: Standalone Application (Non-Technical)
**Perfect for:** Immediate use without installing any code.
1. Download `PolyWavSplitter.zip` from the **Releases** section.
2. Unzip and move `PolyWavSplitter.app` to your Applications folder.
3. **Important:** Because this is an unsigned indie app, **Right-Click** the app and select **Open** the first time you run it.
4. Select your files, choose your settings, and hit **Start**.

### Option B: Python Script (Developers)
**Perfect for:** Customizing the logic or auditing the code.
1. Clone this repository.
2. Install the GUI library: `pip install customtkinter`.
3. Ensure **FFmpeg** and **FFprobe** are installed on your system (or placed in a `/bin` folder within the project).
4. Run via terminal: `python3 main.py`.

---

## ✨ Key Features
* **Batch Conversion:** Process dozens of PolyWavs simultaneously.
* **iXML Metadata Support:** Automatically names tracks based on your soundboard labels (e.g., *Kick, Snare, Vocal*) rather than just *Track 1, Track 2*.
* **Intelligent Organization:** Automatically creates a sub-folder for every PolyWav to keep your exports organized.
* **Modern UI:** Supports macOS Light and Dark modes.

---

## 🛠 Built With
* **Python** & **CustomTkinter** - For the modern, responsive interface.
* **FFmpeg** - The engine used for high-fidelity audio splitting.
* **PyInstaller** - Used to bundle the standalone macOS application.

---

## 📄 License
This project is open-source. Feel free to use, modify, and share.