import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants for Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle System Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Particle Class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.size = random.randint(2, 4)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def move(self, gravity_points):
        # Update velocity based on gravity points
        for gx, gy in gravity_points:
            dx = gx - self.x
            dy = gy - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist != 0:
                force = 100 / (dist ** 2)
                self.vx += force * (dx / dist)
                self.vy += force * (dy / dist)

        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Boundary conditions
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -0.9
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -0.9

        # Keep particle within screen bounds
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Create a list of particles
particles = [Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(1000)]

# Main loop
running = True
gravity_points = []
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button creates gravity points
                gravity_points.append(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[2]:  # Right mouse button for wind effect
                mx, my = pygame.mouse.get_pos()
                for particle in particles:
                    dx = particle.x - mx
                    dy = particle.y - my
                    dist = math.sqrt(dx ** 2 + dy ** 2)
                    if dist < 100:
                        particle.vx += dx / dist
                        particle.vy += dy / dist

    # Update and draw particles
    for particle in particles:
        particle.move(gravity_points)
        particle.draw(screen)

    # Draw gravity points
    for gx, gy in gravity_points:
        pygame.draw.circle(screen, WHITE, (gx, gy), 5)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
