import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import os
import threading
import re

#layout
window = tk.Tk()
window.title("YT2BRZO")
window.geometry("450x350")

url_label = tk.Label(window, text="PASTE THAT HOE")
url_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

url_entry = tk.Entry(window, width=60)
url_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

def on_download():
    url = url_entry.get()
    mode = mode_var.get()
    container = container_var.get().lower()
    quality = quality_var.get()
    output_path = os.path.join(folder_var.get() if folder_var.get() != "Same as script??" else ".", "%(title)s.%(ext)s")

    if url == "":
        print("READ THE DAMN TEXT")
        return
    
    print(f"checking your order, hold up")

    if mode == "The Ocky Way (A)":
        if quality == "Best":
            format_str = "bestaudio"
        else:
            format_str = "bestaudio"
    elif mode == "Staring contest (V)":
        if quality == "Best":
            format_str = "bestvideo"
        elif quality == "1080p":
            format_str = "bestvideo[height<=1080]"
        elif quality == "720p":
            format_str = "bestvideo[height<=720]"
        elif quality == "480p":
            format_str = "bestvideo[height<=480]"
    else:
        if quality == "Best":
            format_str = "bestvideo+bestaudio"
        elif quality == "1080p":
            format_str = "bestvideo[height<=1080]+bestaudio"
        elif quality == "720p":
            format_str = "bestvideo[height<=720]+bestaudio"
        elif quality == "480p":
            format_str = "bestvideo[height<=480]+bestaudio"

    
    if mode == "The Ocky Way (A)":
        command = [
            "yt-dlp",
            "-f", format_str,
            "--extract-audio",
            "--audio-format", container,
            "-o", output_path,
            url
        ]
    else:
        command = [
            "yt-dlp",
            "-f", format_str,
            "--merge-output-format", container,
            "-o", output_path,
            url
        ]

    print(f"lemme grab that rq, {url}, right?\nActually dont answer that. I do what I want, fuck you\nand just so yk im running {command}\n any issues? if so, it ur fault dickhead")    
    
    def run_download():
        progress_var.set(0)
        progress_label.config(text="imma grab that rq...")
        download_btn.config(state="disabled")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            print(line, end="")
            match = re.search(r"(\d+\.\d+)%", line)
            if match:
                percent = float(match.group(1))
                progress_var.set(percent)
                progress_label.config(text=f"{percent:.1f}%")

        process.wait()
        progress_var.set(100)
        progress_label.config(text="ok pull up hoe")
        download_btn.config(state="normal")
    
    thread = threading.Thread(target=run_download)
    thread.start()

    print('OK pull up hoe')

def on_mode_change(event):
    if mode_var.get() == "The Ocky Way (A)":
        container_dropdown["values"] = ("MP3", "M4A", "OPUS", "WAV")
        container_dropdown.current(0)
        quality_dropdown["values"] = ("Best", "320k", "192k", "128k")
        quality_dropdown.current(0)
    else:
        container_dropdown["values"] = ("MKV", "MP4")
        container_dropdown.current(0)
        quality_dropdown["values"] = ("Best", "1080p", "720p", "480p")
        quality_dropdown.current(0)

def pick_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

#inputs
download_btn = tk.Button(window, text="Download type shi", command=on_download)
download_btn.grid(row=2, column=0, columnspan=2, pady=10)


mode_label = tk.Label(window, text="How you want it?")
mode_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")

mode_var = tk.StringVar()
mode_dropdown = ttk.Combobox(window, textvariable=mode_var, state="readonly", width=20)
mode_dropdown["values"] = ("Reg (A+V)", "The Ocky Way (A)", "Staring contest (V)")
mode_dropdown.current(0)
mode_dropdown.grid(row=3, column=1, padx=10, pady=(10,0), sticky="w")
mode_dropdown.bind("<<ComboboxSelected>>", on_mode_change)


container_label = tk.Label(window, text="Container:")
container_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="e")

container_var = tk.StringVar()
container_dropdown = ttk.Combobox(window, textvariable=container_var, state="readonly", width=20)
container_dropdown["values"] = ("MKV", "MP4")
container_dropdown.current(0)
container_dropdown.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="w")


quality_label = tk.Label(window, text="Quality:")
quality_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="e")

quality_var = tk.StringVar()
quality_dropdown = ttk.Combobox(window, textvariable=quality_var, state="readonly", width=20)
quality_dropdown["values"] = ("Best", "1080p", "720p", "480p")
quality_dropdown.current(0)
quality_dropdown.grid(row=5, column=1, padx=10, pady=(10, 0), sticky="w")


folder_label = tk.Label(window, text="Im putting it there --->")
folder_label.grid(row=6, column=0, padx=5, pady=(10, 0), sticky="e")

folder_var = tk.StringVar()
folder_var.set("Same as script??")

folder_display = tk.Label(window, textvariable=folder_var, width=30, anchor='w')
folder_display.grid(row=6, column=1, padx=5, pady=(10, 0), sticky="w")

folder_btn = tk.Button(window, text="I have a better place", command=pick_folder)
folder_btn.grid(row=6, column=1, padx=110, pady=(10, 0), sticky="w")


progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=100, length=300)
progress_bar.grid(row=8, column=0, columnspan=2, pady=(15,0))

progress_label = tk.Label(window, text="waiting on u big guy")
progress_label.grid(row=9, column=0, columnspan=2, pady=(5, 0))

window.mainloop()