import tkinter as tk
from pages.page_welcome import PageWelcome
from pages.page_xampp import PageXampp
from pages.page_htdocs import PageHtdocs
from pages.page_website import PageWebsite
from pages.page_done import PageDone

class InstallerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Server Installer Wizard")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.current_page_index = 0
        self.pages = []
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Shared state
        self.state = {"htdocs_dir": ""}

        # Initialize pages
        self.pages = [
            PageWelcome(self),
            PageXampp(self),
            PageHtdocs(self),
            PageWebsite(self),
            PageDone(self)
        ]

        self.show_page(0)

    def show_page(self, index):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.current_page_index = index
        page = self.pages[index]
        page.render(self.container)

    def next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.show_page(self.current_page_index + 1)

    def prev_page(self):
        if self.current_page_index > 0:
            self.show_page(self.current_page_index - 1)

    def run(self):
        self.root.mainloop()
