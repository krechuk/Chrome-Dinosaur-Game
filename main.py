import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dinosaur Game")

# Fonts
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Dinosaur class
class Dinosaur:
    def __init__(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 100
        self.is_jumping = False
        self.jump_speed = 15
        self.gravity = 1
        self.y_velocity = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = -self.jump_speed

        if self.is_jumping:
            self.rect.y += self.y_velocity
            self.y_velocity += self.gravity
            if self.rect.y >= SCREEN_HEIGHT - 100:
                self.rect.y = SCREEN_HEIGHT - 100
                self.is_jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Obstacle class
class Obstacle:
    def __init__(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 80
        self.speed = 7

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -30:
            self.rect.x = SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Game class
class Game:
    def __init__(self):
        self.dino = Dinosaur()
        self.obstacle = Obstacle()
        self.running = True
        self.lives = 3
        self.timer = 0
        self.game_over = False

    def reset(self):
        self.dino = Dinosaur()
        self.obstacle = Obstacle()
        self.lives = 3
        self.timer = 0
        self.game_over = False

    def handle_collision(self):
        if self.dino.rect.colliderect(self.obstacle.rect):
            self.lives -= 1
            self.obstacle.rect.x = SCREEN_WIDTH
            if self.lives <= 0:
                self.game_over = True

    def update(self):
        if not self.game_over:
            self.dino.update()
            self.obstacle.update()
            self.handle_collision()
            self.timer += 1 / FPS

    def draw(self):
        screen.fill(WHITE)
        self.dino.draw(screen)
        self.obstacle.draw(screen)
        timer_text = font.render(f"Time: {int(self.timer)}", True, BLACK)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        screen.blit(timer_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        if self.game_over:
            game_over_text = font.render("Game Over! Press R to restart.", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset()

            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

# Main menu function
def main_menu():
    while True:
        screen.fill(WHITE)
        title_text = font.render("Chrome Dinosaur Game", True, BLACK)
        start_text = font.render("Press SPACE to Start", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# Run the game
if __name__ == "__main__":
    while True:
        main_menu()
        game = Game()
        game.run()
