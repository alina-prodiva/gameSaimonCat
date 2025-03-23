import random
import pygame
from pygame import mixer
import os, sys


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
SIZE = WIDTH, HEIGHT = 800, 600
FPS = 60
score = 0
num_bees = 6
num_flies = 2


def load_image(name, colorkey=None):
    # функция загрузки изображения
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Camera:
    # Модель камеры для фокуса на игроке
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Bee(pygame.sprite.Sprite):
    # Модель пчелки, добавляем в обе группы спрайтов
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_bees)  # по данной группе будем отслеживать столкновения кота по маске
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(load_image('leftbee.png'), (45, 45))
        self.rect = pygame.Rect(x, y, 45, 45)
        self.vector = 'left'  # задаем начальное направление

    def update(self):
        global score
        k = score // 30 + 1  # ускорение движения пчелок через каждые 30 очков
        # изменение положения пчелы в зависимости от направления движения
        if self.vector == 'left' and self.x - 2 > 10:
            self.x -= 3 * k
        elif self.vector == 'left' and self.x - 2 <= 10:
            self.image = pygame.transform.scale(load_image('rightbee.png'), (45, 45))
            self.vector = 'right'
            self.x += 3 * k
        elif self.vector == 'right' and self.x + 2 < WIDTH - 50:
            self.x += 3 * k
        elif self.vector == 'right' and self.x + 2 >= WIDTH - 50:
            self.image = pygame.transform.scale(load_image('leftbee.png'), (45, 45))
            self.vector = 'left'
            self.x -= 3 * k
        self.y += random.randint(-5, 5)  # чтобы было больше похоже на полет пчелы добавим дрожание по вертикали
        while not 40 < self.y < 350:
            self.y += random.randint(-5, 5)
        self.rect = pygame.Rect(self.x, self.y, 45, 45)

class Fly(pygame.sprite.Sprite):
    # Модель мухи, добавляем в обе группы спрайтов
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_flies)  # по данной группе будем отслеживать столкновения кота по маске
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(load_image('leftfly.png'), (45, 45))
        self.rect = pygame.Rect(x, y, 45, 45)
        self.vector = 'left'  # задаем начальное направление

    def update(self):
        global score
        k = score // 30 + 1  # ускорение движения пчелок через каждые 30 очков
        # изменение положения пчелы в зависимости от направления движения
        if self.vector == 'left' and self.x - 2 > 10:
            self.x -= 2 * k
        elif self.vector == 'left' and self.x - 2 <= 10:
            self.image = pygame.transform.scale(load_image('rightfly.png'), (45, 45))
            self.vector = 'right'
            self.x += 2 * k
        elif self.vector == 'right' and self.x + 2 < WIDTH - 50:
            self.x += 2 * k
        elif self.vector == 'right' and self.x + 2 >= WIDTH - 50:
            self.image = pygame.transform.scale(load_image('leftfly.png'), (45, 45))
            self.vector = 'left'
            self.x -= 2 * k
        self.y += random.randint(-5, 5)  # чтобы было больше похоже на полет мухи добавим дрожание по вертикали
        while not 40 < self.y < 350:
            self.y += random.randint(-5, 5)
        self.rect = pygame.Rect(self.x, self.y, 45, 45)


