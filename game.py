import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wario Shart: Tripple Smash!!!")

# Clock
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 80
player_speed = 5

# Player 1 (WASD)
player1_x = WIDTH // 4 - player_width // 2
player1_y = HEIGHT - player_height - 20
player1_color = RED

# Player 2 (Arrow keys)
player2_x = 3 * WIDTH // 4 - player_width // 2
player2_y = HEIGHT - player_height - 20
player2_color = BLUE

# Obstacle settings
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []

# Power-up settings
powerup_width = 30
powerup_height = 30
powerups = []
POWERUP_TYPES = ["speed_boost", "invincibility"]

# Score
score = 0
font = pygame.font.SysFont(None, 35)

# Power-up effects
player1_speed_boost = False
player2_speed_boost = False
player1_invincible = False
player2_invincible = False

# Functions
def draw_player(x, y, color):
    pygame.draw.rect(screen, color, [x, y, player_width, player_height])

def draw_obstacle(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, obstacle_width, obstacle_height])

def draw_powerup(x, y, type):
    color = YELLOW if type == "speed_boost" else GREEN
    pygame.draw.rect(screen, color, [x, y, powerup_width, powerup_height])

def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def game_over():
    game_over_text = font.render("Game Over! Press Q to Quit or R to Restart", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 250, HEIGHT // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    main()

def spawn_obstacle():
    x = random.randint(0, WIDTH - obstacle_width)
    y = -obstacle_height
    obstacles.append([x, y])

def spawn_powerup():
    x = random.randint(0, WIDTH - powerup_width)
    y = -powerup_height
    type = random.choice(POWERUP_TYPES)
    powerups.append([x, y, type])

def check_collision(player_x, player_y, player_width, player_height, obj_x, obj_y, obj_width, obj_height):
    return (player_x < obj_x + obj_width and
            player_x + player_width > obj_x and
            player_y < obj_y + obj_height and
            player_y + player_height > obj_y)

def main():
    global player1_x, player1_y, player2_x, player2_y, score
    global player1_speed_boost, player2_speed_boost, player1_invincible, player2_invincible

    # Reset game state
    player1_x = WIDTH // 4 - player_width // 2
    player1_y = HEIGHT - player_height - 20
    player2_x = 3 * WIDTH // 4 - player_width // 2
    player2_y = HEIGHT - player_height - 20
    score = 0
    obstacles.clear()
    powerups.clear()
    player1_speed_boost = False
    player2_speed_boost = False
    player1_invincible = False
    player2_invincible = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player 1 movement (WASD)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player1_x > 0:
            player1_x -= player_speed * (1.5 if player1_speed_boost else 1)
        if keys[pygame.K_d] and player1_x < WIDTH - player_width:
            player1_x += player_speed * (1.5 if player1_speed_boost else 1)
        if keys[pygame.K_w] and player1_y > 0:
            player1_y -= player_speed * (1.5 if player1_speed_boost else 1)
        if keys[pygame.K_s] and player1_y < HEIGHT - player_height:
            player1_y += player_speed * (1.5 if player1_speed_boost else 1)

        # Player 2 movement (Arrow keys)
        if keys[pygame.K_LEFT] and player2_x > 0:
            player2_x -= player_speed * (1.5 if player2_speed_boost else 1)
        if keys[pygame.K_RIGHT] and player2_x < WIDTH - player_width:
            player2_x += player_speed * (1.5 if player2_speed_boost else 1)
        if keys[pygame.K_UP] and player2_y > 0:
            player2_y -= player_speed * (1.5 if player2_speed_boost else 1)
        if keys[pygame.K_DOWN] and player2_y < HEIGHT - player_height:
            player2_y += player_speed * (1.5 if player2_speed_boost else 1)

        # Spawn obstacles and power-ups
        if random.randint(1, 100) == 1:
            spawn_obstacle()
        if random.randint(1, 200) == 1:
            spawn_powerup()

        # Move obstacles and power-ups
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        for powerup in powerups:
            powerup[1] += obstacle_speed
            if powerup[1] > HEIGHT:
                powerups.remove(powerup)

        # Check for collisions
        for obstacle in obstacles:
            if (not player1_invincible and check_collision(player1_x, player1_y, player_width, player_height, obstacle[0], obstacle[1], obstacle_width, obstacle_height)):
                game_over()
            if (not player2_invincible and check_collision(player2_x, player2_y, player_width, player_height, obstacle[0], obstacle[1], obstacle_width, obstacle_height)):
                game_over()

        for powerup in powerups:
            if check_collision(player1_x, player1_y, player_width, player_height, powerup[0], powerup[1], powerup_width, powerup_height):
                if powerup[2] == "speed_boost":
                    player1_speed_boost = True
                    pygame.time.set_timer(pygame.USEREVENT, 5000)  # 5-second boost
                elif powerup[2] == "invincibility":
                    player1_invincible = True
                    pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # 5-second invincibility
                powerups.remove(powerup)

            if check_collision(player2_x, player2_y, player_width, player_height, powerup[0], powerup[1], powerup_width, powerup_height):
                if powerup[2] == "speed_boost":
                    player2_speed_boost = True
                    pygame.time.set_timer(pygame.USEREVENT + 2, 5000)  # 5-second boost
                elif powerup[2] == "invincibility":
                    player2_invincible = True
                    pygame.time.set_timer(pygame.USEREVENT + 3, 5000)  # 5-second invincibility
                powerups.remove(powerup)

        # Draw everything
        screen.fill(WHITE)
        draw_player(player1_x, player1_y, player1_color)
        draw_player(player2_x, player2_y, player2_color)
        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1])
        for powerup in powerups:
            draw_powerup(powerup[0], powerup[1], powerup[2])
        display_score(score)

        # Update the display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()