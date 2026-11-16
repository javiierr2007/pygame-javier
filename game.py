import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Pygame")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 36)

# Clock
clock = pygame.time.Clock()

# --- CLASSES ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5  # Initial speed

    def update(self, keys, up_key, down_key, left_key, right_key):
        # Movement
        if keys[left_key]:
            self.rect.x -= self.speed
        if keys[right_key]:
            self.rect.x += self.speed
        if keys[up_key]:
            self.rect.y -= self.speed
        if keys[down_key]:
            self.rect.y += self.speed

        # RETO 1: Player boundaries (Simple clamp logic)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # RETO 2: Random obstacle sizes between 20 and 70 pixels
        size = random.randint(20, 70)
        self.image = pygame.Surface((size, size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
        # Keep obstacle completely inside the window width
        self.rect.x = random.randint(0, SCREEN_WIDTH - size)
        self.rect.y = -size
        self.speed_y = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed_y
        # Remove if it goes off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# --- GAME VARIABLES ---
# Jugador 1 (Azul) se mueve con las FLECHAS
player1 = Player(300, 500, BLUE)
# Jugador 2 (Verde) se mueve con WASD
player2 = Player(500, 500, GREEN)

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

obstacles = pygame.sprite.Group()

# Timers and Spawns
SPAWN_OBSTACLE = pygame.USEREVENT + 1
obstacle_spawn_time = 1000  # Initial spawn time in milliseconds
pygame.time.set_timer(SPAWN_OBSTACLE, obstacle_spawn_time)

score = 0
high_score = 0  # RETO 9: High score variable
start_ticks = pygame.time.get_ticks()

game_over = False
paused = False  # RETO 4: Pause flag

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # RETO 4: Pause game with ESC
            if event.key == pygame.K_ESCAPE:
                if paused:
                    paused = False
                else:
                    paused = True

            # RETO 5: Restart game with R when Game Over
            if game_over and event.key == pygame.K_r:
                score = 0
                game_over = False
                start_ticks = pygame.time.get_ticks()
                
                # Clear all obstacles completely from groups
                for obs in obstacles:
                    obs.kill()
                obstacles.empty()
                
                player1.rect.x, player1.rect.y = 300, 500
                player2.rect.x, player2.rect.y = 500, 500
                player1.speed = 5
                obstacle_spawn_time = 1000
                pygame.time.set_timer(SPAWN_OBSTACLE, obstacle_spawn_time)

            # RETO 8: Cambiar la velocidad del Jugador 1 con M (subir) y N (bajar) 
            # Permitido tanto si juega normal como si está en pausa (not game_over)
            if not game_over:
                if event.key == pygame.K_m:  # M para subir velocidad
                    if player1.speed < 12:
                        player1.speed += 1
                if event.key == pygame.K_n:  # N para bajar velocidad
                    if player1.speed > 2:
                        player1.speed -= 1

        # Spawn obstacles (Only if not paused and not game over)
        if event.type == SPAWN_OBSTACLE and not game_over and not paused:
            obs = Obstacle()
            obstacles.add(obs)
            all_sprites.add(obs)
            
            score += 1

            # RETO 7: Increasing difficulty every 10 points
            if score % 10 == 0:
                obstacle_spawn_time -= 50
                if obstacle_spawn_time < 150:
                    obstacle_spawn_time = 150
                pygame.time.set_timer(SPAWN_OBSTACLE, obstacle_spawn_time)

    # Game logic (Only updates if not paused and not game over)
    if not game_over and not paused:
        keys = pygame.key.get_pressed()
        
        # Player 1 controls (Arrow keys) -> Azul
        player1.update(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        
        # Player 2 controls (WASD keys) -> Verde
        player2.update(keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

        # Update obstacles
        obstacles.update()

        # RETO 3: Collision with Player 1 or Player 2
        for obs in obstacles:
            if player1.rect.colliderect(obs.rect) or player2.rect.colliderect(obs.rect):
                game_over = True
                # RETO 9: Update high score if current score is higher
                if score > high_score:
                    high_score = score

        # RETO 6: Survival timer calculation
        seconds_survived = (pygame.time.get_ticks() - start_ticks) // 1000

    # Drawing section
    screen.fill(WHITE)

    if not paused and not game_over:
        all_sprites.draw(screen)
    elif paused:
        # Draw everything static during pause
        all_sprites.draw(screen)
        pause_text = font.render("PAUSE (M/N para velocidad)", True, RED)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    # Render UI Text (Score, Timer, High Score, P1 Speed)
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    timer_text = font.render(f"Time: {seconds_survived}s", True, BLACK)
    p1_speed_text = font.render(f"P1 Speed (M/N): {player1.speed}", True, BLUE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    screen.blit(timer_text, (10, 70))
    screen.blit(p1_speed_text, (10, 100))

    # Game Over screen
    if game_over:
        game_over_text = font.render("GAME OVER - Press 'R' to Restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()