class Cat(pygame.sprite.Sprite):
    # Модель кота - главного игрока
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.vector = 'left'
        self.image = pygame.transform.scale(load_image('leftcat.png'), (150, 100))
        self.rect = pygame.Rect(x, y, 150, 100)

    def arrow_move(self, vector):
        # перемещения кота в зависимости от нажатой стрелки
        if vector == 'left' and self.y == 480:
            self.vector = 'left'
            self.image = pygame.transform.scale(load_image('leftcat.png'), (150, 100))
            if self.x - 10 > 10:
                self.x -= 10
            self.rect = pygame.Rect(self.x, self.y, 150, 100)
        elif vector == 'right' and self.y == 480:
            self.vector = 'right'
            self.image = pygame.transform.scale(load_image('rightcat.png'), (150, 100))
            if self.x + 10 < WIDTH - 150:
                self.x += 10
            self.rect = pygame.Rect(self.x, self.y, 150, 100)
        elif vector == 'left' and self.vector == 'right' and self.y < 480:
            self.vector = 'left'
            self.image = pygame.transform.scale(load_image('leftcatup.png'), (100, 200))
            if self.x - 10 > 10:
                self.x -= 10
            self.rect = pygame.Rect(self.x, self.y, 100, 200)
        elif vector == 'right' and self.vector == 'left' and self.y < 480:
            self.vector = 'right'
            self.image = pygame.transform.scale(load_image('rightcatup.png'), (100, 200))
            if self.x + 10 < WIDTH - 150:
                self.x += 10
            self.rect = pygame.Rect(self.x, self.y, 100, 200)
        elif vector == 'up' and self.vector == 'left':
            self.image = pygame.transform.scale(load_image('leftcatup.png'), (100, 200))
            if self.y - 100 > 0:
                self.y -= 100
            if self.x - 10 > 10:
                self.x -= 10
            self.rect = pygame.Rect(self.x, self.y, 100, 200)
        elif vector == 'up' and self.vector == 'right':
            self.image = pygame.transform.scale(load_image('rightcatup.png'), (100, 200))
            if self.y - 100 > 0:
                self.y -= 100
            if self.x + 10 < WIDTH - 150:
                self.x += 10
            self.rect = pygame.Rect(self.x, self.y, 100, 200)
        elif vector == 'up' and self.vector == '':
            self.vector = 'right'
            self.image = pygame.transform.scale(load_image('rightcatup.png'), (100, 200))
            if self.x + 10 < WIDTH - 150:
                self.x += 10
            self.rect = pygame.Rect(self.x, self.y, 100, 200)
        elif vector == 'down':
            self.vector = ''
            self.y = 480
            self.image = pygame.transform.scale(load_image('sleepcat.png'), (220, 100))
            self.rect = pygame.Rect(self.x, self.y, 220, 100)

    def update(self):
        global score
        # после каждого прыжка кота возвращаем на место
        if self.y <= 400:
            self.y += 20
            self.rect = pygame.Rect(self.x, self.y, 100, 200)
        else:
            self.y = 480
            if self.vector == 'left':
                self.image = pygame.transform.scale(load_image('leftcat.png'), (150, 100))
            elif self.vector == 'right':
                self.image = pygame.transform.scale(load_image('rightcat.png'), (150, 100))
            self.rect = pygame.Rect(self.x, self.y, 100, 200)
        for bee in all_bees:  # проходим по группе пчел для мониторинга столкновений
            if pygame.sprite.collide_mask(self, bee):
                bee.remove(all_bees)
                bee.kill()
                score += 1  # за каждую "убитую" пчелу + 1 очко
        for fly in all_flies:  # проходим по группе мух для мониторинга столкновений
            if pygame.sprite.collide_mask(self, fly):
                fly.remove(all_flies)
                fly.kill()
                if score - 5 > 0:
                    score -= 5  # за каждую "убитую" муху - 5 очко
                else:
                    score = 0


def game_over():  # завершающий экран, показывает очки за игру
    intro_text = ["Конец игры", "Заработано очков: " + str(score)]
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('final.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)

def start_screen():  # начальная заставка
    intro_text = ["Начать игру", "Только не лови мух!"]
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('start.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 450
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра "Кот Саймона"')
    screen = pygame.display.set_mode(SIZE)
    icon = pygame.image.load('data/catfoot.ico')  # загрузка иконки для окна
    pygame.display.set_icon(icon)
    mixer.music.load("data/sunshine.wav")  # загрузка музыки
    mixer.music.play(-1)
    start_screen()  # запуск начальной заставки
    background = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))  # установили задний фон
    font = pygame.font.Font('freesansbold.ttf', 32)
    camera = Camera()  # запустили камеру
    running = True
    all_sprites = pygame.sprite.Group()
    all_bees = pygame.sprite.Group()
    all_flies = pygame.sprite.Group()
    clock = pygame.time.Clock()
    cat = Cat(400, 480)  # создали игрока кота
    for _ in range(num_bees):  # создали пчелок
        Bee(random.randint(50, WIDTH - 50), random.randint(50, 300))
    for _ in range(num_flies):  # создали мух
        Fly(random.randint(50, WIDTH - 50), random.randint(50, 300))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
                running = False
        keys = pygame.key.get_pressed()
        # отслеживаем нажатия клавиш, управление игроком стрелками
        if keys[pygame.K_LEFT]:
            cat.arrow_move('left')
        if keys[pygame.K_RIGHT]:
            cat.arrow_move('right')
        if keys[pygame.K_UP]:
            cat.arrow_move('up')
        if keys[pygame.K_DOWN]:
            cat.arrow_move('down')
        clock.tick(FPS)
        if len(all_bees) < num_bees:  # пополняем количество пчелок, если какие-то убиты
            Bee(random.randint(50, WIDTH - 50), random.randint(50, 300))
        if len(all_flies) < num_flies:  # пополняем количество мух, если какие-то убиты
            Fly(random.randint(50, WIDTH - 50), random.randint(50, 300))
        all_sprites.update()
        all_bees.update()
        all_flies.update()
        camera.update(cat)
        screen.fill(BLACK)  # обновляем после каждого кадра фон, чтобы не было следов движения
        background = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))
        score_text = font.render("Score : " + str(score), 1, WHITE)  # ведем запись очков
        intro_rect = score_text.get_rect()
        intro_rect.top = 10
        intro_rect.x = 10
        screen.blit(score_text, intro_rect)
        all_sprites.draw(screen)  # после каждого обновления кадра восстанавливаем всех спрайтов
        pygame.display.flip()