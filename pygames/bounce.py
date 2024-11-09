import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set mode((WIDTH, HEIGHT))
pygame.display.set caption("Sweet Red Yellow Green Game")

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)

# Ball class
class Ball:
    def   init  (self, x, y, radius, color, dx=0, dy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.dx = -self.dx
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < self.radius + other.radius

# Create balls
red ball = Ball(WIDTH // 2, HEIGHT // 2, 20, RED, 5, 5)
yellow ball = Ball(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 20, YELLOW, 3, 3)
green ball = Ball(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 20, GREEN, 3, 3)

# List to hold smaller balls
small balls = []

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move balls
    red ball.move()
    yellow ball.move()
    green ball.move()

    # Check collisions
    for ball in [yellow ball, green ball]:
        if red ball.collide(ball):
            # Create smaller balls upon collision
            for   in range(5):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 4)
                dx = speed * math.cos(angle)
                dy = speed * math.sin(angle)
                color = random.choice([BLUE, RED, PURPLE])
                small balls.append(Ball(red ball.x, red ball.y, 5, color, dx, dy))

    # Move small balls
    for small ball in small balls:
        small ball.move()

    # Draw everything
    screen.fill(WHITE)
    red ball.draw(screen)
    yellow ball.draw(screen)
    green ball.draw(screen)
    for small ball in small balls:
        small ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()