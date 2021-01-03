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


class Menu_Background(pygame.sprite.Sprite):  # фон меню
    image = load_image("menu_background.jpg")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Menu_Background.image
        self.rect = self.image.get_rect()
        self.rect.bottom = height


class Menu_Btn(pygame.sprite.Sprite):  # кнопки меню
    image = load_image("menu_btn.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Menu_Btn.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width / 2 - self.rect[2] / 2)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Wolf & Eggs')
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)
    running = True

    all_sprites = pygame.sprite.Group()
    menu_background = Menu_Background()
    menu_list_of_btn_names = ['Играть', 'Настройки', 'Справка']
    font = pygame.font.Font(None, 40)
    for i in range(3):
        menu_btn = Menu_Btn()
        menu_btn.rect.y = int(height * 0.4 + i * (menu_btn.rect[3] + int(height / 54)))
    while running:
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
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
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()