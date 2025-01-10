import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_HEIGHT = HEIGHT - 40

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dinosaur Game")

# Load assets
FONT = pygame.font.Font(None, 36)

# Classes
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.is_jumping = False
        self.jump_speed = 15
        self.gravity = 1
        self.velocity = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity = -self.jump_speed

        if self.is_jumping:
            self.rect.y += self.velocity
            self.velocity += self.gravity

            if self.rect.y >= GROUND_HEIGHT - self.rect.height:
                self.rect.y = GROUND_HEIGHT - self.rect.height
                self.is_jumping = False

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = GROUND_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.dino = Dinosaur()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.dino)
        self.score = 0
        self.lives = 3
        self.add_obstacle()

    def add_obstacle(self):
        obstacle = Obstacle()
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def main_menu(self):
        while True:
            screen.fill(WHITE)
            title = FONT.render("Chrome Dinosaur Game", True, BLACK)
            start_text = FONT.render("Press ENTER to Start", True, BLACK)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

            pygame.display.flip()

    def game_over(self):
        while True:
            screen.fill(WHITE)
            game_over_text = FONT.render("Game Over!", True, BLACK)
            restart_text = FONT.render("Press ENTER to Restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reset_game()
                    return

            pygame.display.flip()

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.dino.rect.y = GROUND_HEIGHT - self.dino.rect.height
        for obstacle in self.obstacles:
            obstacle.rect.x = WIDTH

    def run(self):
        self.main_menu()
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update()

            # Collision detection
            if pygame.sprite.spritecollideany(self.dino, self.obstacles):
                self.lives -= 1
                if self.lives == 0:
                    self.game_over()

            # Update score
            self.score += 1 / FPS

            # Draw everything
            screen.fill(WHITE)
            pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 2)
            self.all_sprites.draw(screen)

            # Display score and lives
            score_text = FONT.render(f"Score: {int(self.score)}", True, BLACK)
            lives_text = FONT.render(f"Lives: {self.lives}", True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (WIDTH - 120, 10))

            pygame.display.flip()

        pygame.quit()

# Run the game
game = Game()
game.run()
