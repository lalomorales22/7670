import cv2
import mediapipe as mp
import pygame
import sys
import numpy as np
import tkinter as tk
from tkinter import ttk
import random
import pyttsx3
import threading
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional
import math

# Constants
WINDOW_TITLE = "Gesture Controlled HUD"
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7
MAX_HANDS = 2
TARGET_FPS = 30

@dataclass
class ARObject:
    position: Tuple[int, int]
    size: int
    color: Tuple[int, int, int]
    type: str
    lifetime: int = -1  # -1 means permanent

class Particle:
    def __init__(self, position: Tuple[float, float]):
        self.position = np.array(position, dtype=float)
        self.velocity = np.random.randn(2) * 2
        self.lifetime = random.randint(60, 120)
        self.color = [random.randint(100, 255) for _ in range(3)]
        self.size = random.randint(2, 5)

    def update(self):
        self.position += self.velocity
        self.lifetime -= 1
        self.velocity *= 0.95  # Add some drag

    def is_alive(self):
        return self.lifetime > 0

    def draw(self, screen):
        if self.is_alive():
            alpha = min(255, self.lifetime * 2)
            pygame.draw.circle(
                screen,
                (*self.color, alpha),
                self.position.astype(int),
                self.size
            )

class CameraSelector:
    def __init__(self):
        self.selected_camera = 0

    def get_available_cameras(self) -> List[int]:
        available_cameras = []
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    available_cameras.append(i)
                cap.release()
        return available_cameras

    def show_camera_dialog(self) -> Optional[int]:
        root = tk.Tk()
        root.title("Select Camera")

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
            ttk.Label(frame, text="No cameras found! Please check your connection.").grid(row=0, column=0, pady=20)
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

class GestureControlledHUD:
    def __init__(self, camera_index):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
            max_num_hands=MAX_HANDS
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Initialize camera
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open camera {camera_index}")

        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Failed to read from camera")

        self.camera_height, self.camera_width = frame.shape[:2]
        print(f"Camera initialized: {self.camera_width}x{self.camera_height}")

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        pygame.display.set_caption(WINDOW_TITLE)

        # Initialize state variables
        self.running = True
        self.particles = []
        self.ar_objects = []
        self.gesture_history = []
        self.last_gesture_time = time.time()
        self.mode = "normal"
        self.debug_mode = False

        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.voice_feedback_enabled = True
        
        # Add some initial AR objects (virtual buttons)
        self.ar_objects.append(ARObject((50, 50), 40, (0, 255, 0), "button"))
        self.ar_objects.append(ARObject((50, 120), 40, (255, 0, 0), "button"))

    def process_gestures(self, hand_landmarks) -> Optional[str]:
        if not hand_landmarks:
            return None

        # Get the first hand's landmarks
        landmarks = hand_landmarks[0].landmark

        # Calculate relevant finger positions
        thumb_tip = np.array([landmarks[4].x, landmarks[4].y])
        index_tip = np.array([landmarks[8].x, landmarks[8].y])
        
        # Calculate distance between thumb and index finger
        pinch_distance = np.linalg.norm(thumb_tip - index_tip)

        # Detect pinch gesture
        if pinch_distance < 0.05:  # Threshold for pinch
            return "pinch"
        
        # Detect open palm
        if all(landmarks[i].y < landmarks[0].y for i in [8, 12, 16, 20]):
            return "open_palm"

        return None

    def provide_feedback(self, message: str):
        if self.voice_feedback_enabled:
            threading.Thread(target=self.tts_engine.say, args=(message,), daemon=True).start()
            self.tts_engine.runAndWait()

    def add_particles(self, position: Tuple[int, int], count: int = 10):
        for _ in range(count):
            self.particles.append(Particle(position))

    def update_particles(self):
        # Update existing particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()

    def draw_ar_overlays(self):
        for obj in self.ar_objects:
            if obj.type == "button":
                pygame.draw.circle(self.screen, obj.color, obj.position, obj.size)
                # Add highlight effect
                pygame.draw.circle(self.screen, (255, 255, 255), obj.position, obj.size + 2, 2)

    def draw_debug_info(self, frame_rate: float):
        if not self.debug_mode:
            return

        font = pygame.font.Font(None, 36)
        debug_info = [
            f"FPS: {frame_rate:.1f}",
            f"Mode: {self.mode}",
            f"Particles: {len(self.particles)}",
            f"AR Objects: {len(self.ar_objects)}"
        ]

        y = 10
        for info in debug_info:
            text = font.render(info, True, (255, 255, 255))
            self.screen.blit(text, (10, y))
            y += 30

    def run(self):
        clock = pygame.time.Clock()
        last_time = time.time()
        
        while self.running:
            # Calculate frame rate
            current_time = time.time()
            dt = current_time - last_time
            frame_rate = 1.0 / dt if dt > 0 else 0
            last_time = current_time

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:  # Toggle debug mode
                        self.debug_mode = not self.debug_mode
                    elif event.key == pygame.K_v:  # Toggle voice feedback
                        self.voice_feedback_enabled = not self.voice_feedback_enabled
                        self.provide_feedback("Voice feedback toggled")

            # Read and process camera frame
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame")
                break

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Process hand landmarks and gestures
            if results.multi_hand_landmarks:
                # Draw hand landmarks
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Add particles at fingertips
                    for tip_id in [4, 8, 12, 16, 20]:  # Finger tip indices
                        tip = hand_landmarks.landmark[tip_id]
                        screen_x = int(tip.x * self.camera_width)
                        screen_y = int(tip.y * self.camera_height)
                        self.add_particles((screen_x, screen_y), 2)

                # Process gestures
                gesture = self.process_gestures(results.multi_hand_landmarks)
                if gesture and (current_time - self.last_gesture_time) > 1.0:
                    self.provide_feedback(f"Detected {gesture}")
                    self.last_gesture_time = current_time

            # Convert frame to Pygame surface
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame_surface = pygame.surfarray.make_surface(frame)

            # Draw everything
            self.screen.blit(frame_surface, (0, 0))
            self.update_particles()
            for particle in self.particles:
                particle.draw(self.screen)
            self.draw_ar_overlays()
            self.draw_debug_info(frame_rate)

            # Update display
            pygame.display.flip()
            clock.tick(TARGET_FPS)

        # Cleanup
        self.cap.release()
        pygame.quit()
        cv2.destroyAllWindows()

def main():
    # Initialize camera selector
    camera_selector = CameraSelector()
    camera_index = camera_selector.show_camera_dialog()
    
    if camera_index is None:
        print("No camera selected. Exiting...")
        sys.exit(1)

    try:
        # Initialize and run the HUD
        hud = GestureControlledHUD(camera_index)
        hud.run()
    except Exception as e:
        print(f"Error running HUD: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()