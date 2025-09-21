import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бегущий квадрат")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Игрок
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Препятствия
obstacle_width = 70
obstacle_height = 20
obstacle_speed = 5
obstacles = []
obstacle_frequency = 25  # Частота появления препятствий

# Счет
score = 0
font = pygame.font.SysFont(None, 36)

# Игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    
    # Создание новых препятствий
    if random.randint(1, obstacle_frequency) == 1:
        obstacle_x = random.randint(0, WIDTH - obstacle_width)
        obstacles.append([obstacle_x, 0])
    
    # Движение препятствий
    for obstacle in obstacles[:]:
        obstacle[1] += obstacle_speed
        if obstacle[1] > HEIGHT:
            obstacles.remove(obstacle)
            score += 1
    
    # Проверка столкновений
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            running = False
    
    # Отрисовка
    screen.fill(BLACK)
    
    # Отрисовка игрока
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    
    # Отрисовка препятствий
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))
    
    # Отрисовка счета
    score_text = font.render(f"Счет: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Обновление экрана
    pygame.display.flip()
    
    # Контроль FPS
    clock.tick(60)

# Завершение игры
pygame.quit()
sys.exit()