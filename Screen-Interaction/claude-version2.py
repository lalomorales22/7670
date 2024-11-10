import cv2
import mediapipe as mp
import pygame
import sys
import numpy as np
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import json
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import math
import time

# Constants
WINDOW_TITLE = "Advanced Gesture Control Interface"
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7
MAX_HANDS = 2
TARGET_FPS = 30

@dataclass
class VisualizationSettings:
    show_landmarks: bool = True
    show_connections: bool = True
    landmark_color: Tuple[int, int, int] = (0, 255, 0)
    connection_color: Tuple[int, int, int] = (255, 0, 0)
    particle_effects: bool = True
    debug_overlay: bool = False
    visualization_mode: str = "normal"  # normal, heat_map, skeleton, minimalist
    overlay_opacity: float = 0.7

@dataclass
class ARObject:
    position: Tuple[int, int]
    size: int
    color: Tuple[int, int, int]
    type: str
    active: bool = True
    label: str = ""
    icon: Optional[str] = None

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.enabled = True
        self.max_particles = 100
        self.particle_lifetime = 60
        self.particle_size_range = (2, 5)
        self.particle_speed = 2.0
        self.particle_colors = [(255, 255, 255), (0, 255, 255), (255, 0, 255)]

    def add_particle(self, position: Tuple[float, float]):
        if not self.enabled or len(self.particles) >= self.max_particles:
            return

        self.particles.append({
            'position': np.array(position, dtype=float),
            'velocity': np.random.randn(2) * self.particle_speed,
            'lifetime': random.randint(30, self.particle_lifetime),
            'color': random.choice(self.particle_colors),
            'size': random.randint(*self.particle_size_range)
        })

    def update(self):
        self.particles = [p for p in self.particles if p['lifetime'] > 0]
        for particle in self.particles:
            particle['position'] += particle['velocity']
            particle['lifetime'] -= 1
            particle['velocity'] *= 0.95

    def draw(self, surface):
        if not self.enabled:
            return

        for particle in self.particles:
            alpha = min(255, particle['lifetime'] * 2)
            color_with_alpha = (*particle['color'], alpha)
            pos = particle['position'].astype(int)
            pygame.draw.circle(surface, color_with_alpha, pos, particle['size'])

class CameraSelector:
    def __init__(self):
        self.selected_camera = 0

    def get_available_cameras(self) -> List[int]:
        available_cameras = []
        # Only check the first 3 camera indices (0, 1, 2)
        for i in range(3):
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, _ = cap.read()
                    if ret:
                        available_cameras.append(i)
                cap.release()
            except Exception as e:
                print(f"Error checking camera {i}: {e}")
        return available_cameras

    def show_camera_dialog(self) -> Optional[int]:
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

class GestureControlGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Gesture Control Settings")
        self.settings = VisualizationSettings()
        self.create_gui()

    def create_gui(self):
        # Create main frame with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # Visual Settings Tab
        visual_frame = ttk.Frame(self.notebook)
        self.notebook.add(visual_frame, text='Visual Settings')

        # Create settings controls
        ttk.Label(visual_frame, text="Visualization Mode").grid(row=0, column=0, pady=5)
        self.mode_var = tk.StringVar(value=self.settings.visualization_mode)
        modes = ['normal', 'heat_map', 'skeleton', 'minimalist']
        mode_combo = ttk.Combobox(visual_frame, textvariable=self.mode_var, values=modes)
        mode_combo.grid(row=0, column=1, pady=5)

        # Checkboxes for various options
        self.landmark_var = tk.BooleanVar(value=self.settings.show_landmarks)
        ttk.Checkbutton(visual_frame, text="Show Landmarks", variable=self.landmark_var).grid(row=1, column=0, pady=5)

        self.connections_var = tk.BooleanVar(value=self.settings.show_connections)
        ttk.Checkbutton(visual_frame, text="Show Connections", variable=self.connections_var).grid(row=2, column=0, pady=5)

        self.particles_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(visual_frame, text="Particle Effects", variable=self.particles_var).grid(row=3, column=0, pady=5)

        # Color selection buttons
        ttk.Button(visual_frame, text="Landmark Color", command=self.choose_landmark_color).grid(row=1, column=1, pady=5)
        ttk.Button(visual_frame, text="Connection Color", command=self.choose_connection_color).grid(row=2, column=1, pady=5)

        # Opacity slider
        ttk.Label(visual_frame, text="Overlay Opacity").grid(row=4, column=0, pady=5)
        self.opacity_var = tk.DoubleVar(value=self.settings.overlay_opacity)
        ttk.Scale(visual_frame, from_=0, to=1, variable=self.opacity_var, orient='horizontal').grid(row=4, column=1, pady=5)

        # Gesture Settings Tab
        gesture_frame = ttk.Frame(self.notebook)
        self.notebook.add(gesture_frame, text='Gesture Settings')

        # Add gesture sensitivity controls
        ttk.Label(gesture_frame, text="Detection Confidence").grid(row=0, column=0, pady=5)
        self.detection_confidence = tk.DoubleVar(value=MIN_DETECTION_CONFIDENCE)
        ttk.Scale(gesture_frame, from_=0, to=1, variable=self.detection_confidence, orient='horizontal').grid(row=0, column=1, pady=5)

        # Custom Gestures Tab
        gestures_frame = ttk.Frame(self.notebook)
        self.notebook.add(gestures_frame, text='Custom Gestures')

        # Add custom gesture recording interface
        self.gesture_listbox = tk.Listbox(gestures_frame, height=10)
        self.gesture_listbox.grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Button(gestures_frame, text="Record New Gesture", command=self.record_gesture).grid(row=1, column=0, pady=5)
        ttk.Button(gestures_frame, text="Delete Selected", command=self.delete_gesture).grid(row=1, column=1, pady=5)

    def choose_landmark_color(self):
        color = colorchooser.askcolor(title="Choose Landmark Color")
        if color[0]:
            self.settings.landmark_color = tuple(map(int, color[0]))

    def choose_connection_color(self):
        color = colorchooser.askcolor(title="Choose Connection Color")
        if color[0]:
            self.settings.connection_color = tuple(map(int, color[0]))

    def record_gesture(self):
        # Implement gesture recording functionality
        pass

    def delete_gesture(self):
        # Implement gesture deletion functionality
        pass

    def get_settings(self) -> VisualizationSettings:
        self.settings.visualization_mode = self.mode_var.get()
        self.settings.show_landmarks = self.landmark_var.get()
        self.settings.show_connections = self.connections_var.get()
        self.settings.particle_effects = self.particles_var.get()
        self.settings.overlay_opacity = self.opacity_var.get()
        return self.settings

