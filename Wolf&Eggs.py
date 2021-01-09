import pygame
import os
import sys
import tkinter as tk
from backend import registration, check_login_password

root = tk.Tk()

#  Переменные - ошибочные действия пользователей
error_menu_limit = False
error_wrong_data = False
error_sign = False
error_reg = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    kx, ky = 1920 / root.winfo_screenwidth(), 1080 / root.winfo_screenheight()  # коэфы масштабирования
    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (int(image.get_rect()[2] / kx), int(image.get_rect()[3] / ky)))
    return image


# Вход начало ---------------------------------------------------------------------------------------------------


class Login_panel(pygame.sprite.Sprite):
    image = load_image("login_panel.png")

    def __init__(self):
        super().__init__(login_sprites)
        self.image = Login_panel.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width / 2 - self.rect[2] / 2)
        self.rect.y = int(height / 2 - self.rect[3] / 2)


class Input_login(pygame.sprite.Sprite):
    image = load_image("input_login.png")

    def __init__(self):
        super().__init__(login_sprites)
        self.image = Input_login.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width / 2 - self.rect[2] / 2) * 1.03
        self.rect.y = int(height / 2 - self.rect[3] / 2) * 0.78
        self.font = pygame.font.Font(None, 50)
        self.string = ''

    def update(self, *args):
        global menu, log_in, read_log, error_menu_limit, read_pass, error_wrong_data, error_reg, error_sign
        text = self.font.render(self.string, True, (0, 0, 0))
        txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 0.78))
        screen.blit(text, txt_rect)
        if error_menu_limit:
            font = pygame.font.Font(None, 60)
            text = font.render('Превышено кол-во символов', True, (100, 0, 0))
            txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 0.2))
            screen.blit(text, txt_rect)
        if read_log and args:
            if args[0].type == pygame.KEYDOWN:
                error_reg, error_sign, error_wrong_data = False, False, False
                if args[0].key == pygame.K_BACKSPACE:
                    if len(self.string) > 0:
                        self.string = self.string[:len(self.string) - 1]
                        error_menu_limit = False
                else:
                    if len(self.string) <= 20:
                        self.string += args[0].unicode
                        error_menu_limit = False
                    else:
                        error_menu_limit = True
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            read_log = True
            read_pass = False


class Input_password(pygame.sprite.Sprite):
    image = load_image("input_login.png")

    def __init__(self):
        super().__init__(login_sprites)
        self.image = Input_password.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width / 2 - self.rect[2] / 2) * 1.03
        self.rect.y = int(height / 2 - self.rect[3] / 2) * 1.05
        self.font = pygame.font.Font(None, 50)
        self.string = ''

    def update(self, *args):
        global menu, log_in, read_log, read_pass, error_menu_limit, error_wrong_data, error_reg, error_sign
        text = self.font.render(self.string, True, (0, 0, 0))
        txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 1.05))
        screen.blit(text, txt_rect)
        if read_pass and args:
            if args[0].type == pygame.KEYDOWN:
                error_reg, error_sign, error_wrong_data = False, False, False
                if args[0].key == pygame.K_BACKSPACE:
                    if len(self.string) > 0:
                        error_menu_limit = False
                        self.string = self.string[:len(self.string) - 1]
                else:
                    if len(self.string) <= 20:
                        error_menu_limit = False
                        self.string += args[0].unicode
                    else:
                        error_menu_limit = True
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            read_log = False
            read_pass = True


