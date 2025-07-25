import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

# Initialize mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Webcam
cap = cv2.VideoCapture(0)

# Previous click time
prev_left_click = 0
prev_right_click = 0

# Cursor smoothing parameters
smoothening = 5
prev_loc_x, prev_loc_y = 0, 0

# Toggle flag
mouse_enabled = True

def get_distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

print("[INFO] Press 't' to toggle mouse control. Press 'Esc' to exit.")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                lm_x, lm_y = int(lm.x * w), int(lm.y * h)
                lm_list.append((lm_x, lm_y))

            if lm_list:
                # Landmarks
                index_x, index_y = lm_list[8]
                middle_x, middle_y = lm_list[12]
                ring_x, ring_y = lm_list[16]

                # Draw hand landmarks
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if mouse_enabled:
                    # Smoothened cursor position
                    target_x = np.interp(index_x, [0, w], [0, screen_width])
                    target_y = np.interp(index_y, [0, h], [0, screen_height])

                    cur_x = prev_loc_x + (target_x - prev_loc_x) / smoothening
                    cur_y = prev_loc_y + (target_y - prev_loc_y) / smoothening
                    pyautogui.moveTo(cur_x, cur_y)
                    prev_loc_x, prev_loc_y = cur_x, cur_y

                    # Left click (Index + Middle)
                    if get_distance(index_x, index_y, middle_x, middle_y) < 40:
                        current_time = time.time()
                        if current_time - prev_left_click > 1:
                            pyautogui.click()
                            prev_left_click = current_time
                            cv2.circle(img, (index_x, index_y), 12, (0, 255, 0), cv2.FILLED)

                    # Right click (Middle + Ring)
                    if get_distance(middle_x, middle_y, ring_x, ring_y) < 40:
                        current_time = time.time()
                        if current_time - prev_right_click > 1:
                            pyautogui.rightClick()
                            prev_right_click = current_time
                            cv2.circle(img, (ring_x, ring_y), 12, (255, 0, 0), cv2.FILLED)

    # Display mouse toggle status
    status_text = f'Mouse Control: {"ON" if mouse_enabled else "OFF"}'
    cv2.putText(img, status_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0) if mouse_enabled else (0,0,255), 2)

    cv2.imshow("Virtual Mouse", img)

    key = cv2.waitKey(1)
    if key == 27:  # ESC to quit
        break
    elif key == ord('t'):
        mouse_enabled = not mouse_enabled

cap.release()
cv2.destroyAllWindows()
