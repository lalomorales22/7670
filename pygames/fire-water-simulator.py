import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fire and Water Flow Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Fire
BLUE = (0, 0, 255)  # Water

# Grid settings
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

grid = [[None for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

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
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // CELL_SIZE
            grid_y = my // CELL_SIZE
            if event.button == 1:  # Left mouse button places fire
                grid[grid_x][grid_y] = 'fire'
            elif event.button == 3:  # Right mouse button places water
                grid[grid_x][grid_y] = 'water'

    # Update grid
    new_grid = [[grid[x][y] for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 'fire':
                # Fire spreads to adjacent cells if they are empty
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                        if grid[nx][ny] is None:
                            new_grid[nx][ny] = 'fire'
            elif grid[x][y] == 'water':
                # Water blocks fire and spreads slowly
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                        if grid[nx][ny] == 'fire':
                            new_grid[nx][ny] = None
                        elif grid[nx][ny] is None and random.random() < 0.1:
                            new_grid[nx][ny] = 'water'

    grid = new_grid

    # Draw grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 'fire':
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[x][y] == 'water':
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
