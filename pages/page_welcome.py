import tkinter as tk

class PageWelcome:
    def __init__(self, app):
        self.app = app

    def render(self, root):
        tk.Label(root, text="Welcome to the Web Server Setup Wizard", font=("Arial", 16, "bold")).pack(pady=30)
        tk.Label(root, text="This wizard will guide you to install and configure a local web server using XAMPP.\n\nClick Next to continue.", wraplength=500).pack(pady=10)
        tk.Button(root, text="Next ➡️", command=self.app.next_page).pack(pady=20)
