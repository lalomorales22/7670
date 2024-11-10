import cv2
import mediapipe as mp
import pygame
import sys
import numpy as np
import tkinter as tk
from tkinter import ttk
import random

class CameraSelector:
    def __init__(self):
        self.selected_camera = 0

    def get_available_cameras(self):
        """Find available camera devices"""
        available_cameras = []
        # Only check first 5 indexes
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    available_cameras.append(i)
                cap.release()
        return available_cameras

    def show_camera_dialog(self):
        """Show camera selection dialog"""
        root = tk.Tk()
        root.title("Select Camera")

        # Center window
        window_width = 300
        window_height = 150
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        cameras = self.get_available_cameras()

        if not cameras:
            ttk.Label(frame, text="No cameras found! Please check your camera connection.").grid(row=0, column=0, pady=20)
            self.selected_camera = None

            def close_dialog():
                root.destroy()

            ttk.Button(frame, text="OK", command=close_dialog).grid(row=1, column=0, pady=10)
        else:
            ttk.Label(frame, text="Select camera:").grid(row=0, column=0, pady=5)
            camera_var = tk.StringVar(value=f"Camera {cameras[0]}")
            camera_combo = ttk.Combobox(frame, textvariable=camera_var, state="readonly")
            camera_combo['values'] = [f"Camera {i}" for i in cameras]
            camera_combo.grid(row=1, column=0, pady=5)

            def on_select():
                selected_index = camera_combo.current()
                if selected_index >= 0:
                    self.selected_camera = cameras[selected_index]
                else:
                    self.selected_camera = cameras[0]
                root.destroy()

            ttk.Button(frame, text="Start", command=on_select).grid(row=2, column=0, pady=20)

        root.mainloop()
        return self.selected_camera

class Particle:
    def __init__(self, position):
        self.position = np.array(position, dtype=float)
        self.velocity = np.random.randn(2) * 2
        self.lifetime = random.randint(60, 120)
        # Make particles more vibrant with brighter colors
        self.color = [random.randint(150, 255) for _ in range(3)]
        self.size = random.randint(2, 4)  # Varied particle sizes

    def update(self):
        self.position += self.velocity
        self.lifetime -= 1
        # Fade out the particle as it ages
        fade_factor = self.lifetime / 120
        self.current_color = [int(c * fade_factor) for c in self.color]

    def is_alive(self):
        return self.lifetime > 0

class GestureVisualizer:
    def __init__(self, camera_index):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=2
        )

        # Initialize camera
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open camera {camera_index}")

        # Read a frame to get actual camera resolution
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Failed to read from camera")

        self.camera_height, self.camera_width = frame.shape[:2]
        
        # Initialize Pygame
        pygame.init()
        self.window_width = self.camera_width
        self.window_height = self.camera_height
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Gesture Visualization")

        self.running = True
        self.particles = []
        
        # Colors for hand landmarks and connections
        self.landmark_color = (0, 255, 255)  # Cyan for landmarks
        self.connection_color = (255, 255, 0)  # Yellow for connections

    def draw_landmarks(self, hand_landmarks):
        # Draw connections
        for connection in self.mp_hands.HAND_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            
            start_pos = hand_landmarks.landmark[start_idx]
            end_pos = hand_landmarks.landmark[end_idx]
            
            start_x = int(start_pos.x * self.window_width)
            start_y = int(start_pos.y * self.window_height)
            end_x = int(end_pos.x * self.window_width)
            end_y = int(end_pos.y * self.window_height)
            
            pygame.draw.line(self.screen, self.connection_color, 
                           (start_x, start_y), (end_x, end_y), 2)

        # Draw landmarks
        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * self.window_width)
            y = int(landmark.y * self.window_height)
            pygame.draw.circle(self.screen, self.landmark_color, (x, y), 4)

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Read and process frame
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame from camera.")
                break

            # Flip frame horizontally for natural movement
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            # Clear screen with black background
            self.screen.fill((0, 0, 0))

            # Process hand landmarks and draw particles
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw the hand skeleton
                    self.draw_landmarks(hand_landmarks)
                    
                    # Add particles at fingertips
                    for tip_id in [4, 8, 12, 16, 20]:  # IDs for all fingertips
                        tip = hand_landmarks.landmark[tip_id]
                        x = int(tip.x * self.window_width)
                        y = int(tip.y * self.window_height)
                        # Emit particles at each fingertip
                        for _ in range(2):  # Reduced number of particles per fingertip
                            self.particles.append(Particle([x, y]))

            # Update and draw particles
            new_particles = []
            for particle in self.particles:
                particle.update()
                if particle.is_alive():
                    pygame.draw.circle(self.screen, particle.current_color, 
                                    particle.position.astype(int), particle.size)
                    new_particles.append(particle)
            self.particles = new_particles

            pygame.display.flip()
            clock.tick(60)  # Increased to 60 FPS for smoother animation

        self.cap.release()
        pygame.quit()

if __name__ == "__main__":
    try:
        camera_selector = CameraSelector()
        selected_camera = camera_selector.show_camera_dialog()

        if selected_camera is not None:
            print(f"Selected camera index: {selected_camera}")
            app = GestureVisualizer(selected_camera)
            app.run()
        else:
            print("No camera selected or no cameras available.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)