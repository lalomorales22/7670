import cv2
import mediapipe as mp
import pygame
import sys
import numpy as np
import threading
import time
import pyttsx3  # For voice feedback
import speech_recognition as sr  # For voice commands

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Initialize speech recognizer
recognizer = sr.Recognizer()

class Particle:
    def __init__(self, position):
        self.position = np.array(position, dtype=float)
        self.velocity = np.random.randn(2) * 2
        self.lifetime = np.random.randint(60, 120)
        self.color = [np.random.randint(100, 255) for _ in range(3)]

    def update(self):
        self.position += self.velocity
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0

class GestureControlledHUD:
    def __init__(self, camera_index):
        # Initialize MediaPipe Hands
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

        # Initialize variables for gesture recognition
        self.gesture_history = []
        self.gesture_threshold = 5  # Number of frames to confirm a gesture
        self.current_gesture = None

        # Initialize variables for AR overlays
        self.ar_objects = []  # List to store AR objects

        # Initialize variables for voice feedback
        self.voice_feedback_enabled = True

        # Initialize variables for voice commands
        self.voice_command = None
        self.voice_thread = threading.Thread(target=self.listen_for_voice_commands)
        self.voice_thread.daemon = True
        self.voice_thread.start()

    def listen_for_voice_commands(self):
        """Listen for voice commands in a separate thread"""
        with sr.Microphone() as source:
            while self.running:
                try:
                    audio_data = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    command = recognizer.recognize_google(audio_data)
                    self.voice_command = command.lower()
                    print(f"Voice Command Received: {self.voice_command}")
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    continue

    def process_voice_commands(self):
        """Process voice commands"""
        if self.voice_command:
            if "enable voice feedback" in self.voice_command:
                self.voice_feedback_enabled = True
                self.speak("Voice feedback enabled")
            elif "disable voice feedback" in self.voice_command:
                self.voice_feedback_enabled = False
                self.speak("Voice feedback disabled")
            elif "exit" in self.voice_command or "quit" in self.voice_command:
                self.running = False
            self.voice_command = None

    def speak(self, text):
        """Provide auditory feedback"""
        if self.voice_feedback_enabled:
            tts_engine.say(text)
            tts_engine.runAndWait()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Process voice commands
            self.process_voice_commands()

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
            frame = np.rot90(frame)
            frame_surface = pygame.surfarray.make_surface(frame)

            # Blit the camera frame onto the screen
            self.screen.blit(frame_surface, (0, 0))

            # Draw graphics reacting to hand positions
            self.draw_graphics(hand_positions)

            # Process gestures
            self.process_gestures(hand_positions)

            # Draw AR overlays
            self.draw_ar_overlays()

            # Update particles
            self.update_particles()

            pygame.display.flip()
            clock.tick(30)  # Limit to 30 FPS

        self.cap.release()
        pygame.quit()
        sys.exit()

    def draw_graphics(self, hand_positions):
        """Draw visual effects and feedback"""
        for hand_landmarks in hand_positions:
            index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * self.window_width)
            y = int(index_finger_tip.y * self.window_height)
            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 15)

            # Add particles for visual effect
            self.particles.append(Particle((x, y)))

    def update_particles(self):
        """Update and draw particles"""
        for particle in self.particles[:]:
            particle.update()
            if particle.is_alive():
                pygame.draw.circle(self.screen, particle.color, particle.position.astype(int), 5)
            else:
                self.particles.remove(particle)

    def process_gestures(self, hand_positions):
        """Recognize gestures and trigger actions"""
        if len(hand_positions) == 1:
            hand_landmarks = hand_positions[0]
            fingers = self.get_finger_states(hand_landmarks)
            gesture = self.identify_gesture(fingers)
            self.gesture_history.append(gesture)

            # Keep history within threshold
            if len(self.gesture_history) > self.gesture_threshold:
                self.gesture_history.pop(0)

            # Confirm gesture
            if self.gesture_history.count(gesture) == self.gesture_threshold:
                if gesture != self.current_gesture:
                    self.current_gesture = gesture
                    self.trigger_action(gesture)

    def get_finger_states(self, hand_landmarks):
        """Determine if fingers are up or down"""
        finger_states = []
        landmarks = hand_landmarks.landmark

        # Thumb
        if landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x < landmarks[self.mp_hands.HandLandmark.THUMB_IP].x:
            finger_states.append(1)
        else:
            finger_states.append(0)

        # Fingers
        for tip_id in [self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                       self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                       self.mp_hands.HandLandmark.RING_FINGER_TIP,
                       self.mp_hands.HandLandmark.PINKY_TIP]:
            if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                finger_states.append(1)
            else:
                finger_states.append(0)
        return finger_states

    def identify_gesture(self, fingers):
        """Identify gesture based on finger states"""
        if fingers == [0, 1, 0, 0, 0]:
            return "pointing"
        elif fingers == [0, 1, 1, 1, 1]:
            return "open_hand"
        elif fingers == [0, 0, 0, 0, 0]:
            return "fist"
        elif fingers == [1, 1, 0, 0, 1]:
            return "spiderman"
        else:
            return "unknown"

    def trigger_action(self, gesture):
        """Trigger action based on gesture"""
        print(f"Gesture recognized: {gesture}")
        self.speak(f"Gesture recognized: {gesture}")
        if gesture == "fist":
            self.toggle_ar_object()
        elif gesture == "open_hand":
            self.change_ar_object()
        elif gesture == "pointing":
            self.select_ar_object()
        # Add more gesture actions as needed

    def draw_ar_overlays(self):
        """Draw AR overlays on the screen"""
        for obj in self.ar_objects:
            pygame.draw.rect(self.screen, (255, 0, 0), obj, 2)

    def toggle_ar_object(self):
        """Toggle AR object visibility"""
        if self.ar_objects:
            self.ar_objects = []
        else:
            rect = pygame.Rect(self.window_width // 4, self.window_height // 4,
                               self.window_width // 2, self.window_height // 2)
            self.ar_objects.append(rect)

    def change_ar_object(self):
        """Change AR object properties"""
        if self.ar_objects:
            for obj in self.ar_objects:
                obj.width = np.random.randint(50, self.window_width // 2)
                obj.height = np.random.randint(50, self.window_height // 2)
                obj.x = np.random.randint(0, self.window_width - obj.width)
                obj.y = np.random.randint(0, self.window_height - obj.height)

    def select_ar_object(self):
        """Select and interact with AR object"""
        # Placeholder for selecting AR objects
        pass

if __name__ == "__main__":
    # Prompt the user to enter the camera index
    try:
        camera_index = int(input("Enter the camera index (default is 0): ") or 0)
    except ValueError:
        camera_index = 0

    hud = GestureControlledHUD(camera_index)
    hud.run()
