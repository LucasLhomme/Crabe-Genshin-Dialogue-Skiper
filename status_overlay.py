"""Module managing the status display overlay on top of the game window."""

import os
import tkinter as tk
import tkinter.font as tkFont
from threading import Thread
from time import sleep
from ctypes import windll, byref, create_unicode_buffer
from constants import STATUS_RUN, STATUS_PAUSE, STATUS_EXIT, KEY_START, KEY_PAUSE, KEY_EXIT

# Constants for Windows API
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20

def load_windows_font(font_path, private=True, enumerable=False):
    """
    Loads a font into Windows and makes it available for the application.
    
    Args:
        font_path: Path to the font file (.ttf, .otf, etc.)
        private: If True, the font is private to the current process
        enumerable: If True, the font appears in font enumeration
        
    Returns:
        bool: True if the font was successfully loaded
    """
    try:
        # Adapt code for Python 3
        path_buffer = create_unicode_buffer(font_path)
        add_font_resource_ex = windll.gdi32.AddFontResourceExW
        
        # Define loading options
        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        
        # Add font to the system
        fonts_added = add_font_resource_ex(byref(path_buffer), flags, 0)
        if fonts_added > 0:
            return True
        else:
            print(f"Failed to load font: {font_path}")
            return False
    except Exception as e:
        print(f"Error loading font: {e}")
        return False
        
def get_font_family_name(before_families=None):
    """
    Determines the name of the newly loaded font family.
    
    Args:
        before_families: List of font families before loading
        
    Returns:
        str: Font family name or None if not found
    """
    # Get all available font families
    all_families = list(tkFont.families())
    
    # If we have the before list, find new fonts
    if before_families:
        new_families = [f for f in all_families if f not in before_families]
        if new_families:
            print(f"New fonts detected: {new_families}")
            return new_families[0]  # Take the first new font
    
    # Look for a font that might be ours
    # (approximate search based on name)
    possible_names = ["HYWenHei", "WenHei", "Wen", "85W"]
    for family in all_families:
        for name in possible_names:
            if name.lower() in family.lower():
                print(f"Font found by name: {family}")
                return family
    
    return None