class GestureControlledHUD:
    def __init__(self, camera_index: int):
        try:
            # Initialize MediaPipe
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
                max_num_hands=MAX_HANDS
            )
            self.mp_draw = mp.solutions.drawing_utils

            # Initialize camera with error handling
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                raise ValueError(f"Failed to open camera {camera_index}")
            
            # Try to read a test frame
            ret, test_frame = self.cap.read()
            if not ret or test_frame is None:
                raise ValueError(f"Failed to read from camera {camera_index}")
            
            self.setup_camera()

            # Initialize Pygame
            pygame.init()
            self.setup_display()

            # Initialize systems
            self.particle_system = ParticleSystem()
            self.ar_objects = []
            self.settings = VisualizationSettings()
            self.gui = GestureControlGUI()
            
            # Initialize visualization state
            self.heat_map = np.zeros((self.camera_height, self.camera_width))
            self.gesture_trail = []
            self.running = True
            
        except Exception as e:
            # Clean up if initialization fails
            if hasattr(self, 'cap') and self.cap is not None:
                self.cap.release()
            if pygame.get_init():
                pygame.quit()
            raise Exception(f"Failed to initialize HUD: {str(e)}")
        pygame.init()
        self.setup_display()

        # Initialize systems
        self.particle_system = ParticleSystem()
        self.ar_objects = []
        self.settings = VisualizationSettings()
        self.gui = GestureControlGUI()
        
        # Initialize visualization state
        self.heat_map = np.zeros((self.camera_height, self.camera_width))
        self.gesture_trail = []
        self.running = True

    def setup_camera(self):
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open camera")
        
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Failed to read from camera")
            
        self.camera_height, self.camera_width = frame.shape[:2]

    def setup_display(self):
        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.font = pygame.font.Font(None, 36)

    def process_frame(self, frame):
        # Convert frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        # Update settings from GUI
        self.settings = self.gui.get_settings()

        # Process hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.process_landmarks(hand_landmarks, frame)

        return frame

    def process_landmarks(self, landmarks, frame):
        if self.settings.visualization_mode == "heat_map":
            self.update_heat_map(landmarks)
        
        if self.settings.show_landmarks:
            self.draw_landmarks(landmarks, frame)
            
        if self.settings.particle_effects:
            self.add_particles_at_landmarks(landmarks)

    def update_heat_map(self, landmarks):
        for landmark in landmarks.landmark:
            x = int(landmark.x * self.camera_width)
            y = int(landmark.y * self.camera_height)
            cv2.circle(self.heat_map, (x, y), 10, 1, -1)
        self.heat_map *= 0.95  # Fade effect

    def draw_landmarks(self, landmarks, frame):
        if self.settings.show_landmarks:
            self.mp_draw.draw_landmarks(
                frame,
                landmarks,
                self.mp_hands.HAND_CONNECTIONS if self.settings.show_connections else None,
                landmark_drawing_spec=self.mp_draw.DrawingSpec(
                    color=self.settings.landmark_color,
                    thickness=2,
                    circle_radius=4
                ),
                connection_drawing_spec=self.mp_draw.DrawingSpec(
                    color=self.settings.connection_color,
                    thickness=2
                )
            )

    def add_particles_at_landmarks(self, landmarks):
        for tip_id in [4, 8, 12, 16, 20]:  # Finger tip indices
            tip = landmarks.landmark[tip_id]
            screen_x = int(tip.x * self.camera_width)
            screen_y = int(tip.y * self.camera_height)
            self.particle_system.add_particle((screen_x, screen_y))

    def draw_visualization_overlay(self):
        if self.settings.visualization_mode == "heat_map":
            heat_surface = pygame.surfarray.make_surface(
                (self.heat_map * 255).astype(np.uint8))
            self.screen.blit(heat_surface, (0, 0))

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)

            # Process camera frame
            ret, frame = self.cap.read()
            if not ret:
                break

            # Process the frame
            frame = cv2.flip(frame, 1)  # Mirror effect
            processed_frame = self.process_frame(frame)

            # Update particle system
            self.particle_system.update()

            # Draw everything
            self.draw_frame(processed_frame)
            self.particle_system.draw(self.screen)
            self.draw_visualization_overlay()

            # Update display
            pygame.display.flip()
            clock.tick(TARGET_FPS)

        self.cleanup()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_SPACE:
                # Toggle visualization mode
                modes = ['normal', 'heat_map', 'skeleton', 'minimalist']
                current_index = modes.index(self.settings.visualization_mode)
                self.settings.visualization_mode = modes[(current_index + 1) % len(modes)]

    def draw_frame(self, frame):
        # Convert frame to Pygame surface
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame_surface = pygame.surfarray.make_surface(frame)
        self.screen.blit(frame_surface, (0, 0))

    def cleanup(self):
        self.cap.release()
        pygame.quit()
        cv2.destroyAllWindows()

def main():
    try:
        # Initialize camera selector with error handling
        camera_selector = CameraSelector()
        available_cameras = camera_selector.get_available_cameras()
        
        if not available_cameras:
            messagebox.showerror("Error", "No cameras were detected. Please check your camera connection and try again.")
            return
        
        camera_index = camera_selector.show_camera_dialog()
        
        if camera_index is None:
            print("No camera selected. Exiting...")
            return

        # Initialize and run the HUD
        hud = GestureControlledHUD(camera_index)
        hud.run()
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        messagebox.showerror("Error", error_msg)
        
    finally:
        pygame.quit()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()