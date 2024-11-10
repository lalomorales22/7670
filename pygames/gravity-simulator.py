import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants for Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Planet Class
class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.radius = int(mass ** 0.5)  # Radius depends on mass
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def update_position(self, planets):
        # Calculate gravitational forces from all other planets
        for other in planets:
            if other == self:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist < 1:
                dist = 1  # Prevent division by zero
            force = (self.mass * other.mass) / (dist ** 2)
            acceleration = force / self.mass
            self.vx += acceleration * (dx / dist)
            self.vy += acceleration * (dy / dist)

        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Boundary conditions (wrap around the screen)
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Create a list of planets
planets = [Planet(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(10, 100)) for _ in range(10)]

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button to add a new planet
                mx, my = pygame.mouse.get_pos()
                new_mass = random.randint(10, 100)
                planets.append(Planet(mx, my, new_mass))

    # Update and draw planets
    for planet in planets:
        planet.update_position(planets)
        planet.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
