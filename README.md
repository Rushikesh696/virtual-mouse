# 🖱️ Hand Gesture Virtual Mouse using OpenCV + MediaPipe

Control your computer mouse using only your **index and middle fingers** detected through webcam.

### Features
- Move cursor with index finger
- Left-click: Touch index + middle fingers
- Right-click: Touch middle + ring fingers
- Cursor smoothing to reduce jitter
- Toggle control using `'t'` key

### 🧠 Tech Stack
- Python
- OpenCV
- MediaPipe
- PyAutoGUI

### Tech Stack Explained
1. **Python**
Why: It's easy to use, fast to prototype, and has rich libraries for computer vision and automation.

How it's used:

Runs the logic for capturing webcam input.

Ties everything together using OpenCV, MediaPipe, and PyAutoGUI.

2. **OpenCV**
Why: It’s the most popular library for image/video processing.

How it's used:

Captures real-time video from your webcam (cv2.VideoCapture()).

Converts image color formats (cv2.cvtColor()).

Draws hand landmarks on frames for visual feedback.

Handles keyboard input (cv2.waitKey()).

Displays the webcam feed (cv2.imshow()).

3. **MediaPipe**
Why: It offers high-performance pre-trained ML models for real-time hand, face, pose detection.

How it's used:

Detects your hand and finger landmarks (21 key points per hand).

Specifically extracts coordinates of Index, Middle, Ring fingertips to control the mouse.

Works fast in real-time even on CPU.

4. **PyAutoGUI**
Why: It lets Python control the mouse, keyboard, and screen.

How it's used:

Move cursor based on index finger position (pyautogui.moveTo()).

Left-click and right-click based on finger gestures (pyautogui.click() / rightClick()).

Gets screen resolution for accurate cursor mapping.

### Workflow Summary:
OpenCV reads webcam frame 

MediaPipe detects hand and finger landmarks 

Coordinates are mapped to screen size 

PyAutoGUI moves the mouse or clicks based on gestures 

Output shown on screen via OpenCV GUI
