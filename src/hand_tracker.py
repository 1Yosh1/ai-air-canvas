import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20] # IDs for fingertips (Thumb, Index, Middle, Ring, Pinky)

    def find_hands(self, img, draw=True):
        """
        Detects hands in the current frame and draws the skeleton.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        """
        Returns a list of (id, x, y) coordinates for all 21 hand landmarks.
        """
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                # Convert normalized coordinates (0.0 - 1.0) to pixel coordinates
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                
                # Highlight the Index Finger Tip (ID 8)
                if draw and id == 8:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lm_list

def main():
    # Standard webcam setup
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    
    print("🎥 Webcam started. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            break
            
        # Flip image horizontally so it acts like a mirror
        img = cv2.flip(img, 1)

        # 1. Find Hand
        img = detector.find_hands(img)
        
        # 2. Get Coordinates
        lm_list = detector.find_position(img)
        
        # 3. Print coordinate of Index Finger Tip (ID 8)
        if len(lm_list) != 0:
            print(f"Index Finger Tip Pos: {lm_list[8]}")

        cv2.imshow("Air Canvas Tracking", img)
        
        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()