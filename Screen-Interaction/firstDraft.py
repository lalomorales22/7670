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

        # Get available cameras
        cameras = self.get_available_cameras()

        if not cameras:
            ttk.Label(frame, text="No cameras found! Please check your camera connection.").grid(row=0, column=0, pady=20)
            self.selected_camera = None

            def close_dialog():
                root.destroy()

            ttk.Button(frame, text="OK", command=close_dialog).grid(row=1, column=0, pady=10)
        else:
            ttk.Label(frame, text="Select camera:").grid(row=0, column=0, pady=5)
            camera_var = tk.StringVar(value=f"Camera {cameras[0]}")  # Set default value
            camera_combo = ttk.Combobox(frame, textvariable=camera_var, state="readonly")
            camera_combo['values'] = [f"Camera {i}" for i in cameras]
            camera_combo.grid(row=1, column=0, pady=5)

            def on_select():
                selected_index = camera_combo.current()
                if selected_index >= 0:
                    self.selected_camera = cameras[selected_index]
                else:
                    self.selected_camera = cameras[0]  # Default to first camera if nothing selected
                root.destroy()

            ttk.Button(frame, text="Start", command=on_select).grid(row=2, column=0, pady=20)

        root.mainloop()
        return self.selected_camera

class Particle:
    def __init__(self, position):
        self.position = np.array(position, dtype=float)
        self.velocity = np.random.randn(2) * 2
        self.lifetime = random.randint(60, 120)
        self.color = [random.randint(100, 255) for _ in range(3)]

    def update(self):
        self.position += self.velocity
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0

class GestureControlledHUD:
    def __init__(self, camera_index):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=2
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Initialize camera
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open camera {camera_index}")

        # Read a frame to get actual camera resolution
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Failed to read from camera")

        self.camera_height, self.camera_width = frame.shape[:2]
        print(f"Camera initialized with resolution: {self.camera_width}x{self.camera_height}")

        # Initialize Pygame for graphics window
        pygame.init()
        self.window_width = self.camera_width
        self.window_height = self.camera_height
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Gesture Controlled HUD")

        self.running = True
        self.particles = []

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Read frame from camera
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame from camera.")
                break

            # Flip and process frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            # Clear screen
            self.screen.fill((0, 0, 0))

            hand_positions = []
            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    hand_positions.append(hand_landmarks)
                    # Draw landmarks on the frame
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # Convert OpenCV image to Pygame surface
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)  # Rotate if necessary
            frame_surface = pygame.surfarray.make_surface(frame)

            # Blit the camera frame onto the screen
            self.screen.blit(frame_surface, (0, 0))

            # Draw graphics reacting to hand positions
            self.draw_graphics(hand_positions)

            pygame.display.flip()
            clock.tick(30)  # Limit to 30 FPS

        self.cap.release()
        pygame.quit()

    def draw_graphics(self, hand_positions):
        # Update and draw particles
        new_particles = []
        for particle in self.particles:
            particle.update()
            if particle.is_alive():
                pygame.draw.circle(self.screen, particle.color, particle.position.astype(int), 3)
                new_particles.append(particle)
        self.particles = new_particles

        # Emit new particles based on hand positions
        for hand_landmarks in hand_positions:
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_tip.x * self.window_width)
            y = int(index_tip.y * self.window_height)
            # Emit particles at the index finger tip
            for _ in range(5):  # Emit 5 particles per frame
                self.particles.append(Particle([x, y]))

if __name__ == "__main__":
    try:
        # Show camera selection dialog
        camera_selector = CameraSelector()
        selected_camera = camera_selector.show_camera_dialog()

        if selected_camera is not None:
            print(f"Selected camera index: {selected_camera}")
            # Initialize and run the main application
            app = GestureControlledHUD(selected_camera)
            app.run()
        else:
            print("No camera selected or no cameras available.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