class StatusOverlay:
    """Floating window displaying the current status of the program."""
    
    def __init__(self):
        """Initializes the status display window."""
        self.root = None
        self.status_label = None
        self.title_label = None  # New label for the title
        self.overlay_visible = False
        self.current_status = STATUS_PAUSE
        
        # Variables for fading
        self.fade_after_id = None
        self.fade_steps = 20  # Number of steps for fading
        self.fade_step_time = 50  # Milliseconds between each step
        self.is_fading = False
        
        self.font_loaded = False
        self.font_family = "@HYWenHei-85W"  # Direct name with @ for Chinese fonts
        
        self.thread = Thread(target=self._create_window, daemon=True)
        self.thread.start()
    
    def _create_window(self):
        """Creates the floating window."""
        temp_root = tk.Tk()
        temp_root.withdraw()
        before_families = list(tkFont.families())
        
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                'assets', 'fonts', 'HYWenHei-85W.ttf'))
        if os.path.exists(font_path):
            print(f"Attempting to load font: {font_path}")
            self.font_loaded = load_windows_font(font_path)
            
            if self.font_loaded:
                sleep(0.5)                
                detected_family = get_font_family_name(before_families)
                if detected_family:
                    self.font_family = detected_family
                
                print(f"Font family identified: {self.font_family}")
                
                all_families = list(tkFont.families())
        else:
            print(f"ERROR: Font file not found: {font_path}")
            
        temp_root.destroy()
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("")  # No title
        
        # Configure the window to be always on top and borderless
        self.root.attributes("-topmost", True)  # Always on top
        self.root.attributes("-alpha", 1.0)     # Full opacity at start
        self.root.overrideredirect(True)        # No border or title bar
        
        # Black background color
        self.root.configure(bg="black")
        
        # Make black background transparent
        self.root.wm_attributes("-transparentcolor", "black")
        
        font_options = [
            self.font_family,
            "@HYWenHei-85W",
            "@HYWenHei",
            "HYWenHei-85W",
            "HYWenHei",
            "Arial"  # Fallback
        ]
        
        font_size = 12
        font_weight = "bold"
        font_name = "Arial"  # Default value
        
        for font_option in font_options:
            try:
                test_label = tk.Label(self.root, text="Test", font=(font_option, font_size, font_weight))
                print(f"Valid font found: {font_option}")
                font_name = font_option
                test_label.destroy()
                break
            except Exception as e:
                print(f"Failed with font {font_option}: {e}")
        
        print(f"Using font: {font_name}")
        
        # Create window for title in top right corner
        self.title_window = tk.Toplevel(self.root)
        self.title_window.title("")
        self.title_window.attributes("-topmost", True)
        self.title_window.attributes("-alpha", 1.0)
        self.title_window.overrideredirect(True)
        self.title_window.configure(bg="black")
        self.title_window.wm_attributes("-transparentcolor", "black")
        
        # Position in top right corner
        screen_width = self.root.winfo_screenwidth()
        title_width = 150
        title_height = 15
        self.title_window.geometry(f"{title_width}x{title_height}+{screen_width - title_width - 10}+10")
        
        # Create title label
        try:
            self.title_label = tk.Label(
                self.title_window, 
                text="Crabe Skipper...", 
                fg="#F08080",  # Light coral color
                bg="black",
                font=(font_name, font_size-1, font_weight),  # Slightly smaller font
                anchor="e"  # Right-aligned
            )
            self.title_label.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error creating title label: {e}")
        
        # Position in the middle left of the screen for status
        screen_height = self.root.winfo_screenheight()
        window_width = 150
        window_height = 30
        x_position = 10  # Left position with 10 pixels margin
        y_position = (screen_height - window_height) // 2  # Vertically centered
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # Create label to display status
        try:
            self.status_label = tk.Label(
                self.root, 
                text="PAUSED", 
                fg="yellow", 
                bg="black",
                font=(font_name, font_size, font_weight)
            )
        except Exception as e:
            print(f"Error creating label: {e}")
            self.status_label = tk.Label(
                self.root, 
                text="PAUSED", 
                fg="yellow", 
                bg="black",
                font=("Arial", font_size, font_weight)
            )
            
        self.status_label.pack(fill="both", expand=True)
        
        # Create event handler for moving the status window
        self.root.bind("<Button-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._on_drag)
        
        # Create event handler for moving the title window
        self.title_window.bind("<Button-1>", lambda event: self._start_drag_title(event))
        self.title_window.bind("<B1-Motion>", lambda event: self._on_drag_title(event))
        
        self.overlay_visible = True
        
        # Trigger fading after 2 seconds
        self._schedule_fade()
        
        self.root.mainloop()
    
    def _start_drag_title(self, event):
        """Prepares moving the title window."""
        self._drag_title_x = event.x
        self._drag_title_y = event.y
        
        # Cancel fading and make windows fully visible during movement
        self._cancel_fade()
        if self.title_window:
            self.title_window.attributes("-alpha", 1.0)
            
        # Reactivate fading after movement
        self._schedule_fade()
    
    def _on_drag_title(self, event):
        """Moves the title window during drag-and-drop."""
        if not self.title_window:
            return
            
        x = self.title_window.winfo_x() - self._drag_title_x + event.x
        y = self.title_window.winfo_y() - self._drag_title_y + event.y
        self.title_window.geometry(f"+{x}+{y}")
    
    def _schedule_fade(self):
        """Schedules the progressive disappearance of the overlay."""
        # Cancel any previous ongoing fading
        self._cancel_fade()
        
        # Ensure overlays are visible
        if self.root:
            self.root.attributes("-alpha", 1.0)
        if hasattr(self, 'title_window') and self.title_window:
            self.title_window.attributes("-alpha", 1.0)
            
        # Schedule fading after 2 seconds
        if self.root:
            self.fade_after_id = self.root.after(2000, self._start_fade_out)
    
    def _cancel_fade(self):
        """Cancels any ongoing fading."""
        if self.fade_after_id and self.root:
            self.root.after_cancel(self.fade_after_id)
            self.fade_after_id = None
        self.is_fading = False
    
    def _start_fade_out(self):
        """Starts the progressive fading."""
        if self.root:
            self.is_fading = True
            self._fade_step(1.0)
    
    def _fade_step(self, current_alpha):
        """
        Executes one step of fading.
        
        Args:
            current_alpha: Current opacity level (from 1.0 to 0.0)
        """
        if not self.root or not self.is_fading:
            return
            
        # Calculate new opacity
        new_alpha = max(0.0, current_alpha - (1.0 / self.fade_steps))
        
        # Apply new opacity to both windows
        self.root.attributes("-alpha", new_alpha)
        
        if hasattr(self, 'title_window') and self.title_window:
            self.title_window.attributes("-alpha", new_alpha)
        
        # Continue fading if necessary
        if new_alpha > 0 and self.is_fading:
            self.fade_after_id = self.root.after(
                self.fade_step_time, 
                lambda: self._fade_step(new_alpha)
            )
        else:
            self.is_fading = False
    
    def _start_drag(self, event):
        """Prepares moving the window."""
        self._drag_x = event.x
        self._drag_y = event.y
        
        # Cancel fading and make window fully visible during movement
        self._cancel_fade()
        if self.root:
            self.root.attributes("-alpha", 1.0)
        if hasattr(self, 'title_window') and self.title_window:
            self.title_window.attributes("-alpha", 1.0)
            
        # Reactivate fading after movement
        self._schedule_fade()
    
    def _on_drag(self, event):
        """Moves the window during drag-and-drop."""
        x = self.root.winfo_x() - self._drag_x + event.x
        y = self.root.winfo_y() - self._drag_y + event.y
        self.root.geometry(f"+{x}+{y}")
    
    def update_status(self, status):
        """Updates the status displayed on the window."""
        self.current_status = status
        
        # Check that the window is created and functional
        if not self.overlay_visible or not self.root:
            return
        
        # Update text and color based on status
        if status == STATUS_RUN:
            text = "ACTIVE"
            color = "lime green"
        elif status == STATUS_PAUSE:
            text = "PAUSED"
            color = "yellow"
        elif status == STATUS_EXIT:
            text = "CLOSING..."
            color = "red"
        else:
            text = "UNKNOWN STATUS"
            color = "white"
        
        # Use after() to modify the interface from the tkinter main thread
        if self.root:
            self.root.after(0, lambda: self._update_label_safely(text, color))
            
        # Ensure overlays are visible and schedule fading
        if self.root:
            self.root.attributes("-alpha", 1.0)
        if hasattr(self, 'title_window') and self.title_window:
            self.title_window.attributes("-alpha", 1.0)
        self._schedule_fade()
    
    def _update_label_safely(self, text, color):
        """Updates the status label in a thread-safe way."""
        try:
            if self.status_label:
                self.status_label.config(text=text, fg=color)
        except tk.TclError:
            # The window may have been closed
            pass
    
    def show_keybindings(self):
        """Displays keyboard shortcuts in the center of the screen for 3 seconds."""
        # Cancel any previous display
        if hasattr(self, 'help_window') and self.help_window:
            try:
                self.help_window.destroy()
            except:
                pass
        
        # Create a new window for help
        self.help_window = tk.Toplevel()
        self.help_window.title("")
        self.help_window.attributes("-topmost", True)
        self.help_window.overrideredirect(True)
        self.help_window.configure(bg="black")
        
        # Position in center of screen
        screen_width = self.help_window.winfo_screenwidth()
        screen_height = self.help_window.winfo_screenheight()
        window_width = 300
        window_height = 200
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.help_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # Add a frame with border
        frame = tk.Frame(self.help_window, bg="black", borderwidth=2, relief="solid")
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add title
        title_label = tk.Label(
            frame,
            text="KEYBOARD SHORTCUTS",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="black"
        )
        title_label.pack(pady=(10, 5))
        
        # Add shortcuts
        help_text = f"""F8 — Start
F9 — Pause
F12 — Exit
² — Show this help"""
        
        help_label = tk.Label(
            frame,
            text=help_text,
            justify="left",
            font=("Arial", 10),
            fg="#CCCCCC",
            bg="black"
        )
        help_label.pack(pady=5)
        
        # Close after 3 seconds
        self.help_window.after(3000, lambda: self._close_help_window())
    
    def _close_help_window(self):
        """Closes the help window if it exists."""
        if hasattr(self, 'help_window') and self.help_window:
            try:
                self.help_window.destroy()
                self.help_window = None
            except:
                pass
    
    def close(self):
        """Closes the display windows."""
        try:
            self._cancel_fade()
            if hasattr(self, 'help_window') and self.help_window:
                self.help_window.destroy()
            if self.root:
                self.root.destroy()
            if hasattr(self, 'title_window') and self.title_window:
                self.title_window.destroy()
            self.overlay_visible = False
        except tk.TclError:
            # Windows may have already been closed
            pass