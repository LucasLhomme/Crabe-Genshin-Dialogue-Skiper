"""Module managing the automatic skipping of dialogues in Genshin Impact."""

import sys
from random import randint, uniform
from typing import Tuple, Union
from time import perf_counter, sleep

from pyautogui import click, getActiveWindowTitle, pixel
from pynput.mouse import Controller # type: ignore
from pynput.keyboard import Key, KeyCode # type: ignore
import win32gui # type: ignore
import win32con # type: ignore

from constants import (COLOR_AUTOPLAY_ICON, COLOR_WHITE, 
                     STATUS_RUN, STATUS_PAUSE, STATUS_EXIT,
                     KEY_START, KEY_PAUSE, KEY_EXIT, KEY_HELP)
from status_overlay import StatusOverlay

class DialogueSkipper:
    """Main class managing dialogue skipping in Genshin Impact."""
    
    def __init__(self, screen_setup):
        """Initializes the dialogue skipper with the specified screen configuration."""
        self.screen = screen_setup
        self.status = STATUS_PAUSE
        self.mouse = Controller()
        self.last_reposition = 0.0
        self.time_between_repositions = self.random_interval() * 40
        
        # Create the status overlay
        self.status_overlay = StatusOverlay()
    
    def random_interval(self) -> float:
        """Returns a random interval between 0.12 and 0.2 seconds."""
        return uniform(0.18, 0.2) if randint(1, 6) == 6 else uniform(0.12, 0.18)
    
    def random_cursor_position(self) -> Tuple[int, int]:
        """Moves the cursor to a random position within the dialogue area."""
        x = randint(self.screen.bottom_dialogue_min_x, self.screen.bottom_dialogue_max_x)
        y = randint(self.screen.bottom_dialogue_min_y, self.screen.bottom_dialogue_max_y)
        return x, y
    
    def is_genshinimpact_active(self):
        """Checks if Genshin Impact is the active window."""
        return getActiveWindowTitle() == "Genshin Impact"
    
    def is_dialogue_playing(self):
        """Checks if a dialogue is playing automatically."""
        return pixel(self.screen.playing_icon_x, 
                    self.screen.playing_icon_y) == COLOR_AUTOPLAY_ICON
    
    def is_dialogue_option_available(self):
        """Checks if a dialogue option is available."""
        if pixel(self.screen.loading_screen_x, 
                self.screen.loading_screen_y) == COLOR_WHITE:
            return False
        if pixel(self.screen.dialogue_icon_x, 
                self.screen.dialogue_icon_lower_y) == COLOR_WHITE:
            return True
            
        if pixel(self.screen.dialogue_icon_x, 
                self.screen.dialogue_icon_higher_y) == COLOR_WHITE:
            return True
            
        return False
    
    def set_status(self, new_status):
        """Changes the status and updates the overlay."""
        self.status = new_status
        self.status_overlay.update_status(new_status)
    
    def on_press(self, key: Union[Key, KeyCode, None]) -> None:
        """Handles keyboard shortcuts to control the program."""
        key_pressed = str(key)
        
        if key_pressed == KEY_START:
            self.set_status(STATUS_RUN)
            print('ACTIVE')
            try:
                hdlg = win32gui.FindWindow(None, "Genshin Impact")
                win32gui.SetForegroundWindow(hdlg)
                win32gui.ShowWindow(hdlg, win32con.SW_SHOWNORMAL)
            except Exception as e:  
                print(f"Error bringing the window to the foreground: {e}")
        elif key_pressed == KEY_PAUSE:
            self.set_status(STATUS_PAUSE)
            print('PAUSED')
        elif key_pressed == KEY_EXIT:
            self.set_status(STATUS_EXIT)
            print('Closing the program')
            self.status_overlay.close()
            sys.exit(0)
        elif key_pressed == KEY_HELP:
            print('Displaying help')
            # Call the method to display shortcuts
            if hasattr(self, 'status_overlay') and self.status_overlay:
                self.status_overlay.show_keybindings()
    
    def run(self):
        """Executes the main loop of the dialogue skipper."""
        print('-------------\n'
              'F8 to start\n'
              'F9 to pause\n'
              'F12 to quit\n'
              '-------------')
              
        while True:
            while self.status == STATUS_PAUSE:
                sleep(0.5)
                
            if self.status == STATUS_EXIT:
                print('Closing the program')
                break
                
            if self.is_genshinimpact_active() and \
               (self.is_dialogue_playing() or self.is_dialogue_option_available()):
                # Periodically reposition the cursor to avoid bot detection
                if perf_counter() - self.last_reposition > self.time_between_repositions:
                    self.last_reposition = perf_counter()
                    self.time_between_repositions = self.random_interval() * 40
                    self.mouse.position = self.random_cursor_position()
                click()