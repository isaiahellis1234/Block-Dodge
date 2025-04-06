import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Dodge")

# Set up colors
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (255, 0, 0)

# Player settings
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

BULLET_SPD = 3

blocks = []

# Main game loop
running = True
while running:
    pygame.time.delay(16)  # ~60 FPS
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Optional: press ESC to quit
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

       # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_p]:
        rand_int = random.randint(0, WIDTH - 50)
        rand_size = random.randint(20, 50)
        block = pygame.Rect(rand_int, 0, rand_size, rand_size)
        blocks.append(block)
    # Fill the screen with blue
    window.fill(BLUE)
    pygame.draw.rect(window, RED, (player_x, player_y, player_size, player_size))  # Draw player
    for block1 in blocks:
        pygame.draw.rect(window, RED, block1)
        block1.y += BULLET_SPD
        if block1.y >= 400:
            blocks.remove(block1)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

