import tkinter as tk
import webbrowser

class PageXampp:
    def __init__(self, app):
        self.app = app

    def open_download(self):
        webbrowser.open("https://www.apachefriends.org/download.html")

    def render(self, root):
        tk.Label(root, text="Step 1: Install XAMPP", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(root, text="If you haven’t installed XAMPP yet, click below to download it.\nAfter installing, open the XAMPP Control Panel and start Apache and MySQL.", wraplength=520).pack(pady=10)
        tk.Button(root, text="🌐 Open XAMPP Download Page", command=self.open_download).pack(pady=10)
        tk.Label(root, text="Once done, click Next to continue.", fg="green").pack(pady=5)
        tk.Button(root, text="⬅️ Back", command=self.app.prev_page).place(x=200, y=330)
        tk.Button(root, text="Next ➡️", command=self.app.next_page).place(x=350, y=330)
