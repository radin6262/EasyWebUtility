import tkinter as tk
from tkinter import filedialog

class PageHtdocs:
    def __init__(self, app):
        self.app = app

    def choose_dir(self):
        folder = filedialog.askdirectory(title="Select XAMPP htdocs Folder")
        if folder:
            self.app.state["htdocs_dir"] = folder
            self.label_var.set(f"Selected: {folder}")

    def render(self, root):
        tk.Label(root, text="Step 2: Select your XAMPP htdocs directory", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(root, text="Choose the folder where your websites are stored.\nUsually: C:\\xampp\\htdocs", wraplength=520).pack(pady=10)
        self.label_var = tk.StringVar(value="No folder selected yet.")
        tk.Label(root, textvariable=self.label_var, fg="blue").pack(pady=10)
        tk.Button(root, text="📁 Choose Folder", command=self.choose_dir).pack(pady=10)
        tk.Button(root, text="⬅️ Back", command=self.app.prev_page).place(x=200, y=330)
        tk.Button(root, text="Next ➡️", command=self.app.next_page).place(x=350, y=330)
