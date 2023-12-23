import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Определение размеров окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Математические примеры")

# Шрифты
font_small = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 48)
font_large = pygame.font.Font(None, 64)

# Переменные игры
game_state = "MAIN_MENU"
difficulty = ""
score = 0

# Функция отображения текста на экране
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Функция отображения главного меню
def draw_main_menu():
    screen.fill(BLACK)
    draw_text("Математические примеры", font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(f"Максимальный счёт: {score}", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Играть", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)

# Функция отображения меню выбора сложности
def draw_difficulty_menu():
    screen.fill(BLACK)
    draw_text("Выберите сложность", font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text("Очень легко", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 5)
    draw_text("Легко", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 5)
    draw_text("Нормально", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 4 // 5)

# Функция генерации случайного примера
def generate_equation(difficulty):
    if difficulty == "Очень легко":
        a, b = random.randint(1, 10), random.randint(1, 10)
        operator = random.choice(["+", "-"])
        equation = f"{a} {operator} {b} = ?"
    elif difficulty == "Легко":
        a, b = random.randint(1, 20), random.randint(1, 20)
        operator = random.choice(["+", "-", "*"])
        equation = f"{a} {operator} {b} = ?"
    elif difficulty == "Нормально":
        a, b = random.randint(1, 50), random.randint(1, 50)
        operator = random.choice(["+", "-", "*", "/"])
        equation = f"{a} {operator} {b} = ?"
    elif difficulty == "Сложно":
        a, b = random.randint(1, 100), random.randint(1, 100)
        operator = random.choice(["+", "-", "*", "/"])
        equation = f"{a} {operator} {b} = ?"
    return equation


def game_loop():
    global game_state, difficulty, score
    clock, running, c = pygame.time.Clock(), True, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "MAIN_MENU":
                    if event.button == 1:  # Левая кнопка мыши
                        game_state = "DIFFICULTY_MENU"
                elif game_state == "DIFFICULTY_MENU":
                    if event.button == 1:  # Левая кнопка мыши
                        pos = pygame.mouse.get_pos()
                        # Подобие кнопок
                        if pos[1] >= SCREEN_HEIGHT * 2 // 5 and pos[1] < SCREEN_HEIGHT * 3 // 5:
                            difficulty = "Очень легко"
                        elif pos[1] >= SCREEN_HEIGHT * 3 // 5 and pos[1] < SCREEN_HEIGHT * 4 // 5:
                            difficulty = "Легко"
                        elif pos[1] >= SCREEN_HEIGHT * 4 // 5:
                            difficulty = "Нормально"
                        game_state = "PLAYING"
                        score = 0 # Позже планируется вносить макс счёт в txt документ под ником игрока

        screen.fill(BLACK)

        if game_state == "MAIN_MENU":
            draw_main_menu()
        elif game_state == "DIFFICULTY_MENU":
            draw_difficulty_menu()
        elif game_state == "PLAYING":
            if c == 0:
                start_ticks = pygame.time.get_ticks()
                equation = generate_equation(difficulty)
                draw_text(equation, font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                c += 1
            else:
                start_ticks = pygame.time.get_ticks()
                equation = generate_equation(difficulty)
                draw_text(equation, font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                time.sleep(10) # Временный таймер для теста на 1 секунду, позже сделаем вывод времени для овтета на экран

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Запуск игры
game_loop()