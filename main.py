import cv2
import os
import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TimelapseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timelapse Capture")
        
        # Variables
        self.webcam_index = tk.IntVar(value=0)
        self.capture_interval = tk.IntVar(value=10)
        self.output_dir = tk.StringVar(value="timelapse")
        self.is_running = False

        # Create GUI elements
        self.create_widgets()
        
        # Capture thread
        self.capture_thread = None

    def create_widgets(self):
        # Webcam index
        tk.Label(self.root, text="Webcam Index:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.webcam_index).grid(row=0, column=1, padx=10, pady=5)

        # Capture interval
        tk.Label(self.root, text="Capture Interval (s):").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.capture_interval).grid(row=1, column=1, padx=10, pady=5)

        # Output directory
        tk.Label(self.root, text="Output Folder:").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.output_dir).grid(row=2, column=1, padx=10, pady=5)

        # Start and Stop buttons
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_capture)
        self.start_button.grid(row=3, column=0, padx=10, pady=10)
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_capture, state=tk.DISABLED)
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)

        # Status message
        self.status_label = tk.Label(self.root, text="Stopped", fg="red")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def create_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def capture_images(self):
        self.create_directory(self.output_dir.get())
        cap = cv2.VideoCapture(self.webcam_index.get())
        
        if not cap.isOpened():
            messagebox.showerror("Error", f"Could not open webcam with index {self.webcam_index.get()}.")
            self.stop_capture()
            return

        count = 0
        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image")
                self.stop_capture()
                break

            img_name = os.path.join(self.output_dir.get(), f"frame_{count:04d}.jpg")
            cv2.imwrite(img_name, frame)
            print(f"Saved {img_name}")

            count += 1
            time.sleep(self.capture_interval.get())

        cap.release()

    def start_capture(self):
        if self.is_running:
            return

        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Running", fg="green")
        
        self.capture_thread = threading.Thread(target=self.capture_images)
        self.capture_thread.start()

    def stop_capture(self):
        if not self.is_running:
            return

        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Stopped", fg="red")

        if self.capture_thread is not None:
            self.capture_thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimelapseApp(root)
    root.mainloop()
