import cv2
import mediapipe as mp
import pygame
import os
import sys
import numpy as np
import tkinter as tk
from tkinter import ttk
import random
from enum import Enum
from colorsys import hsv_to_rgb
from tkinter import colorchooser
from tkinter import messagebox
import PIL.Image, PIL.ImageTk
import pygame.surfarray
from PIL import ImageDraw

class DrawMode(Enum):
    NONE = 0
    PAINT = 1
    ERASE = 2

class UIButton:
    def __init__(self, x, y, width, height, color, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.active = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.active:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        # Draw text
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class UISlider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x, y, 20, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.text = text
        self.active = False
        self.update_handle_position()
    
    def update_handle_position(self):
        val_range = self.max_val - self.min_val
        pos = ((self.value - self.min_val) / val_range) * (self.rect.width - 20)
        self.handle_rect.x = self.rect.x + pos
        
    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            rel_x = pos[0] - self.rect.x
            self.value = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
            self.value = max(self.min_val, min(self.max_val, self.value))
            self.update_handle_position()
            return True
        return False

    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, (70, 70, 70), self.rect)
        pygame.draw.rect(surface, (120, 120, 120), self.handle_rect)
        
        # Draw text and value
        font = pygame.font.SysFont(None, 20)
        text_surface = font.render(f"{self.text}: {int(self.value)}", True, (255, 255, 255))
        surface.blit(text_surface, (self.rect.x, self.rect.y - 20))

class ColorPicker:
    def __init__(self, parent, width=200, height=100, callback=None):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="x", padx=5, pady=5)
        
        self.callback = callback
        
        # Create canvas for color gradient
        self.canvas = tk.Canvas(self.frame, width=width, height=height)
        self.canvas.pack(fill="x", padx=5, pady=5)
        
        # Create gradient image
        self.width = width
        self.height = height
        self.create_gradient()
        
        # Selected color display
        self.color_display = tk.Canvas(self.frame, width=50, height=25)
        self.color_display.pack(pady=5)
        
        # Bind click event
        self.canvas.bind('<Button-1>', self.on_click)
        self.selected_color = (255, 0, 0)  # Default red
        self.update_color_display()

    def create_gradient(self):
        # Create PIL image for gradient
        image = PIL.Image.new('RGB', (self.width, self.height))
        draw = PIL.ImageDraw.Draw(image)
        
        # Draw gradient
        for x in range(self.width):
            for y in range(self.height):
                hue = x / self.width
                sat = 1.0
                val = 1.0 - (y / self.height)
                rgb = tuple(int(c * 255) for c in hsv_to_rgb(hue, sat, val))
                draw.point((x, y), fill=rgb)
        
        # Convert to PhotoImage and display
        self.gradient = PIL.ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.gradient, anchor="nw")

    def on_click(self, event):
        # Get color at clicked position
        x = event.x
        y = event.y
        hue = x / self.width
        sat = 1.0
        val = 1.0 - (y / self.height)
        self.selected_color = tuple(int(c * 255) for c in hsv_to_rgb(hue, sat, val))
        self.update_color_display()
        
        # Call callback when color changes
        if self.callback:
            self.callback(self.selected_color)

    def update_color_display(self):
        # Update color display
        self.color_display.delete("all")
        self.color_display.configure(bg='#{:02x}{:02x}{:02x}'.format(*self.selected_color))

    def get_color(self):
        return self.selected_color

