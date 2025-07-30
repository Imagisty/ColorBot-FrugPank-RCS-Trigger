Enhanced Aimbot Vision (Windows PC, Python)
This project is an AI-assisted automatic aiming and auto-shooting tool written in Python with a modern GUI and flexible settings using Tkinter. It supports Windows OS, uses screen capture, PyWin32, and OpenCV.

Features
Auto-Aim: Automatic mouse aiming on targets based on color detection (neon pink/magenta).

Auto-Shoot: Automatic shooting when the target is within a designated zone.

Recoil Compensation: Compensates weapon recoil for better accuracy.

Multi-tab customizable GUI to change detection zones, sensitivity, radii, keybinds, and aggressive options.

Settings are saved in a JSON file and loaded automatically on start.

Works across all active windows on Windows.

Installation
Clone or download this repository:
Install Python (version 3.8 to 3.12 recommended).

Install the dependencies:
requirements
text
opencv-python
numpy
pywin32
pynput
mss
Make sure you have Visual C++ Redistributable installed, especially if you face errors with pywin32 or OpenCV.

Usage
Run the main script:


python main.py
The GUI will open automatically.

Use the GUI to adjust all parameters on the fly (aim sensitivity, zones, shoot delay, etc.).

Press configured hotkeys to toggle features.

Project Structure
main.py — main loop with event handling, input listeners, and screen capture.

aiming.py — functions for mouse aiming and shooting logic.

config.py — constants and screen resolution/scaling.

detection.py — target detection algorithms based on color masks.

gui.py — implementation of the Tkinter GUI with tabs and widgets.

recoil.py — recoil compensation logic.

utils.py — settings management, loading/saving configs, and helpers.

enhanced_settings.json — settings file auto-generated and saved.

Recommended
Run the program as Administrator for best compatibility.

Adjust parameters according to your screen resolution and game window.

This program only controls mouse movement and clicks through Windows API, no memory manipulation.

License and Disclaimer
This project is for educational purposes. Using any aimbot or auto-shoot software in multiplayer games can violate game policies and may result in bans. Use responsibly and only in permitted environments.
