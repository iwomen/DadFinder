import pygame
import random
import sys
import os
from pygame.locals import *

# ✅ 加入这个函数，处理打包后的资源路径
def resource_path(relative_path):
    """打包后能找到资源的通用方式"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dad Finder')

# Clock to control the game's frame rate
clock = pygame.time.Clock()

# Load images and resize to 40x40 pixels
player_img = pygame.image.load(resource_path('img/son.png'))
player_img = pygame.transform.scale(player_img, (40, 40))

enemy_img = pygame.image.load(resource_path('img/dad.png'))
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

goal_img = pygame.image.load(resource_path('img/kim.png'))
goal_img = pygame.transform.scale(goal_img, (40, 40))

# Colors
DARK_BACKGROUND = (10, 10, 10)
RETRO_GREEN = (0, 255, 0)

# Font
font = pygame.font.SysFont('Courier', 24)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 8

    def update(self, keys_pressed):
        if keys_pressed[K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN]:
            self.rect.y += self.speed

        # Keep the player within the screen boundaries
        self.rect.clamp_ip(screen.get_rect())

# Enemy class (kim)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(
            x=random.randint(0, SCREEN_WIDTH - 40),
            y=random.randint(0, SCREEN_HEIGHT - 40)
        )
        self.speed_x = random.choice([-4, -3, -2, 2, 3, 4])
        self.speed_y = random.choice([-4, -3, -2, 2, 3, 4])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

# Goal class (dad)
class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = goal_img
        self.rect = self.image.get_rect(
            x=random.randint(0, SCREEN_WIDTH - 40),
            y=random.randint(0, SCREEN_HEIGHT - 40)
        )
        self.speed_x = random.choice([-4, -3, -2, 2, 3, 4])
        self.speed_y = random.choice([-4, -3, -2, 2, 3, 4])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

# Groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
goal_group = pygame.sprite.Group()

player = Player()
player_group.add(player)

# Game variables
game_over = False
game_won = False
start_time = pygame.time.get_ticks()
enemy_spawn_time = start_time
goal_spawned = False

# Display instructions before the game starts
def display_instructions():
    screen.fill(DARK_BACKGROUND)
    instructions = [
        "Instructions:",
        "Use arrow keys to move the son icon.",
        "Avoid the kim icons that spawn every second.",
        "After 3 seconds, an dad icon will appear.",
        "Touch the dad icon to win.",
        "Press any key to start."
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, RETRO_GREEN)
        screen.blit(text, (50, 100 + i * 30))
    pygame.display.flip()

    # Wait for the player to press a key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                waiting = False
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

display_instructions()

# Main game loop
while True:
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000  # in seconds
    timer_text = font.render(f"Time: {int(elapsed_time)}", True, RETRO_GREEN)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not game_won:
        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed)

        # Spawn an enemy every second
        if current_time - enemy_spawn_time >= 1000:
            enemy = Enemy()
            enemy_group.add(enemy)
            enemy_spawn_time = current_time

        # Spawn the goal after 3 seconds
        if not goal_spawned and elapsed_time >= 3:
            goal = Goal()
            goal_group.add(goal)
            goal_spawned = True

        enemy_group.update()
        goal_group.update()

        # Check for collisions with enemies
        if pygame.sprite.spritecollideany(player, enemy_group):
            game_over = True

        # Check for collision with the goal
        if pygame.sprite.spritecollideany(player, goal_group):
            game_won = True

        # Draw everything
        screen.fill(DARK_BACKGROUND)
        player_group.draw(screen)
        enemy_group.draw(screen)
        goal_group.draw(screen)

        # Draw text
        s39_text = font.render("Crying baby Trump", True, RETRO_GREEN)
        screen.blit(s39_text, (10, 10))
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()

    elif game_over:
        # Game over screen
        screen.fill(DARK_BACKGROUND)
        game_over_text = font.render("You Died! Press any key to restart.", True, RETRO_GREEN)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        # Wait for the player to press a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Reset the game
                    game_over = False
                    start_time = pygame.time.get_ticks()
                    enemy_spawn_time = start_time
                    enemy_group.empty()
                    goal_group.empty()
                    goal_spawned = False
                    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    waiting = False
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    elif game_won:
        # Win screen
        screen.fill(DARK_BACKGROUND)
        win_text = font.render("You Win! Press any key to restart.", True, RETRO_GREEN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        # Wait for the player to press a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Reset the game
                    game_won = False
                    start_time = pygame.time.get_ticks()
                    enemy_spawn_time = start_time
                    enemy_group.empty()
                    goal_group.empty()
                    goal_spawned = False
                    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    waiting = False
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