class UIPanel:
    def __init__(self, width, height):
        # Increase panel height for better spacing
        panel_height = 200  # Increased from 160
        self.surface = pygame.Surface((width, panel_height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(0, height - panel_height))
        
        # Improved layout parameters
        button_width = 100  # Increased from 80
        button_height = 40
        spacing = 20       # Increased from 15
        section_spacing = 40  # New spacing between sections
        
        # Left margin
        x = spacing * 2
        y = spacing * 2   # Increased top margin

        # Main control buttons - First row
        self.buttons = [
            UIButton(x, y, button_width, button_height, (100, 100, 100), "Paint", "paint"),
            UIButton(x + (button_width + spacing), y, button_width, button_height, (100, 100, 100), "Erase", "erase"),
            UIButton(x + (button_width + spacing) * 2, y, button_width, button_height, (100, 100, 100), "Clear", "clear"),
        ]

        # Add trails button on second row
        trails_x = x
        trails_y = y + button_height + spacing
        self.buttons.append(
            UIButton(trails_x, trails_y, button_width, button_height, (100, 100, 100), "Trails", "toggle_trails")
        )

        # Add color picker - Positioned on the right side
        color_picker_x = width - 200 - spacing * 2  # Right aligned with margin
        color_picker_y = y
        self.color_picker = ColorPicker(color_picker_x, color_picker_y, 150, button_height * 2)

        # Add sliders - Positioned in the middle
        slider_width = 250  # Increased from 200
        slider_x = x + (button_width + spacing) * 3 + section_spacing
        slider_y = y + 5  # Align with buttons
        
        self.brush_slider = UISlider(slider_x, slider_y, slider_width, 20, 1, 30, 8, "Brush Size")
        self.trail_slider = UISlider(slider_x, slider_y + 40, slider_width, 20, 1, 20, 5, "Trail Length")

        # Section labels
        self.sections = [
            ("Tools", (x, y - 25)),
            ("Adjustments", (slider_x, y - 25)),
            ("Color", (color_picker_x, y - 25))
        ]

        self.trails_enabled = True
        self.active_tool = None

    def draw(self, screen):
        # Draw panel background with gradient
        self.surface.fill((30, 30, 30, 240))
        
        # Draw section labels
        font = pygame.font.SysFont(None, 24)
        for label, pos in self.sections:
            text_surface = font.render(label, True, (200, 200, 200))
            self.surface.blit(text_surface, pos)
        
        # Draw divider lines between sections
        for i in range(1, len(self.sections)):
            x = self.sections[i][1][0] - 20
            pygame.draw.line(self.surface, (100, 100, 100), 
                           (x, 10), 
                           (x, self.rect.height - 40), 
                           2)
        
        # Draw buttons with improved visual feedback
        for button in self.buttons:
            button.draw(self.surface)
            if button.active:
                pygame.draw.rect(self.surface, (0, 255, 0), button.rect, 2)

        # Draw color picker
        self.color_picker.draw(self.surface)
        
        # Draw sliders
        self.brush_slider.draw(self.surface)
        self.trail_slider.draw(self.surface)
        
        # Draw mode indicator at the bottom
        mode_text = f"Active Mode: {self.active_tool or 'None'}"
        text_surface = font.render(mode_text, True, (255, 255, 255))
        self.surface.blit(text_surface, (20, self.rect.height - 30))

        screen.blit(self.surface, self.rect)

    def handle_click(self, pos):
        relative_pos = (pos[0], pos[1] - self.rect.y)
        
        # Check color picker first
        if self.color_picker.handle_click(relative_pos):
            return ("color", self.color_picker.selected_color)
            
        # Check sliders
        if self.brush_slider.handle_click(relative_pos):
            return ("brush_size", self.brush_slider.value)
        if self.trail_slider.handle_click(relative_pos):
            return ("trail_length", self.trail_slider.value)
            
        # Check buttons
        for button in self.buttons:
            if button.rect.collidepoint(relative_pos):
                if button.action == "toggle_trails":
                    self.trails_enabled = not self.trails_enabled
                    button.active = self.trails_enabled
                    return ("trails", self.trails_enabled)
                return button.action
        return None

class CameraSelector:
    def __init__(self):
        self.selected_camera = 0
        self.dialog = None

    def get_available_cameras(self):
        """Find available camera devices"""
        available_cameras = []
        max_cameras = 10  # Check up to 10 cameras
        
        for i in range(max_cameras):
            try:
                cap = cv2.VideoCapture(i, cv2.CAP_ANY)  # Try any available API
                if cap.isOpened():
                    ret, _ = cap.read()
                    if ret:
                        # Test if camera is actually working
                        available_cameras.append(i)
                    cap.release()
            except Exception as e:
                print(f"Error checking camera {i}: {e}")
                continue
                
        if not available_cameras:
            print("No cameras found!")
        else:
            print(f"Found cameras at indices: {available_cameras}")
            
        return available_cameras

    def show_camera_dialog(self):
        """Show camera selection dialog"""
        # Get available cameras before creating dialog
        cameras = self.get_available_cameras()
        if not cameras:
            messagebox.showerror("Error", "No cameras found! Please check your camera connection.")
            return None
            
        self.dialog = tk.Toplevel()
        self.dialog.title("Select Camera")
        self.dialog.transient()
        self.dialog.grab_set()

        # Center window
        window_width = 300
        window_height = 150
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')

        frame = ttk.Frame(self.dialog, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.selected_camera = None

        ttk.Label(frame, text="Select camera:").grid(row=0, column=0, pady=5)
        camera_var = tk.StringVar(value=f"Camera {cameras[0]}")
        camera_combo = ttk.Combobox(frame, textvariable=camera_var, state="readonly")
        camera_combo['values'] = [f"Camera {i}" for i in cameras]
        camera_combo.grid(row=1, column=0, pady=5)
        camera_combo.current(0)  # Select first camera by default

        def on_select():
            selected_index = camera_combo.current()
            if selected_index >= 0:
                self.selected_camera = cameras[selected_index]
            else:
                self.selected_camera = cameras[0]
            self.dialog.destroy()

        ttk.Button(frame, text="Start", command=on_select).grid(row=2, column=0, pady=20)

        # Wait for dialog to close
        self.dialog.wait_window()
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

class TrailPoint:
    def __init__(self, position, color=(255, 255, 255)):
        self.position = position
        self.color = color
        self.alpha = 255
        self.fade_speed = 5

    def update(self):
        self.alpha = max(0, self.alpha - self.fade_speed)

    def is_alive(self):
        return self.alpha > 0

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
        pygame.display.setCaption("Gesture Visualization")

        self.running = True
        self.particles = []
        self.trails = []  # Add this line
        self.trail_color = (128, 0, 255)  # Purple trail color
        
        # Colors for hand landmarks and connections
        self.landmark_color = (0, 255, 255)  # Cyan for landmarks
        self.connection_color = (255, 255, 0)  # Yellow for connections

        self.draw_mode = DrawMode.NONE
        self.draw_color = (255, 0, 0)  # Default red
        self.brush_size = 8  # Increased brush size
        self.trail_max_length = 150  # Add this line
        self.trails_enabled = True    # Add this line
        self.ui_panel = UIPanel(self.window_width, self.window_height)
        self.canvas_surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)

    def handle_ui_action(self, action):
        try:
            if isinstance(action, tuple):
                action_type, value = action
                if action_type == "color":
                    self.draw_color = value
                    self.draw_mode = DrawMode.PAINT
                elif action_type == "brush_size":
                    self.brush_size = int(value)
                elif action_type == "trail_length":
                    self.trail_max_length = int(value)
                elif action_type == "trails":
                    self.trails_enabled = value
            elif action == "paint":
                self.draw_mode = DrawMode.PAINT
                self.ui_panel.active_tool = "Paint"
            elif action == "erase":
                self.draw_mode = DrawMode.ERASE
                self.ui_panel.active_tool = "Erase"
            elif action == "clear":
                self.canvas_surface.fill((0, 0, 0, 0))
            
            # Update button states
            for button in self.ui_panel.buttons:
                button.active = (
                    (button.action == "paint" and self.draw_mode == DrawMode.PAINT) or
                    (button.action == "erase" and self.draw_mode == DrawMode.ERASE) or
                    (button.action == "toggle_trails" and self.trails_enabled)
                )
        except Exception as e:
            print(f"Error handling UI action: {e}")

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

        # Add trails for each fingertip
        for tip_id in [4, 8, 12, 16, 20]:  # fingertip indices
            tip = hand_landmarks.landmark[tip_id]
            x = int(tip.x * self.window_width)
            y = int(tip.y * self.window_height)
            self.trails.append(TrailPoint((x, y), self.trail_color))

    def run(self):
        clock = pygame.time.Clock()
        trail_surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.ui_panel.rect.collidepoint(mouse_pos):
                            action = self.ui_panel.handle_click(mouse_pos)
                            if action:
                                self.handle_ui_action(action)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        # Reset any active dragging
                        pass
                    elif event.type == pygame.MOUSEMOTION:
                        if pygame.mouse.get_pressed()[0]:  # Left button
                            mouse_pos = pygame.mouse.get_pos()
                            if self.ui_panel.rect.collidepoint(mouse_pos):
                                action = self.ui_panel.handle_click(mouse_pos)
                                if action:
                                    self.handle_ui_action(action)
                
                # Read and process frame
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read frame from camera.")
                    break

                # Flip frame horizontally for natural movement
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)

                # Clear main screen with black background
                self.screen.fill((0, 0, 0))
                trail_surface.fill((0, 0, 0, 0))  # Clear trail surface with transparency

                # Update and draw trails
                new_trails = []
                for trail in self.trails:
                    trail.update()
                    if trail.is_alive():
                        pygame.draw.circle(trail_surface, 
                                        (*self.trail_color, trail.alpha),
                                        trail.position,
                                        3)  # Trail point size
                        new_trails.append(trail)
                self.trails = new_trails

                # Limit the number of trail points
                if len(self.trails) > self.trail_max_length:  # Adjust this value to control trail length
                    self.trails = self.trails[-self.trail_max_length:]

                # Draw trails and particles
                self.screen.blit(trail_surface, (0, 0))

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

                # Draw on canvas if in paint mode
                if results.multi_hand_landmarks and self.draw_mode != DrawMode.NONE:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Use index finger tip for drawing (landmark 8)
                        tip = hand_landmarks.landmark[8]
                        x = int(tip.x * self.window_width)
                        y = int(tip.y * self.window_height)
                        
                        if self.draw_mode == DrawMode.PAINT:
                            pygame.draw.circle(self.canvas_surface, self.draw_color, (x, y), self.brush_size)
                        elif self.draw_mode == DrawMode.ERASE:
                            pygame.draw.circle(self.canvas_surface, (0, 0, 0, 0), (x, y), self.brush_size * 2)

                # Draw layers in order
                self.screen.blit(self.canvas_surface, (0, 0))  # Draw canvas first
                self.screen.blit(trail_surface, (0, 0))        # Draw trails
                
                # Draw hand landmarks and particles
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.draw_landmarks(hand_landmarks)
                        # ...existing particle code...

                # Draw UI panel last (make sure it's always on top)
                self.ui_panel.draw(self.screen)
                pygame.display.flip()
                clock.tick(60)  # Increased to 60 FPS for smoother animation

            except Exception as e:
                print(f"Error in main loop: {e}")
                continue

        self.cap.release()
        pygame.quit()

