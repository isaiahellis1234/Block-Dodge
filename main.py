import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()
pygame.font.init()

font = pygame.font.SysFont(None, 30)

# Set up the window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Dodge")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_size = 50
player_speed = 5
player_x = WIDTH // 2
player_y = HEIGHT // 2
BULLET_SPD = 3

timer = 0

# Game state
score = 0
player_health = 100
player_max_health = 100
blocks = []

#POWER UPS
spd_pwu = [] # SPEED POWERUP

PLAYERSPD = 5

spawn_enemies = True

max_restart_timer = 200
restart_timer = max_restart_timer

min_health = 90

# Function to reset the game state
def reset_game():
    global player_speed
    global spawn_enemies
    global player_x, player_y, player_health, score, blocks
    player_speed = 5
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    player_health = player_max_health
    score = 0
    blocks = []
    spawn_enemies = True

def enemy_spawner():
    global timer
    if spawn_enemies == True:
        timer += 1
        if timer >= random.randint(50, 150):
            rand_int = random.randint(0, WIDTH - 50)
            rand_size = random.randint(20, 50)
            block = pygame.Rect(rand_int, 0, rand_size, rand_size)
            blocks.append(block)
            timer = 0
        

def key_presses():
    global player_x, player_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed


def draw_health_bar(surface, x, y, width, height, health, max_health):
    # Calculate health ratio
    ratio = health / max_health

    # Background bar (gray)
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))

    # Health bar color (green to red)
    if ratio > 0.5:
        color = (0, 255, 0)  # Green
    elif ratio > 0.2:
        color = (255, 165, 0)  # Orange
    else:
        color = (255, 0, 0)  # Red

    # Foreground bar (colored portion)
    pygame.draw.rect(surface, color, (x, y, width * ratio, height))

# Main game loop
clock = pygame.time.Clock()  # Create a clock object to control FPS
running = True
while running:
    clock.tick(60)  # Limit FPS to 60

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_t:  # Press 'T' to restart the game
                print("Game Restarting...")
                reset_game()  # Reset the game state
    if player_health > min_health:
        score += 1

    # Get key presses for player movement
    key_presses()

    game_over_text = font.render("Game Over! Score: " + str(score), True, BLACK)
    restart_over_text = font.render("Restart in: " + str(restart_timer), True, BLACK)


    # Create the player rectangle
    player = pygame.Rect(player_x, player_y, 35, 35)

    # Fill the screen with blue (background color)
    window.fill(BLUE)

    # Draw player rectangle
    pygame.draw.rect(window, WHITE, player)

    # Lists to hold blocks and bullets that should be removed
    blocks_to_remove = []
    bullets_to_remove = []

    # Check for player collisions with blocks
    if blocks:  # Only loop if there are blocks to check
        for block1 in blocks[:]:  # Iterate over a copy of the list
            pygame.draw.rect(window, RED, block1)
            block1.y += BULLET_SPD

            if player.colliderect(block1):  # Check if player collides with block
                print("Got hit!")
                player_health -= 5  # Decrease health by 5 per collision 
                if player_health <= 0:  # Ensure health doesn't go below 0
                    player_health = 0
                blocks_to_remove.append(block1)  # Mark block for removal

            # Remove block if it reaches the bottom
            if block1.y >= HEIGHT:
                blocks_to_remove.append(block1)  # Mark block for removal

    # Remove blocks and bullets after processing
    for block1 in blocks_to_remove:
        blocks.remove(block1)

    if player_health <= min_health:
        spawn_enemies = False
        blocks.clear()
        player_speed = 0
        restart_timer -= 1
        window.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2))
        window.blit(restart_over_text, (WIDTH / 2 - restart_over_text.get_width() / 2, HEIGHT / 2 + 100))
        if restart_timer <= 0:
            reset_game()
            restart_timer = max_restart_timer
        

    # Draw health bar
    draw_health_bar(window, 10, 10, 200, 20, player_health, player_max_health)

    enemy_spawner()

    # Display the score

    score_text = font.render(str(score), True, BLACK)
    if player_health > min_health:
        window.blit(score_text, (100, 100))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
