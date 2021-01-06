import pygame
import os
import sys
from ctypes import *


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    kx, ky = 1920 / windll.user32.GetSystemMetrics(0), 1080 / windll.user32.GetSystemMetrics(1)  # коэфы масштабирования
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (int(image.get_rect()[2] * kx), int(image.get_rect()[3] * ky)))
    return image

# Вход начало ---------------------------------------------------------------------------------------------------


class Login_panel(pygame.sprite.Sprite):  # кнопки меню
    image = load_image("login_panel.png")

    def __init__(self):
        super().__init__(login_sprites)
        self.image = Login_panel.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width / 2 - self.rect[2] / 2)
        self.rect.y = int(height / 2 - self.rect[2] / 2)

    def update(self, *args):
        global menu, log_in
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            menu = True  # Переключение на окно Меню ---------------------------------------------------------------
            log_in = False


def log_in_call():
    global running, menu, log_in
    screen.fill((255, 255, 255))
    login_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        login_sprites.update(event)
    login_sprites.update()
    pygame.display.flip()


# Вход конец ----------------------------------------------------------------------------------------------------------

# Меню начало ---------------------------------------------------------------------------------------------------


class Menu_Background(pygame.sprite.Sprite):  # фон меню
    image = load_image("menu_background.jpg")

    def __init__(self):
        super().__init__(menu_sprites)
        super().__init__(login_sprites)
        self.image = Menu_Background.image
        self.rect = self.image.get_rect()
        self.rect.bottom = height


class Menu_Btn(pygame.sprite.Sprite):  # кнопки меню
    image = load_image("menu_btn.png")

    def __init__(self):
        super().__init__(menu_sprites)
        self.image = Menu_Btn.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width / 2 - self.rect[2] / 2)


class Cup(pygame.sprite.Sprite):  # кнопки меню
    image = load_image("cup.png")

    def __init__(self):
        super().__init__(menu_sprites)
        self.image = Cup.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width * 0.7 - self.rect[2] / 2)
        self.rect.y = int(height * 0.75 - self.rect[2] / 2)


def menu_call():
    global running, menu_sprites
    menu_background = Menu_Background()
    menu_list_of_btn_names = ['Играть', 'Настройки', 'Справка']
    font = pygame.font.Font(None, 40)
    for i in range(3):
        menu_btn = Menu_Btn()
        menu_btn.rect.y = int(height * 0.4 + i * (menu_btn.rect[3] + int(height / 54)))
    cup = Cup()
    screen.fill((255, 255, 255))
    menu_sprites.draw(screen)
    for i in range(3):
        text = font.render(menu_list_of_btn_names[i], True, (255, 255, 255))
        txt_rect = text.get_rect(center=(width / 2,
                                         int(height * 0.45 + i * (menu_btn.rect[3] + int(height / 54)))))
        screen.blit(text, txt_rect)  # текст на кнопках меню
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Esc - выход из приложения
                running = False
    menu_sprites.update()
    pygame.display.flip()


# Меню конец ----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Wolf & Eggs')
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)
    running = True

    # Флаги, отвечающие за вызов функций и отрисовку окна
    log_in = True
    menu = False
    # -----------------------------------------------------------------------------------------------------------

    # Логин -------------------------------------------------------------------------------------------------------
    login_sprites = pygame.sprite.Group()
    login_panel = Login_panel()
    # Логин ------------------------------------------------------------------------------------------------------
    
    # Меню ------------------------------------------------------------------------------------------------------
    menu_sprites = pygame.sprite.Group()
    '''
    menu_background = Menu_Background()
    menu_list_of_btn_names = ['Играть', 'Настройки', 'Справка']
    font = pygame.font.Font(None, 40)
    for i in range(3):
        menu_btn = Menu_Btn()
        menu_btn.rect.y = int(height * 0.4 + i * (menu_btn.rect[3] + int(height / 54)))'''
    # Меню ----------------------------------------------------------------------------------------------------------

    while running:
        if log_in:
            log_in_call()
        if menu:
            menu_call()
    pygame.quit()