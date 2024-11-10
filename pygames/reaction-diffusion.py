import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Constants for Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reaction-Diffusion Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Simulation parameters
DIFF_A = 1.0  # Diffusion rate of substance A
DIFF_B = 0.5  # Diffusion rate of substance B
FEED = 0.055  # Feed rate of substance A
KILL = 0.062  # Kill rate of substance B

# Initialize the grid
A = np.ones((WIDTH, HEIGHT))  # Substance A starts at full concentration
B = np.zeros((WIDTH, HEIGHT))  # Substance B starts at zero concentration

# Function to update the grid based on reaction-diffusion equations
def update_grid(A, B, DA, DB, feed, kill):
    # Calculate Laplacian for A and B
    laplacian_A = (
        np.roll(A, 1, axis=0) + np.roll(A, -1, axis=0) +
        np.roll(A, 1, axis=1) + np.roll(A, -1, axis=1) -
        4 * A
    )
    laplacian_B = (
        np.roll(B, 1, axis=0) + np.roll(B, -1, axis=0) +
        np.roll(B, 1, axis=1) + np.roll(B, -1, axis=1) -
        4 * B
    )

    # Reaction-diffusion equations
    reaction = A * B * B
    A += (DA * laplacian_A - reaction + feed * (1 - A))
    B += (DB * laplacian_B + reaction - (feed + kill) * B)

    # Ensure values stay within bounds
    A = np.clip(A, 0, 1)
    B = np.clip(B, 0, 1)

    return A, B

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button adds substance B
                mx, my = pygame.mouse.get_pos()
                B[mx-10:mx+10, my-10:my+10] = 1  # Add substance B in a small area

    # Update the grid
    A, B = update_grid(A, B, DIFF_A, DIFF_B, FEED, KILL)

    # Draw the grid
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color_value = int((B[x, y] - A[x, y]) * 255)
            color = (max(0, color_value), 0, max(0, -color_value))
            screen.set_at((x, y), color)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
