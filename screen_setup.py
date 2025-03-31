"""Module managing screen configuration and dimensions."""

import os
from win32api import GetSystemMetrics # type: ignore
from dotenv import find_dotenv, load_dotenv, set_key # type: ignore

class ScreenSetup:
    """Class managing screen configuration and dimensions."""
    
    def __init__(self):
        """Initializes screen dimensions and detection pixel coordinates."""
        self.width = None
        self.height = None
        self.setup_screen_dimensions()
        self.calculate_pixel_coordinates()
    
    def setup_screen_dimensions(self):
        """Sets up screen dimensions from .env file or by detection."""
        load_dotenv()
        
        if os.environ.get('WIDTH', '') == '' or os.environ.get('HEIGHT', '') == '':
            self._detect_screen_dimensions()
        else:
            self.width = int(os.getenv('WIDTH'))
            self.height = int(os.getenv('HEIGHT'))
    
    def _detect_screen_dimensions(self):
        """Detects screen dimensions and saves them."""
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

        print(f'Detected resolution: {self.width}x{self.height}')
        print('Is the resolution correct? (y/n)')
        response = input()

        if response.lower().startswith('n'):
            print('Enter width: ', end='')
            self.width = int(input())
            print('Enter height: ', end='')
            self.height = int(input())
            print(f'\nNew resolution: {self.width}x{self.height}\n')

        # Save to .env file
        dotenv_file = find_dotenv()
        set_key(dotenv_file, "WIDTH", str(self.width), quote_mode="never")
        set_key(dotenv_file, "HEIGHT", str(self.height), quote_mode="never")
    
    def width_adjust(self, x: int) -> int:
        """Adjusts an x coordinate to screen width."""
        return int(x/1920 * self.width)
    
    def height_adjust(self, y: int) -> int:
        """Adjusts a y coordinate to screen height."""
        return int(y/1080 * self.height)
    
    def get_position_right(self, hdpos_x: int, doublehdpos_x: int, extra: float = 0) -> int:
        """Calculates the position of a pixel related to the right side of the screen."""
        if self.width <= 3840:
            extra = 0
        diff = doublehdpos_x - hdpos_x
        change_per_pixel = diff/1920
        screen_diff = self.width - 1920
        extra_pixels = screen_diff * (change_per_pixel + extra)
        return int(hdpos_x + extra_pixels)
    
    def get_position_left(self, hdpos_x: int, doublehdpos_x: int) -> int:
        """Calculates the position of a pixel related to the left side of the screen."""
        diff = doublehdpos_x - hdpos_x
        change_per_pixel = diff/1920
        screen_diff = self.width - 1920
        extra_pixels = screen_diff * change_per_pixel
        return int(hdpos_x + extra_pixels)
    
    def calculate_pixel_coordinates(self):
        """Calculates all detection pixel coordinates."""
        is_non_standard_ratio = (self.width > 1920 and 
                                float(self.height)/float(self.width) != 0.5625)
                                
        # Lower dialogue area
        if is_non_standard_ratio:
            self.bottom_dialogue_min_x = self.get_position_right(1300, 2734, 0.031)
            self.bottom_dialogue_max_x = self.get_position_right(1700, 3303, -0.015)
        else:
            self.bottom_dialogue_min_x = self.width_adjust(1300)
            self.bottom_dialogue_max_x = self.width_adjust(1700)
        self.bottom_dialogue_min_y = self.height_adjust(790)
        self.bottom_dialogue_max_y = self.height_adjust(800)
        
        # Autoplay button position
        if is_non_standard_ratio:
            self.playing_icon_x = self.get_position_left(84, 230)
            if self.playing_icon_x > 231:
                self.playing_icon_x = 230
            self.playing_icon_y = self.height_adjust(46)
        else:
            self.playing_icon_x = self.width_adjust(84)
            self.playing_icon_y = self.height_adjust(46)
        
        # Dialogue icon position
        if is_non_standard_ratio:
            self.dialogue_icon_x = self.get_position_right(1301, 2770, 0.02)
            self.dialogue_icon_lower_y = self.height_adjust(810)
            self.dialogue_icon_higher_y = self.height_adjust(792)
        else:
            self.dialogue_icon_x = self.width_adjust(1301)
            self.dialogue_icon_lower_y = self.height_adjust(808)
            self.dialogue_icon_higher_y = self.height_adjust(790)
        
        # Loading screen check point
        self.loading_screen_x = self.width_adjust(1200)
        self.loading_screen_y = self.height_adjust(700)