class Sign_in(pygame.sprite.Sprite):
    image = load_image("btn_sign_in.png")

    def __init__(self):
        super().__init__(login_sprites)
        self.image = Sign_in.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width / 2 - self.rect[2] / 2) * 0.82
        self.rect.y = int(height / 2 - self.rect[3] / 2) * 1.34

    def update(self, *args):
        global menu, log_in, input_pass, input_login, error_wrong_data, error_sign, error_reg, error_menu_limit
        if error_sign:
            font = pygame.font.Font(None, 60)
            text = font.render(check_login_password(input_login.string, input_pass.string), True, (100, 0, 0))
            txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 0.2))
            screen.blit(text, txt_rect)
        if self.rect.collidepoint((pygame.mouse.get_pos()[0] + 22, pygame.mouse.get_pos()[1] + 5)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(
                    (args[0].pos[0] + 22, args[0].pos[1] + 5)):  # Подбор ------------------------------------------
            error_reg, error_sign, error_menu_limit, error_wrong_data = False, False, False, False
            if input_login.string and input_pass.string and check_login_password(input_login.string, input_pass.string):
                if isinstance(check_login_password(input_login.string, input_pass.string), tuple):
                    menu = True  # Переключение на окно Меню ---------------------------------------------------------------
                    log_in = False
                    error_wrong_data = False
                    error_sign = False
                else:
                    error_sign = True
                    error_wrong_data = False
            else:
                error_wrong_data = True
                error_sign = False


class Register(pygame.sprite.Sprite):
    image = load_image("btn_register.png")

    def __init__(self):
        super().__init__(login_sprites)
        self.image = Register.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width / 2 - self.rect[2] / 2) * 1.23
        self.rect.y = int(height / 2 - self.rect[3] / 2) * 1.34

    def update(self, *args):
        global menu, log_in, error_wrong_data, input_pass, input_login, error_reg, error_sign
        if error_wrong_data:
            font = pygame.font.Font(None, 60)
            text = font.render('Неверные данные', True, (100, 0, 0))
            txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 0.2))
            screen.blit(text, txt_rect)
        if error_reg:
            font = pygame.font.Font(None, 60)
            text = font.render(registration(input_login.string, input_pass.string), True, (100, 0, 0))
            txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 0.2))
            screen.blit(text, txt_rect)
        if self.rect.collidepoint((pygame.mouse.get_pos()[0] + 22, pygame.mouse.get_pos()[1] + 5)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(
                    (args[0].pos[0] + 22, args[0].pos[1] + 5)):  # Подбор ------------------------------------------
            error_reg, error_sign, error_menu_limit, error_wrong_data = False, False, False, False
            if input_login.string and input_pass.string:
                if not registration(input_login.string, input_pass.string):
                    error_wrong_data = False
                    error_reg = False
                    error_sign = False
                    menu = True  # Переключение на окно Меню ---------------------------------------------------------------
                    log_in = False
                else:
                    error_reg = True
                    error_wrong_data = False
                    error_sign = False
            else:
                error_wrong_data = True
                error_reg = False


def log_in_call():
    global running, menu, log_in
    screen.fill((255, 255, 255))
    login_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Esc - выход из приложения
                running = False
        login_sprites.update(event)
    login_sprites.update()
    pygame.display.flip()
    if menu:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


# Вход конец ----------------------------------------------------------------------------------------------------------

# Меню начало ---------------------------------------------------------------------------------------------------


class Menu_Background(pygame.sprite.Sprite):  # фон меню
    image = load_image("menu_background.jpg")

    def __init__(self):
        global info_sprites, game_sprites
        super().__init__(menu_sprites)
        super().__init__(game_sprites)
        super().__init__(info_sprites)
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


class Btn_Start(Menu_Btn):
    def update(self, *args):
        global menu, game
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0] + 22, args[0].pos[1] + 5)):
            game = True
            menu = False


class Btn_Settings(Menu_Btn):
    def update(self, *args):
        global menu
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


class Btn_Info(Menu_Btn):
    def update(self, *args):
        global menu, info
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0] + 22, args[0].pos[1] + 5)):
            info = True
            menu = False


class Exit_Btn(pygame.sprite.Sprite):  # кнопки меню
    image = load_image("btn_exit.png")

    def __init__(self):
        super().__init__(menu_sprites)
        self.image = Exit_Btn.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width * 0.1)
        self.rect.y = int(height * 0.1)

    def update(self, *args):
        global running
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0] + 22, args[0].pos[1] + 5)):
            running = False


