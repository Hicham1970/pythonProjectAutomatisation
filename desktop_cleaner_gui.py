import logging
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from desktop_cleaner_bot import OrganizerConfig, organize, setup_logging


class TextHandler(logging.Handler):
    """Custom logging handler to redirect logs to a text widget."""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)


class DesktopCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Cleaner Bot - GUI")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables for storing paths and settings
        self.source_dir = tk.StringVar()
        self.music_dir = tk.StringVar()
        self.sfx_dir = tk.StringVar()
        self.video_dir = tk.StringVar()
        self.image_dir = tk.StringVar()
        self.docs_dir = tk.StringVar()
        self.sfx_size_mb = tk.DoubleVar(value=10.0)
        self.dry_run = tk.BooleanVar(value=True)
        self.log_level = tk.StringVar(value="INFO")
        
        self.setup_ui()
        self.setup_logging()
        
    def setup_ui(self):
        # Create main frame with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Desktop Cleaner Bot", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Directory selection frame
        dir_frame = ttk.LabelFrame(main_frame, text="Directory Configuration", padding=10)
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Source directory
        self.create_directory_row(dir_frame, "Source Directory:", self.source_dir, 0)
        
        # Destination directories
        self.create_directory_row(dir_frame, "Music Directory:", self.music_dir, 1)
        self.create_directory_row(dir_frame, "SFX Directory:", self.sfx_dir, 2)
        self.create_directory_row(dir_frame, "Video Directory:", self.video_dir, 3)
        self.create_directory_row(dir_frame, "Image Directory:", self.image_dir, 4)
        self.create_directory_row(dir_frame, "Documents Directory:", self.docs_dir, 5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # SFX size threshold
        sfx_frame = ttk.Frame(settings_frame)
        sfx_frame.pack(fill=tk.X, pady=2)
        ttk.Label(sfx_frame, text="SFX Size Threshold (MB):").pack(side=tk.LEFT)
        sfx_spinbox = ttk.Spinbox(sfx_frame, from_=1, to=100, width=10, 
                                 textvariable=self.sfx_size_mb, increment=1)
        sfx_spinbox.pack(side=tk.RIGHT)
        
        # Log level
        log_frame = ttk.Frame(settings_frame)
        log_frame.pack(fill=tk.X, pady=2)
        ttk.Label(log_frame, text="Log Level:").pack(side=tk.LEFT)
        log_combo = ttk.Combobox(log_frame, textvariable=self.log_level, 
                                values=["DEBUG", "INFO", "WARNING", "ERROR"], 
                                state="readonly", width=10)
        log_combo.pack(side=tk.RIGHT)
        
        # Dry run checkbox
        dry_run_check = ttk.Checkbutton(settings_frame, text="Dry Run (Preview only - don't move files)", 
                                       variable=self.dry_run)
        dry_run_check.pack(anchor=tk.W, pady=2)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Organize button
        self.organize_btn = ttk.Button(button_frame, text="🗂️ Organize Files", 
                                      command=self.start_organization, style="Accent.TButton")
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear log button
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear Log", 
                              command=self.clear_log)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Load defaults button
        defaults_btn = ttk.Button(button_frame, text="📁 Load Defaults", 
                                 command=self.load_defaults)
        defaults_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Log output frame
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log text widget with scrollbar
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, state='disabled',
                                                 wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def create_directory_row(self, parent, label_text, var, row):
        """Create a row with label, entry, and browse button for directory selection."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        label = ttk.Label(frame, text=label_text, width=20)
        label.pack(side=tk.LEFT)
        
        entry = ttk.Entry(frame, textvariable=var, width=50)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        browse_btn = ttk.Button(frame, text="Browse", width=8,
                               command=lambda: self.browse_directory(var))
        browse_btn.pack(side=tk.RIGHT)
        
    def browse_directory(self, var):
        """Open directory selection dialog."""
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            var.set(directory)
            
    def load_defaults(self):
        """Load default directory paths."""
        import os
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Set default paths
        self.source_dir.set(desktop)
        self.music_dir.set(os.path.join(desktop, "Organized", "Music"))
        self.sfx_dir.set(os.path.join(desktop, "Organized", "SFX"))
        self.video_dir.set(os.path.join(desktop, "Organized", "Videos"))
        self.image_dir.set(os.path.join(desktop, "Organized", "Images"))
        self.docs_dir.set(os.path.join(desktop, "Organized", "Documents"))
        
        self.status_var.set("Default paths loaded")
        
    def setup_logging(self):
        """Setup logging to redirect to the text widget."""
        # Clear any existing handlers
        logging.getLogger().handlers.clear()
        
        # Create text handler
        self.text_handler = TextHandler(self.log_text)
        self.text_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        
        # Add handler to root logger
        logging.getLogger().addHandler(self.text_handler)
        logging.getLogger().setLevel(logging.DEBUG)
        
    def clear_log(self):
        """Clear the log text widget."""
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        self.status_var.set("Log cleared")
        
    def validate_inputs(self):
        """Validate all required inputs."""
        if not self.source_dir.get().strip():
            messagebox.showerror("Error", "Please select a source directory")
            return False
            
        if not self.music_dir.get().strip():
            messagebox.showerror("Error", "Please select a music directory")
            return False
            
        if not self.sfx_dir.get().strip():
            messagebox.showerror("Error", "Please select an SFX directory")
            return False
            
        if not self.video_dir.get().strip():
            messagebox.showerror("Error", "Please select a video directory")
            return False
            
        if not self.image_dir.get().strip():
            messagebox.showerror("Error", "Please select an image directory")
            return False
            
        if not self.docs_dir.get().strip():
            messagebox.showerror("Error", "Please select a documents directory")
            return False
            
        if not os.path.isdir(self.source_dir.get()):
            messagebox.showerror("Error", "Source directory does not exist")
            return False
            
        return True
        
    def start_organization(self):
        """Start the file organization process in a separate thread."""
        if not self.validate_inputs():
            return
            
        # Disable the organize button
        self.organize_btn.configure(state='disabled')
        self.progress.start()
        self.status_var.set("Organizing files...")
        
        # Start organization in a separate thread
        thread = threading.Thread(target=self.run_organization)
        thread.daemon = True
        thread.start()
        
    def run_organization(self):
        """Run the organization process."""
        try:
            # Update logging level
            setup_logging(self.log_level.get())
            
            # Create configuration
            config = OrganizerConfig(
                source_dir=self.source_dir.get(),
                dest_dir_music=self.music_dir.get(),
                dest_dir_sfx=self.sfx_dir.get(),
                dest_dir_video=self.video_dir.get(),
                dest_dir_image=self.image_dir.get(),
                dest_dir_documents=self.docs_dir.get(),
                sfx_size_threshold=int(self.sfx_size_mb.get() * 1024 * 1024),
                dry_run=self.dry_run.get()
            )
            
            # Log the configuration
            logging.info("Starting file organization with configuration:")
            logging.info(f"Source: {config.source_dir}")
            logging.info(f"Music: {config.dest_dir_music}")
            logging.info(f"SFX: {config.dest_dir_sfx}")
            logging.info(f"Video: {config.dest_dir_video}")
            logging.info(f"Images: {config.dest_dir_image}")
            logging.info(f"Documents: {config.dest_dir_documents}")
            logging.info(f"SFX Threshold: {self.sfx_size_mb.get()} MB")
            logging.info(f"Dry Run: {config.dry_run}")
            
            # Run organization
            organize(config)
            
            # Show completion message
            mode = "Preview completed" if config.dry_run else "Organization completed"
            self.root.after(0, lambda: self.organization_completed(mode))
            
        except Exception as e:
            error_msg = f"Error during organization: {str(e)}"
            logging.error(error_msg)
            self.root.after(0, lambda: self.organization_error(error_msg))
            
    def organization_completed(self, message):
        """Called when organization is completed successfully."""
        self.progress.stop()
        self.organize_btn.configure(state='normal')
        self.status_var.set(message)
        messagebox.showinfo("Success", message)
        
    def organization_error(self, error_msg):
        """Called when organization encounters an error."""
        self.progress.stop()
        self.organize_btn.configure(state='normal')
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", error_msg)


def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    
    # Create and run the application
    app = DesktopCleanerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()