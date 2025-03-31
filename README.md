# Crabe Dialogue Skipper

**Disclaimer:** Using third-party software is against Genshin Impact's Terms of Service. Use this tool at your own discretion and risk.

---

## Overview

Crabe Skipper is a Python-based tool designed to automatically skip dialogues in Genshin Impact, always selecting the bottom dialogue option. This can significantly speed up gameplay for users who prefer to focus on exploration and combat.

## Features

*   **Automatic Dialogue Skipping:** Automatically advances through dialogues by selecting the bottom option.
*   **Non-Standard Resolution Support:** Adapts to various screen resolutions, including non-standard aspect ratios.
*   **Keyboard Control:** Start, pause, and exit the script using simple keyboard shortcuts.
*   **Status Overlay:** Displays the current status of the script (Active, Paused, Closing...) on a semi-transparent overlay.
*   **Customizable Font:** Supports custom fonts for the status overlay, allowing for a personalized experience.
*   **Help Menu:** Displays a help menu with keyboard shortcuts via an in-game overlay.

## Requirements

*   **Operating System:** Windows
*   **Administrator Privileges:** Required for emulating mouse and keyboard inputs.
*   **Python:** Python 3.6 or higher
*   **Python Packages:** Install the required packages using `pip install -r requirements.txt`.
*   **Genshin Impact Settings:**
    *   The game must be running on the primary display and in a Windowed FullScreen.
    *   In **Settings > Other**, set **Auto-Play Story** to **Off**.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone git@github.com:LucasLhomme/Crabe-Genshin-Dialogue-Skiper.git
    cd Crabe-Genshin-Dialogue-Skiper
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run Genshin Impact.**
2.  **Run the script:** Execute `run.bat` with administrator privileges.
3.  **Control the script:**
    *   Press `F8` to start.
    *   Press `F9` to pause.
    *   Press `F12` to exit.
    *   Press `²` to display the help menu with keyboard shortcuts.

## Configuration

The script uses a `.env` file to store screen dimensions. If the dimensions are not set, the script will attempt to detect them automatically. You can manually edit the `.env` file to adjust the `WIDTH` and `HEIGHT` variables if needed.

## Troubleshooting

*   **Script not working?** Ensure you have administrator privileges and that the game is running on the primary display.
*   **Incorrect screen resolution?** Manually set the `WIDTH` and `HEIGHT` variables in the `.env` file.
*   **Font issues?** Make sure the font file is correctly placed in the `assets/fonts/` directory.

## Contributing

Contributions are welcome! If you have any suggestions or bug reports, please open an issue or submit a pull request.

## Credits

*   This project was inspired by [genshin-dialogue-autoskip](https://github.com/1hubert/genshin-dialogue-autoskip).

## Show Your Support

If you find this project helpful, please consider giving it a star on GitHub! ⭐

**Enjoy!**