class Cup(pygame.sprite.Sprite):
    image = load_image("cup.png")

    def __init__(self):
        super().__init__(menu_sprites)
        self.image = Cup.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width * 0.7 - self.rect[2] / 2)
        self.rect.y = int(height * 0.75 - self.rect[3] / 2)

    def update(self, *args):
        global menu
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


def menu_call():
    global running, menu_sprites, info, game
    menu_background = Menu_Background()
    menu_list_of_btn_names = ['Играть', 'Настройки', 'Справка']
    font = pygame.font.Font(None, 50)
    btn_start, btn_settings, btn_info = Btn_Start(), Btn_Settings(), Btn_Info()
    for n, i in enumerate([btn_start, btn_settings, btn_info]):
        i.rect.y = int(height * 0.4 + n * (i.rect[3] + int(height / 54)))
    cup = Cup()
    exit_btn = Exit_Btn()
    screen.fill((255, 255, 255))
    menu_sprites.draw(screen)
    for i in range(3):
        text = font.render(menu_list_of_btn_names[i], True, (255, 255, 255))
        txt_rect = text.get_rect(center=(width / 2,
                                         int(height * 0.45 + i * (btn_start.rect[3] + int(height / 54)))))
        screen.blit(text, txt_rect)  # текст на кнопках меню
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        menu_sprites.update(event)
    menu_sprites.update()
    pygame.display.flip()
    if info:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if game:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


# Меню конец ----------------------------------------------------------------------------------------------------------

# Справка
class Back_Btn(pygame.sprite.Sprite):  # кнопки меню
    image = load_image("btn_back.png")

    def __init__(self):
        global game_sprites
        super().__init__(info_sprites)
        super().__init__(game_sprites)
        self.image = Back_Btn.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width * 0.1)
        self.rect.y = int(height * 0.1)

    def update(self, *args):
        global menu, info, game
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0] + 22, args[0].pos[1] + 5)):
            info = False
            game = False
            menu = True


info_sprites = pygame.sprite.Group()
with open('info.txt', mode='r', encoding='utf-8') as f:
    text_about = f.read()


def info_call():
    global running, text_about
    btn_back = Back_Btn()
    screen.fill((255, 255, 255))
    info_sprites.draw(screen)
    font = pygame.font.Font(None, 40)
    text = font.render(text_about, True, (200, 0, 0))
    txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 1.5))
    screen.blit(text, txt_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        info_sprites.update(event)
    info_sprites.update()
    pygame.display.flip()
    if menu:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

# Справка

# Игра


game_sprites = pygame.sprite.Group()


def game_call():
    global running
    btn_back = Back_Btn()
    screen.fill((255, 255, 255))
    game_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game_sprites.update(event)
    game_sprites.update()
    pygame.display.flip()
    if menu:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

# Справка


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Wolf & Eggs')
    size = width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    screen = pygame.display.set_mode(size)
    running = True

    # Флаги, отвечающие за вызов функций и отрисовку окна
    log_in = True
    menu = False
    info = False
    game = False

    read_log = False
    read_pass = False
    # -----------------------------------------------------------------------------------------------------------

    # Логин -------------------------------------------------------------------------------------------------------
    login_sprites = pygame.sprite.Group()
    login_panel = Login_panel()
    input_login = Input_login()
    input_pass = Input_password()
    sign_up = Sign_in()
    register = Register()
    # Логин ------------------------------------------------------------------------------------------------------

    # Меню ------------------------------------------------------------------------------------------------------
    menu_sprites = pygame.sprite.Group()
    # Меню ----------------------------------------------------------------------------------------------------------

    # Игра -----------------------------------------------------------------------------------------------------

    # Игра -----------------------------------------------------------------------------------------------------

    # Справка -----------------------------------------------------------------------------------------------------

    # Справка -----------------------------------------------------------------------------------------------------
    clock = pygame.time.Clock()
    while running:
        if log_in:
            log_in_call()
        if menu:
            menu_call()
        if info:
            info_call()
        if game:
            game_call()
        clock.tick(60)
    pygame.quit()
