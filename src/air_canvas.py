import cv2
import numpy as np
import os
from hand_tracker import HandDetector

# --- CONFIGURATION ---
brush_thickness = 15
eraser_thickness = 50
draw_color = (255, 0, 255) # Start with Purple
eraser_color = (0, 0, 0)   # Black acts as eraser

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) # Width
    cap.set(4, 720)  # Height

    detector = HandDetector(detection_con=0.85)
    
    # "xp" and "yp" store the Previous x,y coordinates
    # We need them to draw smooth lines (connecting the dots)
    xp, yp = 0, 0
    
    # The Canvas: A black image where we draw the ink
    img_canvas = np.zeros((720, 1280, 3), np.uint8)

    print("🎨 Air Canvas Started!")
    print("👉 Index Finger ONLY = DRAW")
    print("✌️ Index + Middle Finger = HOVER (Move without drawing)")
    print("🗑️ Press 'c' to CLEAR canvas")
    print("❌ Press 'q' to QUIT")

    while True:
        # 1. Import Image
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1) # Mirror mode

        # 2. Find Hand Landmarks
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=False)

        if len(lm_list) != 0:
            # Tip of Index and Middle Fingers
            x1, y1 = lm_list[8][1:]  # Index Tip
            x2, y2 = lm_list[12][1:] # Middle Tip

            # Check which fingers are up
            fingers = detector.fingers_up() 
            # Note: We need to add fingers_up() to your HandDetector class in the next step!

            # --- SELECTION MODE (Two Fingers Up) ---
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0 # Reset previous points so we don't draw a line from the last drawing spot
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv2.FILLED)
                print("Selection Mode")

            # --- DRAWING MODE (Index Finger Only) ---
            if fingers[1] and not fingers[2]:
                cv2.circle(img, (x1, y1), 15, draw_color, cv2.FILLED)
                print("Drawing Mode")

                # If we are just starting to draw
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                # Draw a line from previous point to current point
                # We draw on the CANVAS, not just the webcam feed
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)
                
                # Update previous points
                xp, yp = x1, y1

        # 3. Merge the Canvas with the Webcam Feed
        # Convert the black canvas to gray to create a mask
        img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        
        # Invert the original image where we drew
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, img_inv)
        
        # Add the color
        img = cv2.bitwise_or(img, img_canvas)

        # 4. Display
        cv2.imshow("Air Canvas", img)
        
        # Controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('c'):
            img_canvas = np.zeros((720, 1280, 3), np.uint8) # Clear

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()