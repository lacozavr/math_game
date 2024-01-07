import pygame
import random
import time
import sqlite3


class Timer:
    def __init__(self, dif):
        self.dif = dif
        if self.dif == "Очень легко":
            self.sec = 5
        elif self.dif == "Легко":
            self.sec = 10
        elif self.dif == "Нормально":
            self.sec = 20
        elif self.dif == "Сложно":
            self.sec = 25
        self.start = time.time()
        self.end = False
        self.b = 4.9 / self.sec
        self.a = 0

    def chek(self):
        if int(self.start) + self.sec < int(time.time()):
            self.end = True
        return self.end

    def get_part(self):
        self.a += self.b
        return 300 - self.a


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font_small.render(text, True, self.color)
        self.active = False
        self.maximka = False
        self.only_digit = False

    # добавление текста
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif not self.maxim():
                    if self.only_digit:
                        if event.unicode == '-':
                            self.text += event.unicode
                        elif event.unicode.isdigit():
                            self.text += event.unicode
                    else:
                        self.text += event.unicode
                self.txt_surface = font_small.render(self.text, True, BLACK)

    # увеличение и ограничение бокса
    def maxim(self):
        maximka = self.txt_surface.get_width() >= 300
        if not maximka:
            width = max(200, self.txt_surface.get_width() + 30)
            self.rect.w = width
        return maximka

    # отображение бокса
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    # возвращение текста бокса
    def get_text(self, text=''):
        return self.text

    # печать текста в боксе
    def set_text(self, text):
        self.text = text

    # включение и выкл режима только цифры... и минус
    def digit(self):
        if self.only_digit:
            self.only_digit = False
        else:
            self.only_digit = True


# Инициализация Pygame
pygame.init()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
FON = pygame.color.Color('#88C0D3')
BUTTON = pygame.color.Color('#CFD4DF')
COLOR_INACTIVE = pygame.Color(0, 0, 0)
COLOR_ACTIVE = pygame.Color(255, 255, 255)

#Подключение к базе данных
con = sqlite3.connect('math_game.db')
cur = con.cursor()

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
User = [False, '', 0] #Зарегестрирован ли пользователь, имя, рекорд

