import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_HEIGHT = 100
GRAVITY = 1

# Set fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Dino class
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
        self.velocity_y = 0
        self.jumping = False

    def update(self):
        if self.jumping:
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y

            if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
                self.jumping = False
                self.velocity_y = 0

    def jump(self):
        if not self.jumping:
            self.velocity_y = -20
            self.jumping = True

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = random.randint(20, 60)
        height = random.randint(40, 80)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 200, 100))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 300)
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect.x -= 10
        if self.rect.right < 0:
            self.kill()

# Ground line
def draw_ground():
    pygame.draw.rect(screen, (100, 100, 100), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

# Main Game
def main():
    running = True
    score = 0

    dino = Dino()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(dino)

    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

    while running:
        screen.fill(WHITE)
        draw_ground()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    dino.jump()
            if event.type == obstacle_timer:
                obstacle = Obstacle()
                obstacles.add(obstacle)
                all_sprites.add(obstacle)

        all_sprites.update()
        all_sprites.draw(screen)

        # Collision check
        if pygame.sprite.spritecollideany(dino, obstacles):
            game_over(score)

        # Score display
        score += 1
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Game over screen
def game_over(score):
    over_text = font.render(f"Game Over! Final Score: {score}", True, (200, 0, 0))
    screen.blit(over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(3000)
    main()

if __name__ == "__main__":
    main()
