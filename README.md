# 🖱️ AI Virtual Mouse & Hand Tracker

![Python](https://img.shields.io/badge/Python-3.9-blue)
![OpenCV](https://img.shields.io/badge/Computer%20Vision-OpenCV-green)
![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-orange)
![HCI](https://img.shields.io/badge/Domain-HCI-purple)

## 📋 Executive Summary
This project redefines **Human-Computer Interaction (HCI)** by turning a standard webcam into a touchless mouse. 

Using **Google MediaPipe** for hand landmark detection, the system tracks the index finger in real-time and maps its coordinates to the screen, allowing users to control the OS cursor without physical hardware. It features a "Pinch-to-Click" gesture engine and jitter reduction algorithms for smooth usability.

**Key Technical Features:**
* **Coordinate Mapping:** Linearly interpolates webcam coordinates (640x480) to screen resolution (1920x1080).
* **Jitter Reduction:** Implements a smoothing factor to dampen sensor noise and prevent cursor shaking.
* **Gesture Recognition:** Uses Euclidean distance between Index and Thumb landmarks to trigger "Left Click" events.

---

## 🛠️ Tech Stack
| Component | Library | Purpose |
| :--- | :--- | :--- |
| **Tracking Engine** | `mediapipe` | High-speed (30 FPS) hand skeleton tracking. |
| **Vision Processing** | `opencv-python` | Image flipping, landmark drawing, and frame capture. |
| **Hardware Control** | `pyautogui` | Programmatic control of the OS mouse cursor and clicks. |
| **Math** | `numpy` | Vector calculations for distance and interpolation. |

---

## 🚀 How to Run
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/ai-virtual-mouse.git](https://github.com/YOUR_USERNAME/ai-virtual-mouse.git)
    cd ai-virtual-mouse
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch the Mouse**
    ```bash
    python src/virtual_mouse.py
    ```

**Controls:**
* **Move Cursor:** Point with your **Index Finger** (keep Middle finger down).
* **Click:** Pinch your **Index** and **Thumb** together.
* **Quit:** Press `q`.

---

### 👤 Author
**[Eyoas Zewdie]**