# Функция отображения текста на экране
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Функция отображения главного меню
def draw_main_menu():
    screen.fill(FON)
    pygame.draw.rect(screen, BUTTON, (100, 170, 600, 60))
    draw_text("Математические примеры", font_large, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    pygame.draw.rect(screen, BUTTON, (200, 280, 430, 40))
    draw_text(f"Максимальный счёт: {User[2]}", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, BUTTON, (330, 380, 140, 40))
    draw_text("Играть", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)
    if not User[0]:
        pygame.draw.rect(screen, BLACK, (700, 20, 80, 40), 1)
        draw_text("Вход", font_small, BLACK, 740, 40)
    else:
        draw_text(User[1], font_small, BLACK, 740, 40)

# Функция отображения меню выбора сложности
def draw_difficulty_menu():
    screen.fill(FON)
    pygame.draw.rect(screen, BUTTON, (150, 120, 500, 60))
    draw_text("Выберите сложность", font_large, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    pygame.draw.rect(screen, BUTTON, (290, 217, 220, 40))
    draw_text("Очень легко", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 5)
    pygame.draw.rect(screen, BUTTON, (290, 290, 220, 40))
    draw_text("Легко", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2.6 // 5)
    pygame.draw.rect(screen, BUTTON, (290, 365, 220, 40))
    draw_text("Нормально", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3.2 // 5)
    pygame.draw.rect(screen, BUTTON, (290, 435, 220, 40))
    draw_text("Сложно", font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3.8 // 5)

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
        a, b = random.randint(10, 70), random.randint(1, 20)
        operator = random.choice(["+", "-", "*", "/"])
        equation = f"{a} {operator} {b} = ?"
    elif difficulty == "Сложно":
        a, b = random.randint(1, 100), random.randint(1, 100)
        operator = random.choice(["*", "/"])
        equation = f"{a} {operator} {b} = ?"
    return equation


def draw_sign_in_menu():
    screen.fill(FON)
    inputik.draw(screen)
    pygame.draw.rect(screen, BUTTON, (140, 180, 480, 40))
    draw_text("Введите имя пользователя:", font_medium, BLACK, 380, 200)
    pygame.draw.rect(screen, BUTTON, (220, 380, 360, 40))
    draw_text("Войти/Зарегистрироваться", font_small, BLACK, 400, 400)
    pygame.draw.rect(screen, FON, (737, 32, 30, 35), 1)
    draw_text("Х", font_large, BLACK, 750, 50)


def draw_play_zone(equation, tm):
    screen.fill(FON)
    inputik.draw(screen)
    draw_text(equation, font_medium, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5)
    draw_text(f"Счёт: {score}", font_medium, BLACK, 70, 50)
    pygame.draw.rect(screen, BUTTON, (250, 130, 310, 40))
    pygame.draw.rect(screen, (150, 150, 255), (255, 135, tm.get_part(), 30))


def game_loop():
    global game_state, difficulty, score, inputik, equation
    clock, running, c = pygame.time.Clock(), True, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "MAIN_MENU":
                    if event.button == 1: # Левая кнопка мыши
                        pos = pygame.mouse.get_pos()
                        if (pos[0] >= 330 and pos[0] <= 330 + 140) and (pos[1] >= 380 and pos[1] <= 380 + 40):
                            game_state = "DIFFICULTY_MENU"
                        if (pos[0] >= 700 and pos[0] <= 700 + 80) and (pos[1] >= 20 and pos[1] <= 20 + 40):
                            game_state = "SIGN_IN"
                            inputik = InputBox(150, 230, 200, 40)
                elif game_state == "DIFFICULTY_MENU":
                    if event.button == 1: # Левая кнопка мыши
                        pos = pygame.mouse.get_pos()
                        # Подобие кнопок
                        if (pos[0] >= 290 and pos[0] <= 290 + 220) and (pos[1] >= 217 and pos[1] <= 217 + 40):
                            difficulty = "Очень легко"
                            game_state = "PLAYING"
                            inputik = InputBox(290, 280, 200, 40)
                            inputik.digit()
                            equation = generate_equation(difficulty)
                            tm = Timer(difficulty)
                        elif (pos[0] >= 290 and pos[0] <= 290 + 220) and (pos[1] >= 290 and pos[1] <= 290 + 40):
                            difficulty = "Легко"
                            game_state = "PLAYING"
                            inputik = InputBox(290, 280, 200, 40)
                            inputik.digit()
                            equation = generate_equation(difficulty)
                            tm = Timer(difficulty)
                        elif (pos[0] >= 290 and pos[0] <= 290 + 220) and (pos[1] >= 365 and pos[1] <= 365 + 40):
                            difficulty = "Нормально"
                            game_state = "PLAYING"
                            inputik = InputBox(290, 280, 200, 40)
                            inputik.digit()
                            equation = generate_equation(difficulty)
                            tm = Timer(difficulty)
                        elif (pos[0] >= 290 and pos[0] <= 290 + 220) and (pos[1] >= 435 and pos[1] <= 435 + 40):
                            difficulty = "Сложно"
                            game_state = "PLAYING"
                            inputik = InputBox(290, 280, 200, 40)
                            inputik.digit()
                            equation = generate_equation(difficulty)
                            tm = Timer(difficulty)
                elif game_state == "SIGN_IN":
                    if event.button == 1:  # Левая кнопка мыши
                        pos = pygame.mouse.get_pos()
                        inputik.handle_event(event)
                        if (pos[0] >= 737 and pos[0] <= 737 + 30) and (pos[1] >= 32 and pos[1] <= 32 + 35):
                            game_state = "MAIN_MENU"
                        elif (pos[0] >= 220 and pos[0] <= 220 + 360) and (pos[1] >= 380 and pos[1] <= 380 + 40):
                            if bool(inputik.get_text()):
                                score_us = cur.execute("""SELECT score FROM users
                                                                    WHERE name = ?""", (inputik.get_text(),)).fetchall()
                                if bool(score_us):
                                    User[1] = inputik.get_text()
                                    User[2] = int(score_us[0][0])
                                else:
                                    sql = 'INSERT INTO users VALUES(?, ?)'
                                    data = [(inputik.get_text(), '0',)]
                                    with con:
                                        con.executemany(sql, data)
                                    User[1] = inputik.get_text()
                                game_state = "MAIN_MENU"
                                User[0] = True
                elif game_state == "PLAYING":
                    inputik.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                if game_state == "PLAYING":
                    if event.key == pygame.K_RETURN:
                        if bool(inputik.get_text()):
                            if int(inputik.get_text()) == eval(equation[:-4]):
                                if difficulty == 'Очень легко':
                                    score += 1
                                elif difficulty == 'Легко':
                                    score += 2
                                elif difficulty == 'Нормально':
                                    score += 3
                                else:
                                    score += 4
                                equation = generate_equation(difficulty)
                                inputik.set_text('')
                                tm = Timer(difficulty)
                            else:
                                game_state = "MAIN_MENU"
                                if score > User[2]:
                                    User[2] = score
                                    if User[0]:
                                        sql = 'UPDATE users SET score = ? WHERE name = ?'
                                        data = [(score, User[1])]
                                        with con:
                                            con.executemany(sql, data)
                                score = 0
                    inputik.handle_event(event)
                    if inputik.get_text().isdigit():
                        inputik.get_text(inputik.get_text()[:-1])
                elif game_state == "SIGN_IN":
                    if event.key == pygame.K_RETURN:
                        if bool(inputik.get_text()):
                            score_us = cur.execute("""SELECT score FROM users
                                                                WHERE name = ?""", (inputik.get_text(),)).fetchall()
                            if bool(score_us):
                                User[1] = inputik.get_text()
                                User[2] = int(score_us[0][0])
                            else:
                                sql = 'INSERT INTO users VALUES(?, ?)'
                                data = [(inputik.get_text(), '0',)]
                                with con:
                                    con.executemany(sql, data)
                                User[1] = inputik.get_text()
                            game_state = "MAIN_MENU"
                            User[0] = True
                    else:
                        inputik.handle_event(event)
        if game_state == "MAIN_MENU":
            draw_main_menu()
        elif game_state == "DIFFICULTY_MENU":
            draw_difficulty_menu()
        elif game_state == "SIGN_IN":
            draw_sign_in_menu()
        elif game_state == "PLAYING":
            if tm.chek():
                game_state = "MAIN_MENU"
                if score > User[2]:
                    User[2] = score
                    if User[0]:
                        sql = 'UPDATE users SET score = ? WHERE name = ?'
                        data = [(score, User[1])]
                        with con:
                            con.executemany(sql, data)
                score = 0
            draw_play_zone(equation, tm)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

# Запуск игры
game_loop()