class ImageGestureApp:
    def __init__(self):
        # Initialize Tkinter root first
        self.root = tk.Tk()
        self.root.title("Gesture Drawing")
        self.root.geometry("1200x800")
        
        # Initialize Pygame without display
        pygame.init()
        
        # Initialize all variables first
        self.sidebar_width = 250  # Add this line
        self.sidebar_expanded = True
        self.brush_size = 8
        self.trail_length = 5
        self.draw_mode = DrawMode.NONE
        self.draw_color = (255, 0, 0)  # Default red

        # Initialize camera variables
        self.camera_active = False
        self.cap = None
        self.photo = None
        self.camera_index = None
        
        # Initialize UI state variables
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        self.trail_length_var = tk.IntVar(value=self.trail_length)

        # Add camera view mode flag
        self.show_camera = False  # Start with black screen
        
        # Setup UI components
        self.setup_main_container()
        self.setup_sidebar()
        self.setup_camera_controls()

        # Add MediaPipe initialization
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=2
        )
        
        # Initialize drawing surface
        self.canvas_surface = None
        self.trail_surface = None

    def setup_main_container(self):
        # Main container 
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar container with toggle
        self.sidebar_container = ttk.Frame(self.main_container)
        self.sidebar_container.pack(side=tk.LEFT, fill=tk.Y)
        
        # Toggle button
        self.toggle_btn = ttk.Button(self.sidebar_container, 
                                   text="◀", width=2,
                                   command=self.toggle_sidebar)
        self.toggle_btn.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sidebar
        self.sidebar = ttk.Frame(self.sidebar_container, width=self.sidebar_width)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Content area
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Camera canvas
        self.camera_canvas = tk.Canvas(self.content_frame, bg='black')
        self.camera_canvas.pack(fill=tk.BOTH, expand=True)

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.pack_forget()
            self.toggle_btn.configure(text="▶")
        else:
            self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
            self.toggle_btn.configure(text="◀")
        self.sidebar_expanded = not self.sidebar_expanded
        
        # Force canvas surface recreation on next frame
        self.canvas_surface = None
        self.trail_surface = None

    def setup_sidebar(self):
        # Tools Section
        tools_frame = ttk.LabelFrame(self.sidebar, text="Tools")
        tools_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(tools_frame, text="Paint", command=self.activate_paint).pack(fill="x", pady=2)
        ttk.Button(tools_frame, text="Erase", command=self.activate_erase).pack(fill="x", pady=2)
        ttk.Button(tools_frame, text="Clear", command=self.clear_canvas).pack(fill="x", pady=2)

        # Adjustments Section
        adjust_frame = ttk.LabelFrame(self.sidebar, text="Adjustments")
        adjust_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(adjust_frame, text="Brush Size").pack()
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        ttk.Scale(adjust_frame, from_=1, to=30, variable=self.brush_size_var,
                 command=self.update_brush_size).pack(fill="x")

        ttk.Label(adjust_frame, text="Trail Length").pack()
        self.trail_length_var = tk.IntVar(value=self.trail_length)
        ttk.Scale(adjust_frame, from_=1, to=20, variable=self.trail_length_var,
                 command=self.update_trail_length).pack(fill="x")

        # Color Section with new ColorPicker
        color_frame = ttk.LabelFrame(self.sidebar, text="Color")
        color_frame.pack(fill="x", padx=5, pady=5)
        self.color_picker = ColorPicker(color_frame, callback=self.update_color)

    def activate_paint(self):
        self.draw_mode = DrawMode.PAINT
        
    def activate_erase(self):
        self.draw_mode = DrawMode.ERASE
        
    def clear_canvas(self):
        if hasattr(self, 'canvas_surface'):
            self.canvas_surface.fill((0, 0, 0, 0))
            
    def update_brush_size(self, value):
        self.brush_size = int(float(value))
        
    def update_trail_length(self, value):
        self.trail_length = int(float(value))
        
    def pick_color(self):
        color = colorchooser.askcolor(title="Choose Color", 
                                    color=self.draw_color)
        if color[1]:
            self.draw_color = tuple(int(c) for c in color[0])
            self.color_button.configure(bg=color[1])

    def setup_camera_controls(self):
        camera_frame = ttk.LabelFrame(self.sidebar, text="Camera Controls")
        camera_frame.pack(fill="x", padx=5, pady=5)

        self.camera_status = ttk.Label(camera_frame, text="Status: No Camera")
        self.camera_status.pack(fill="x", padx=5, pady=2)

        self.select_camera_btn = ttk.Button(camera_frame,
                                          text="Select Camera",
                                          command=self.select_camera)
        self.select_camera_btn.pack(fill="x", padx=5, pady=2)
        
        # Add camera view toggle button
        self.camera_view_btn = ttk.Button(camera_frame,
                                        text="Show Camera",
                                        command=self.toggle_camera_view)
        self.camera_view_btn.pack(fill="x", padx=5, pady=2)

    def toggle_camera_view(self):
        self.show_camera = not self.show_camera
        self.camera_view_btn.configure(
            text="Hide Camera" if self.show_camera else "Show Camera"
        )

    def select_camera(self):
        if self.camera_active:
            self.stop_camera()  # Stop current camera if active

        try:
            camera_selector = CameraSelector()
            selected_camera = camera_selector.show_camera_dialog()

            if selected_camera is not None:
                print(f"Attempting to open camera {selected_camera}")
                # Test camera before proceeding
                test_cap = cv2.VideoCapture(selected_camera)
                if test_cap.isOpened():
                    ret, _ = test_cap.read()
                    test_cap.release()
                    
                    if ret:
                        self.camera_index = selected_camera
                        self.camera_status.configure(
                            text=f"Status: Camera {selected_camera} selected")
                        # Initialize surfaces to None to force recreation
                        self.canvas_surface = None
                        self.trail_surface = None
                        self.root.after(100, self.start_camera)  # Start camera after a short delay
                    else:
                        messagebox.showerror("Error", f"Camera {selected_camera} failed to provide video feed")
                else:
                    messagebox.showerror("Error", f"Failed to open camera {selected_camera}")
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting camera: {str(e)}")

    def start_camera(self):
        if self.camera_index is None:
            messagebox.showwarning("Warning", "Please select a camera first")
            return

        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open camera")
            return

        self.camera_active = True
        self.camera_status.configure(text=f"Status: Camera {self.camera_index} active")
        self.update_camera()

    def stop_camera(self):
        self.camera_active = False
        self.camera_status.configure(
            text=f"Status: Camera {self.camera_index} stopped")
        if self.cap:
            self.cap.release()
            self.cap = None
        # Clear canvas
        self.camera_canvas.delete("all")

    def update_camera(self):
        if not self.camera_active or not self.cap:
            return
            
        try:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame")
                self.stop_camera()
                return
                
            frame = cv2.flip(frame, 1)
            
            # Process frame with MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            # Get canvas dimensions
            canvas_width = self.camera_canvas.winfo_width()
            canvas_height = self.camera_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                try:
                    # Create base frame (black or camera view)
                    if self.show_camera:
                        frame_array = cv2.resize(rgb_frame, (canvas_width, canvas_height))
                    else:
                        frame_array = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
                    
                    # Draw hand landmarks directly on frame_array
                    if results.multi_hand_landmarks:
                        print("Hand landmarks detected!")  # Debug print
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Draw connections between landmarks
                            for connection in self.mp_hands.HAND_CONNECTIONS:
                                start_idx = connection[0]
                                end_idx = connection[1]
                                
                                start_pos = hand_landmarks.landmark[start_idx]
                                end_pos = hand_landmarks.landmark[end_idx]
                                
                                start_x = int(start_pos.x * canvas_width)
                                start_y = int(start_pos.y * canvas_height)
                                end_x = int(end_pos.x * canvas_width)
                                end_y = int(end_pos.y * canvas_height)
                                
                                # Draw connection line using cv2
                                cv2.line(frame_array, 
                                       (start_x, start_y), 
                                       (end_x, end_y),
                                       (255, 255, 0), 2)
                            
                            # Draw landmarks
                            for landmark in hand_landmarks.landmark:
                                x = int(landmark.x * canvas_width)
                                y = int(landmark.y * canvas_height)
                                # Draw circles using cv2
                                cv2.circle(frame_array, (x, y), 4, (0, 255, 255), -1)
                                cv2.circle(frame_array, (x, y), 4, (255, 255, 255), 1)
                    
                    # Initialize surfaces if needed
                    if self.canvas_surface is None:
                        self.canvas_surface = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)
                    
                    # Handle drawing if in paint mode
                    if results.multi_hand_landmarks and self.draw_mode == DrawMode.PAINT:
                        for hand_landmarks in results.multi_hand_landmarks:
                            tip = hand_landmarks.landmark[8]  # Index fingertip
                            x = int(tip.x * canvas_width)
                            y = int(tip.y * canvas_height)
                            cv2.circle(self.canvas_surface, (x, y), 
                                     self.brush_size, (*self.draw_color, 255), -1)
                    
                    # Combine frame and canvas
                    frame_rgba = cv2.cvtColor(frame_array, cv2.COLOR_RGB2RGBA)
                    final_frame = cv2.addWeighted(frame_rgba, 1, self.canvas_surface, 1, 0)
                    
                    # Convert to PIL Image
                    image = PIL.Image.fromarray(final_frame)
                    
                    # Convert to PhotoImage and display
                    self.photo = PIL.ImageTk.PhotoImage(image=image)
                    self.camera_canvas.delete("all")
                    self.camera_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                
                except Exception as e:
                    print(f"Error in camera update: {e}")
                    print(f"Error details: {str(e)}")  # More detailed error info
                
            # Continue update loop
            if self.camera_active:  # Only schedule if still active
                self.root.after(16, self.update_camera)
                
        except Exception as e:
            print(f"Error in camera update: {e}")
            self.stop_camera()

    def update_color(self, color):
        """Update the drawing color and switch to paint mode"""
        self.draw_color = color
        self.draw_mode = DrawMode.PAINT  # Automatically switch to paint mode when color is selected
        print(f"Color updated to: {color}")  # Debug print

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageGestureApp()
    app.run()