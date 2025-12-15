import cv2
import numpy as np
import pyautogui
import time
from hand_tracker import HandDetector

# --- CONFIGURATION ---
wCam, hCam = 640, 480       # Camera Resolution
frameR = 100                # Frame Reduction (padding) to reach edges of screen
smoothening = 7             # Higher = Smoother mouse, but more lag

def main():
    # 1. Setup Camera
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    
    detector = HandDetector(max_hands=1)
    
    # Get Screen Size (Your actual monitor size)
    wScr, hScr = pyautogui.size()
    
    # Variables for smoothing
    plocX, plocY = 0, 0 # Previous Location
    clocX, clocY = 0, 0 # Current Location
    
    print("🖱️ AI Virtual Mouse Started!")
    print("👉 Index Up: Move Cursor")
    print("🤏 Index + Middle Up + Click: Left Click")
    print("❌ Press 'q' to Quit")

    while True:
        # 1. Find Hand Landmarks
        success, img = cap.read()
        if not success: break
        
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=False)
        
        # Draw the "Active Box" (You must keep your hand inside this box)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        if len(lm_list) != 0:
            # Get coordinates of Index (8) and Middle (12)
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[12][1:]
            
            # Check which fingers are up
            fingers = detector.fingers_up()
            
            # --- MODE 1: MOVING MOUSE (Index Up, Middle Down) ---
            if fingers[1] == 1 and fingers[2] == 0:
                # Convert Coordinates: Map Camera (640x480) to Screen (1920x1080)
                # We use np.interp to scale the values
                # We mirror x1 (wCam - x1) because the webcam is mirrored
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                
                # Smoothening (Current = Previous + (Target - Previous) / Smoothness)
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                
                # Move Mouse
                # Fail-safe: PyAutoGUI has a safety feature. If you slam mouse to corner, it stops.
                try:
                    pyautogui.moveTo(wScr - clocX, clocY) # wScr - clocX flips it horizontally for intuition
                except:
                    pass
                
                # Update Previous location
                plocX, plocY = clocX, clocY
                
                # Visual Feedback
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            # --- MODE 2: CLICKING (Index + Middle Up) ---
            # Wait... isn't drawing Middle down? 
            # Let's change click to: Index Up + Thumb Up (Pinch)
            # Distance between Index (8) and Thumb (4)
            x_thumb, y_thumb = lm_list[4][1], lm_list[4][2]
            
            # Calculate distance
            dist = np.hypot(x1 - x_thumb, y1 - y_thumb)
            
            # If pinched close enough (< 30 pixels)
            if dist < 30:
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED) # Green circle
                pyautogui.click()
                print("Clicked!")
                time.sleep(0.2) # Prevent double clicking too fast

        # Display
        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()