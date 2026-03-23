import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Logic to find FFmpeg whether running as a script or a bundled .app
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

FFMPEG_PATH = get_resource_path("bin/ffmpeg")
FFPROBE_PATH = get_resource_path("bin/ffprobe")

class PolyWavApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PolyWav Splitter Pro")
        self.geometry("600x450")
        
        # UI Elements
        self.label = ctk.CTkLabel(self, text="PolyWav to Mono Splitter", font=("Helvetica", 20, "bold"))
        self.label.pack(pady=20)

        # File Selection
        self.btn_select = ctk.CTkButton(self, text="Select PolyWav Files", command=self.select_files)
        self.btn_select.pack(pady=10)

        self.file_list_label = ctk.CTkLabel(self, text="No files selected", wraplength=500)
        self.file_list_label.pack(pady=5)

        # Options
        self.meta_var = tk.BooleanVar(value=True)
        self.check_meta = ctk.CTkCheckBox(self, text="Use iXML Track Names (if available)", variable=self.meta_var)
        self.check_meta.pack(pady=10)

        # Output Folder
        self.btn_dest = ctk.CTkButton(self, text="Select Output Folder", command=self.select_dest, fg_color="transparent", border_width=2)
        self.btn_dest.pack(pady=10)
        
        self.dest_label = ctk.CTkLabel(self, text="Default: Same as source", text_color="gray")
        self.dest_label.pack(pady=5)

        # Progress
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.btn_run = ctk.CTkButton(self, text="START CONVERSION", command=self.run_conversion, fg_color="green", hover_color="darkgreen")
        self.btn_run.pack(pady=20)

        self.files = []
        self.dest_folder = ""

    def select_files(self):
        self.files = filedialog.askopenfilenames(filetypes=[("Wav files", "*.wav")])
        if self.files:
            self.file_list_label.configure(text=f"{len(self.files)} files selected")

    def select_dest(self):
        self.dest_folder = filedialog.askdirectory()
        if self.dest_folder:
            self.dest_label.configure(text=self.dest_folder)

    def run_conversion(self):
        if not self.files:
            messagebox.showerror("Error", "Please select files first!")
            return

        total = len(self.files)
        for idx, f in enumerate(self.files):
            base_name = os.path.splitext(os.path.basename(f))[0]
            
            # Set up output directory
            parent_dir = self.dest_folder if self.dest_folder else os.path.dirname(f)
            out_dir = os.path.join(parent_dir, f"{base_name}_tracks")
            os.makedirs(out_dir, exist_ok=True)

            # Get channel count via FFprobe
            cmd_probe = [FFPROBE_PATH, "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=channels", "-of", "default=noprint_wrappers=1:nokey=1", f]
            channels = int(subprocess.check_output(cmd_probe).decode().strip())

            # Get Metadata if checked
            metadata = ""
            if self.meta_var.get():
                cmd_meta = [FFPROBE_PATH, "-v", "error", "-show_entries", "format", "-of", "default=noprint_wrappers=1", f]
                metadata = subprocess.check_output(cmd_meta).decode()

            for i in range(channels):
                track_num = f"{i+1:02d}"
                track_name = f"ch{i+1}"
                
                # Check for sTRK:NAME in metadata string
                search_str = f"sTRK:NAME_{track_num}="
                if search_str in metadata:
                    for line in metadata.split('\n'):
                        if search_str in line:
                            raw_name = line.split('=')[1].strip()
                            track_name = "".join([c if c.isalnum() or c in "-_" else "_" for c in raw_name])

                out_file = os.path.join(out_dir, f"{base_name}_{track_name}.wav")
                
                # Run FFmpeg split
                cmd_ffmpeg = [FFMPEG_PATH, "-i", f, "-map", "0:a:0", "-af", f"pan=mono|c0=c{i}", out_file, "-y"]
                subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            self.progress.set((idx + 1) / total)
            self.update_idletasks()

        messagebox.showinfo("Success", "Conversion Complete!")
        self.progress.set(0)

if __name__ == "__main__":
    app = PolyWavApp()
    app.mainloop()