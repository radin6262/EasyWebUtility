import tkinter as tk
import webbrowser

class PageDone:
    def __init__(self, app):
        self.app = app

    def open_localhost(self):
        webbrowser.open("http://localhost")

    def render(self, root):
        tk.Label(root, text="🎉 Setup Complete!", font=("Arial", 16, "bold")).pack(pady=30)
        tk.Label(root, text="You can now open your browser and visit:\nhttp://localhost\n\nYour example website should be visible!", wraplength=520).pack(pady=10)
        tk.Button(root, text="🌐 Open Localhost", command=self.open_localhost).pack(pady=10)
        tk.Button(root, text="⬅️ Back", command=self.app.prev_page).place(x=250, y=330)
        tk.Button(root, text="Finish", command=self.app.root.destroy).place(x=360, y=330)
