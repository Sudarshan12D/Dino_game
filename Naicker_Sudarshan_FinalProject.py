import sys
import pygame
import random

# Initialize Pygame
pygame.init()

# Global constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FRAME_RATE = 60
GROUND_LEVEL = SCREEN_HEIGHT - 100
MAX_JUMP_HEIGHT = GROUND_LEVEL - 200

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (115, 215, 255)

# Path class for ground
class Path:
    def __init__(self, y, height, color=WHITE):
        self.rect = pygame.Rect(0, y, SCREEN_WIDTH, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Create ground
path = Path(GROUND_LEVEL, SCREEN_HEIGHT - GROUND_LEVEL, color=GREEN)

# Player class for the player object
class Player:
    def __init__(self, x, y, width=50, height=50, color=RED):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_jumping = False
        self.jump_count = 10
        self.gravity = 0.5  
        self.initial_jump_velocity = 10 


    def jump(self):
        if self.is_jumping:
            if self.jump_count >= -self.initial_jump_velocity:
                neg = 1 if self.jump_count > 0 else -1
                self.rect.y -= int((self.jump_count ** 2) * 0.5 * neg * self.gravity)
                self.jump_count -= 1 * self.gravity  # Slower decrement
            else:
                self.is_jumping = False
                self.jump_count = self.initial_jump_velocity
        else:
            if self.rect.bottom > GROUND_LEVEL:
                self.rect.bottom = GROUND_LEVEL


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
# Obstacle class
class Obstacle:
    def __init__(self, x, y, width=50, height=50, color=WHITE, speed=6):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.base_speed = speed
        self.speed = speed
        self.max_speed = 15
        

    def move_left(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update_speed(self, score):
        new_speed = self.base_speed + (score // 2000)
        self.speed = min(new_speed, self.max_speed)

# cloud class for decorations
class Cloud:
    def __init__(self, x, y, width=100, height=50, color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 2  

    def move(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Run...")
clock = pygame.time.Clock()

# Game variables
player = Player(50, SCREEN_HEIGHT - 150)
obstacles = []
clouds = []
score = 0
font = pygame.font.SysFont(None, 55)

def spawn_obstacle():
    max_obstacles = 2  # Max number of obstacles at the same time
    if len(obstacles) < max_obstacles and random.randint(1, 60) == 1:
        obstacle_width = 30  # Fixed width for all obstacles
        obstacle_height = random.randint(50, 150)  # Varying heights for the obstacles
        obstacles.append(Obstacle(SCREEN_WIDTH, GROUND_LEVEL - obstacle_height, obstacle_width, obstacle_height, WHITE))

def spawn_cloud():
    if random.randint(1, 100) == 1:  
        cloud_y = random.randint(50, SCREEN_HEIGHT // 4)
        clouds.append(Cloud(SCREEN_WIDTH, cloud_y))
        
def show_score():
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

def game_over():
    game_over_font = pygame.font.SysFont('arial', 64)
    restart_font = pygame.font.SysFont('arial', 32)
    game_over_surface = game_over_font.render('Game Over', True, RED)
    restart_surface = restart_font.render('Click to Restart', True, WHITE)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    return  
        
        screen.fill(BLUE)
        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_surface.get_height() // 2))
        
        restart_button_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(restart_surface, restart_button_rect.topleft)
        
        pygame.display.flip()
        clock.tick(FRAME_RATE)

        
# Main game loop
running = True
obstacle_spawn_time = 120  # Delay for starting
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not player.is_jumping:
        if keys[pygame.K_SPACE] and player.rect.bottom == GROUND_LEVEL:
            player.is_jumping = True

    player.jump()

     
    # Spawn obstacles after a delay
    if obstacle_spawn_time > 0:
        obstacle_spawn_time -= 1
    else:
        spawn_obstacle()

    # Spawn clouds
    spawn_cloud()
    
    # Colour the screen
    screen.fill(BLUE)
    
    # Move and draw clouds
    for cloud in clouds:
        cloud.move()
        cloud.draw(screen)
    
    # Draw the path 
    path.draw(screen)

    # Move and draw obstacles
    for obstacle in obstacles:
        obstacle.update_speed(score)
        obstacle.move_left()
        obstacle.draw(screen)
        if player.rect.colliderect(obstacle.rect):
            running = False  # Stop the main game loop
            game_over()  # Display game over
            
            # Resetting all variables
            player = Player(50, SCREEN_HEIGHT - 150)
            obstacles = []
            clouds = []
            score = 0
            running = True
            

    # Draw the player
    player.draw(screen)

    #player stays on the ground
    if player.rect.bottom > GROUND_LEVEL:
        player.rect.bottom = GROUND_LEVEL
        
    # Update score
    score += 1
    show_score()

    pygame.display.flip()
    clock.tick(FRAME_RATE)

    # Remove obstacles and clouds that have moved off the screen
    obstacles = [obstacle for obstacle in obstacles if obstacle.rect.x > -50]
    clouds = [cloud for cloud in clouds if cloud.rect.x > -cloud.rect.width]


# If the game loop ends (running is False), close the game
pygame.quit()
sys.exit()
