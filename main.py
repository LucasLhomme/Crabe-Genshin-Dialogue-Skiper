"""
Crabe Dialogue Skipper
Program to automatically skip dialogues in Genshin Impact.
"""

import os
import sys
from threading import Thread
from pynput.keyboard import Listener # type: ignore

from screen_setup import ScreenSetup  
from dialogue_skipper import DialogueSkipper
from constants import STATUS_EXIT

def main():
    """Main function initializing and running the program."""
    try:
        os.system('cls')
        print('Welcome to Crabe Dialogue Skipper\n')
        
        screen_setup = ScreenSetup()
        skipper = DialogueSkipper(screen_setup)
        
        # Starting the main thread
        skipper_thread = Thread(target=skipper.run, daemon=True)
        skipper_thread.start()
        
        # Listening for keyboard events
        listener = Listener(on_press=skipper.on_press)
        listener.start()
        
        # Keep the program active until it is explicitly stopped
        try:
            while skipper_thread.is_alive() and skipper.status != STATUS_EXIT:
                skipper_thread.join(0.5)
        except KeyboardInterrupt:
            print("\nInterruption detected. Closing the program...")
            skipper.set_status(STATUS_EXIT)
            
        listener.stop()  # Proper shutdown of the listener
        if hasattr(skipper, 'status_overlay'):
            skipper.status_overlay.close()
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()