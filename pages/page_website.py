import tkinter as tk
from tkinter import ttk # Import ttk for the modern widgets like Progressbar
import threading # Import threading to prevent the GUI from freezing
from website_setup import setup_website

class PageWebsite:
    def __init__(self, app):
        self.app = app
        # Initialize the spinner and button variables to None
        self.spinner = None
        self.setup_button = None
        self.result_label = None

    def start_setup_thread(self):
        """Starts the setup_site task in a separate thread."""
        
        # 1. Disable the button and clear the result label
        self.setup_button.config(state=tk.DISABLED)
        self.result_label.config(text="")
        
        # 2. Start the spinner animation
        self.spinner.pack(pady=10)
        self.spinner.start(10) # Start the indeterminate animation (10ms steps)

        # 3. Start the heavy task in a new thread
        self.thread = threading.Thread(target=self._run_setup_task, daemon=True)
        self.thread.start()

    def _run_setup_task(self):
        """The function that runs in the separate thread."""
        htdocs = self.app.state.get("htdocs_dir", "")
        # Call the time-consuming website setup function
        success = setup_website(htdocs)
        
        # Once complete, use after() to safely update the GUI from the main thread
        self.app.root.after(0, self._complete_setup, success)

    def _complete_setup(self, success):
        """Updates the GUI once the setup thread is complete."""
        
        # 1. Stop and hide the spinner
        self.spinner.stop()
        self.spinner.pack_forget() 
        
        # 2. Update the result label
        self.result_label.config(
            text="✅ Website created successfully!" if success else "❌ Failed to set up website.",
            fg="green" if success else "red"
        )
        
        # 3. Re-enable the button
        self.setup_button.config(state=tk.NORMAL)

    def render(self, root):
        tk.Label(root, text="Step 3: Setup Website", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(
            root,
            text="This will download and extract an website package to your htdocs directory.",
            wraplength=520
        ).pack(pady=10)
        tk.Label(root, text="optimize the process", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(
            root,
            text="Turn off any Vpn or dns to improve speed. watch the progress in real time in terminal",
            wraplength=520
        ).pack(pady=10)
        
        # Store the button reference
        self.setup_button = tk.Button(
            root, 
            text="🛠 Setup Website (Download & Extract)", 
            command=self.start_setup_thread # Call the thread starter
        )
        self.setup_button.pack(pady=10)
        
        # Create and store the spinner (but don't pack it yet)
        self.spinner = ttk.Progressbar(
            root, 
            orient="horizontal", 
            length=200, 
            mode="indeterminate" # Indeterminate mode creates the 'spinner' effect
        )
        # Note: We use pack_forget/pack to show/hide the spinner.

        # Store the result label reference
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=5)

        tk.Button(root, text="⬅️ Back", command=self.app.prev_page).place(x=200, y=330)
        tk.Button(root, text="Next ➡️", command=self.app.next_page).place(x=350, y=330)