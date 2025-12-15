import cv2
import numpy as np
from hand_tracker import HandDetector
import math

def get_cube_vertices(center, size):
    """
    Returns 3D coordinates of a cube centered at 'center'.
    Structure: [x, y, z]
    """
    cx, cy, cz = center
    r = size / 2  # Radius/Half-size
    
    # 8 corners of a cube
    vertices = np.array([
        [cx - r, cy - r, cz - r], # 0: Back Top Left
        [cx + r, cy - r, cz - r], # 1: Back Top Right
        [cx + r, cy + r, cz - r], # 2: Back Bottom Right
        [cx - r, cy + r, cz - r], # 3: Back Bottom Left
        [cx - r, cy - r, cz + r], # 4: Front Top Left
        [cx + r, cy - r, cz + r], # 5: Front Top Right
        [cx + r, cy + r, cz + r], # 6: Front Bottom Right
        [cx - r, cy + r, cz + r]  # 7: Front Bottom Left
    ])
    return vertices

def project_points(vertices, f=500, cx=640, cy=360):
    """
    Projects 3D points (x,y,z) onto a 2D screen (x,y).
    Formula: x2d = x3d * (f / z3d) + cx
    """
    projected = []
    for v in vertices:
        x, y, z = v
        # Prevent division by zero if z is too close
        if z <= 0.1: z = 0.1
        
        # Perspective Projection Logic
        x_proj = int(x * (f / z) + cx)
        y_proj = int(y * (f / z) + cy)
        projected.append((x_proj, y_proj))
        
    return projected

def draw_cube(img, points, color=(0, 255, 0)):
    """
    Connects the 8 corners to draw the wireframe cube.
    """
    # Define connections (edges)
    edges = [
        (0,1), (1,2), (2,3), (3,0), # Back Face
        (4,5), (5,6), (6,7), (7,4), # Front Face
        (0,4), (1,5), (2,6), (3,7)  # Connecting Lines
    ]
    
    for s, e in edges:
        cv2.line(img, points[s], points[e], color, 3)

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detection_con=0.8)
    
    # Simulated Camera Parameters
    focal_length = 600  # How "zoomed in" the lens is
    
    print("🧊 AR Cube Started!")
    print("👉 Point your Index Finger to hold the cube.")
    print("🤏 Pinch (Index+Thumb) to change color.")
    
    cube_color = (255, 0, 0) # Start Blue

    while True:
        success, img = cap.read()
        if not success: break
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        
        # Center of screen (Principal Point)
        cx, cy = w // 2, h // 2

        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=False)

        if len(lm_list) != 0:
            # Get Index Finger Tip (ID 8)
            idx_x, idx_y = lm_list[8][1], lm_list[8][2]
            
            # --- AR LOGIC ---
            # We map the 2D screen coordinates of the finger to a 3D world position
            # We assume a fixed 'Z' depth for the finger (e.g., 50cm away)
            finger_z_depth = 500 
            
            # Back-calculate the 3D X and Y based on the finger position
            # (Inverse of the projection formula)
            world_x = (idx_x - cx) * finger_z_depth / focal_length
            world_y = (idx_y - cy) * finger_z_depth / focal_length
            
            # Create Cube at this 3D position
            cube_center = [world_x, world_y, finger_z_depth]
            cube_points_3d = get_cube_vertices(cube_center, size=150)
            
            # Rotate Cube (Optional "Wow" Factor: Rotate based on hand movement)
            # For now, let's keep it simple and stable.
            
            # Project back to 2D to draw
            cube_points_2d = project_points(cube_points_3d, f=focal_length, cx=cx, cy=cy)
            
            # Check interaction (Pinch to change color)
            # Distance between Index (8) and Thumb (4)
            x_thumb, y_thumb = lm_list[4][1], lm_list[4][2]
            dist = math.hypot(x_thumb - idx_x, y_thumb - idx_y)
            
            if dist < 30:
                cube_color = (0, 0, 255) # Turn Red on Pinch
                cv2.putText(img, "GRABBED", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
            else:
                cube_color = (255, 255, 0) # Cyan normally

            draw_cube(img, cube_points_2d, color=cube_color)

        cv2.imshow("AR Cube", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()