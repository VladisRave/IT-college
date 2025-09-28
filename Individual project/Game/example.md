# Разработка игр на PyGame: Продвинутый уровень 🚀

## Повторение пройденного 🎯

На прошлом занятии мы создали крутую игру "Уклоняйся!" где:
- Синий квадрат уворачивается от красных препятствий 🟦
- Управление стрелками ← → 
- Счет увеличивается за каждое уклонение ⭐
- Сложность растет со временем 📈

*Отличная работа, ребята! Вы уже освоили основы PyGame! 😊*

---

## Сегодня мы улучшим нашу игру! 

### 1. Добавляем систему жизней 

```python
# Добавляем в настройки
lives = 3
invincible = False
invincible_timer = 0

# В игровом цикле заменяем game_over на систему жизней
for obstacle in obstacles[:]:
    obstacle['y'] += obstacle_speed
    
    # Проверка столкновения (только если не в режиме неуязвимости)
    if not invincible and (player_x < obstacle['x'] + obstacle['width'] and
        player_x + player_size > obstacle['x'] and
        player_y < obstacle['y'] + obstacle['height'] and
        player_y + player_size > obstacle['y']):
        
        lives -= 1
        invincible = True
        invincible_timer = 90  # 1.5 секунды неуязвимости (60 FPS * 1.5)
        
        if lives <= 0:
            game_over = True

# Обработка таймера неуязвимости 
if invincible:
    invincible_timer -= 1
    if invincible_timer <= 0:
        invincible = False
```

### 2. Добавляем бонусы 

```python
# Добавляем в настройки
bonuses = []
bonus_types = ['life', 'slow', 'shield']
bonus_frequency = 200  # Реже чем препятствия

# В игровом цикле (там же где создаются препятствия)
if random.randint(1, bonus_frequency) == 1:
    bonus_type = random.choice(bonus_types)
    bonuses.append({
        'x': random.randint(0, WIDTH - 30),
        'y': -30,
        'type': bonus_type,
        'width': 30,
        'height': 30
    })

# Движение и сбор бонусов
for bonus in bonuses[:]:
    bonus['y'] += obstacle_speed - 2  # Немного медленнее препятствий
    
    # Проверка сбора бонуса
    if (player_x < bonus['x'] + bonus['width'] and
        player_x + player_size > bonus['x'] and
        player_y < bonus['y'] + bonus['height'] and
        player_y + player_size > bonus['y']):
        
        if bonus['type'] == 'life':
            lives = min(5, lives + 1)  # Максимум 5 жизней
        elif bonus['type'] == 'slow':
            obstacle_speed = max(3, obstacle_speed - 2)  # Замедляем препятствия
        elif bonus['type'] == 'shield':
            invincible = True
            invincible_timer = 180  # 3 секунды щита
            
        bonuses.remove(bonus)
    
    # Удаление вышедших за экран бонусов
    if bonus['y'] > HEIGHT:
        bonuses.remove(bonus)
```

### 3. Добавляем анимации 

```python
# Функция для мерцания при неуязвимости
def draw_player():
    if invincible:
        # Мерцание каждые 10 кадров
        if invincible_timer // 10 % 2 == 0:
            pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    else:
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

# Функции для отрисовки бонусов
def draw_bonus(bonus):
    if bonus['type'] == 'life':
        color = GREEN
        pygame.draw.rect(screen, color, (bonus['x'], bonus['y'], 30, 30))
        # Рисуем сердечко 
        pygame.draw.circle(screen, WHITE, (bonus['x'] + 10, bonus['y'] + 12), 5)
        pygame.draw.circle(screen, WHITE, (bonus['x'] + 20, bonus['y'] + 12), 5)
        pygame.draw.polygon(screen, WHITE, [
            (bonus['x'] + 5, bonus['y'] + 15),
            (bonus['x'] + 15, bonus['y'] + 25),
            (bonus['x'] + 25, bonus['y'] + 15)
        ])
    elif bonus['type'] == 'slow':
        color = (255, 255, 0)  # Желтый
        pygame.draw.rect(screen, color, (bonus['x'], bonus['y'], 30, 30))
    elif bonus['type'] == 'shield':
        color = (0, 255, 255)  # Голубой
        pygame.draw.rect(screen, color, (bonus['x'], bonus['y'], 30, 30))
```

### 4. Сохраняем рекорды в файл 

```python
def save_high_score(score):
    try:
        with open("highscore.txt", "w") as file:
            file.write(str(score))
    except:
        pass

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

# В основном коде
high_score = load_high_score()

# При game_over проверяем рекорд
if game_over and score > high_score:
    high_score = score
    save_high_score(high_score)
```

---

## Полный улучшенный код 🎮

```python
import pygame
import random
import sys

# Инициализация PyGame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уклоняйся PRO! 🚀")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Игрок
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 8

# Игровая логика
obstacles = []
bonuses = []
obstacle_speed = 5
obstacle_frequency = 30
lives = 3
score = 0
high_score = 0
game_over = False
invincible = False
invincible_timer = 0

# Шрифты
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Игровой цикл
clock = pygame.time.Clock()

def draw_hearts():
    for i in range(lives):
        pygame.draw.circle(screen, RED, (WIDTH - 30 - i*40, 30), 10)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Рестарт игры
                game_over = False
                lives = 3
                score = 0
                obstacles = []
                bonuses = []
                obstacle_speed = 5
    
    if not game_over:
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        
        # Логика игры (препятствия, бонусы, столкновения)
        # ... (вставить код из примеров выше)
    
    # Отрисовка
    screen.fill(BLACK)
    # ... (вставить отрисовку из примеров выше)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```