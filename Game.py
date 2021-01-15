import pygame
import sys
import tkinter as tk
from backend import *
from random import randrange
from math import radians

root = tk.Tk()

CONST_SKIN_ID = 0
CONST_COUNT_OF_SKINS = 2
CUSTOM_THEME = {}
PLAYER_LOGIN = ''

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
    image = pygame.transform.scale(image,
                                   (int(image.get_rect()[2] / kx), int(image.get_rect()[3] / ky)))
    return image


# Вход начало ---------------------------------------------------------------------------------------------------


class Login_panel(pygame.sprite.Sprite):
    image = load_image("login_panel.png")

    def __init__(self):
        super().__init__(login_sprites)
        self.image = Login_panel.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width / 2 - self.rect[2] / 2)
        self.rect.y = int(height / 2 - self.rect[3] / 2)


class Input_login(pygame.sprite.Sprite):
    image = load_image("input_login.png")

    def __init__(self):
        super().__init__(login_sprites)
        self.image = Input_login.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width / 2 - self.rect[2] / 2) * 1.03
        self.rect.y = int(height / 2 - self.rect[3] / 2) * 0.78
        self.font = pygame.font.Font(None, 50)
        self.string = ''

    def update(self, *args):
        global read_log, error_menu_limit, read_pass, error_wrong_data, error_reg, error_sign
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
        self.rect.x = int(width / 2 - self.rect[2] / 2) * 1.03
        self.rect.y = int(height / 2 - self.rect[3] / 2) * 1.05
        self.font = pygame.font.Font(None, 50)
        self.string = ''

    def update(self, *args):
        global read_log, read_pass, error_menu_limit, error_wrong_data, error_reg, error_sign
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
        self.rect.x = int(width / 2 - self.rect[2] / 2) * 0.82
        self.rect.y = int(height / 2 - self.rect[3] / 2) * 1.34

    def update(self, *args):
        global menu, log_in, input_pass, input_login, error_wrong_data, error_sign, error_reg, error_menu_limit, \
            PLAYER_LOGIN
        if error_sign:
            font = pygame.font.Font(None, 60)
            text = font.render(check_login_password(input_login.string, input_pass.string), True,
                               (100, 0, 0))
            txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 0.2))
            screen.blit(text, txt_rect)
        if self.rect.collidepoint((pygame.mouse.get_pos()[0] + 22, pygame.mouse.get_pos()[1] + 5)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(
                    (args[0].pos[0] + 22,
                     args[0].pos[1] + 5)):  # Подбор ------------------------------------------
            error_reg, error_sign, error_menu_limit, error_wrong_data = False, False, False, False
            if input_login.string and input_pass.string and check_login_password(input_login.string,
                                                                                 input_pass.string):
                if isinstance(check_login_password(input_login.string, input_pass.string), tuple):
                    menu = True  # Переключение на окно Меню ----------------------------------------------------------
                    log_in = False
                    error_wrong_data = False
                    error_sign = False
                    PLAYER_LOGIN = check_login_password(input_login.string, input_pass.string)[1]
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
        self.rect.x = int(width / 2 - self.rect[2] / 2) * 1.23
        self.rect.y = int(height / 2 - self.rect[3] / 2) * 1.34

    def update(self, *args):
        global menu, log_in, error_wrong_data, input_pass, input_login, error_reg, error_sign, error_menu_limit, \
            PLAYER_LOGIN
        if error_wrong_data:
            font = pygame.font.Font(None, 60)
            text = font.render('Неверные данные', True, (100, 0, 0))
            txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 0.2))
            screen.blit(text, txt_rect)
        if error_reg:
            font = pygame.font.Font(None, 60)
            text = font.render(registration(input_login.string, input_pass.string), True,
                               (100, 0, 0))
            txt_rect = text.get_rect(center=(int(width / 2) * 1.03, int(height / 2) * 0.2))
            screen.blit(text, txt_rect)
        if self.rect.collidepoint((pygame.mouse.get_pos()[0] + 22, pygame.mouse.get_pos()[1] + 5)):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(
                    (args[0].pos[0] + 22,
                     args[0].pos[1] + 5)):  # Подбор ------------------------------------------
            error_reg, error_sign, error_menu_limit, error_wrong_data = False, False, False, False
            if input_login.string and input_pass.string:
                if not registration(input_login.string, input_pass.string):
                    error_wrong_data = False
                    error_reg = False
                    error_sign = False
                    menu = True  # Переключение на окно Меню ----------------------------------------------------------
                    log_in = False
                    PLAYER_LOGIN = check_login_password(input_login.string, input_pass.string)[1]
                else:
                    error_reg = True
                    error_wrong_data = False
                    error_sign = False
            else:
                error_wrong_data = True
                error_reg = False


def log_in_call():
    global running, menu
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
        global info_sprites, game_sprites, settings_sprites, rating_sprites
        super().__init__(menu_sprites)
        super().__init__(game_sprites)
        super().__init__(settings_sprites)
        super().__init__(info_sprites)
        super().__init__(rating_sprites)
        self.image = Menu_Background.image
        self.rect = self.image.get_rect()
        self.rect.bottom = height


class Menu_Btn(pygame.sprite.Sprite):  # кнопки меню
    image = load_image("menu_btn.png")

    def __init__(self):
        super().__init__(menu_sprites)
        self.image = Menu_Btn.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width / 2 - self.rect[2] / 2)


class Btn_Start(Menu_Btn):
    def update(self, *args):
        global menu, game, set_game_background_field, wolf, rabbit, first_ball
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0] + 22, args[0].pos[1] + 5)):
            game = True
            menu = False
            set_game_background_field.__init__()
            wolf.__init__()
            rabbit.__init__()
            first_ball.__init__(0)
            second_ball.__init__(1)
            third_ball.__init__(2)
            fourth_ball.__init__(3)
            broken.__init__()
            broken_2.__init__(1)


class Btn_Settings(Menu_Btn):
    def update(self, *args):
        global menu, settings
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0] + 22, args[0].pos[1] + 5)):
            settings = True
            menu = False


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
        self.rect.x = int(width * 0.7 - self.rect[2] / 2)
        self.rect.y = int(height * 0.75 - self.rect[3] / 2)

    def update(self, *args):
        global menu, rate
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0], args[0].pos[1])):
            rate = True
            menu = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


def menu_call(font):
    global running, menu_sprites, info, game
    menu_list_of_btn_names = ['Играть', 'Настройки', 'Справка']
    screen.fill((255, 255, 255))
    menu_sprites.draw(screen)
    for i in range(3):
        text = font.render(menu_list_of_btn_names[i], True, (255, 255, 255))
        txt_rect = text.get_rect(center=(width / 2,
                                         int(height * 0.45 + i * (
                                                 btn_start.rect[3] + int(height / 54)))))
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
        global game_sprites, settings_sprites, back_btn_sprites, rating_sprites
        super().__init__(info_sprites)
        super().__init__(settings_sprites)
        super().__init__(game_sprites)
        super().__init__(back_btn_sprites)
        super().__init__(rating_sprites)
        self.image = Back_Btn.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width * 0.1)
        self.rect.y = int(height * 0.1)

    def update(self, *args):
        global menu, info, game, settings, rate
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0] + 22, args[0].pos[1] + 5)):
            info = False
            settings = False
            game = False
            menu = True
            rate = False


with open('info.txt', mode='r', encoding='utf-8') as f:
    text_about = f.read()


def info_call(font):
    global running, text_about
    screen.fill((255, 255, 255))
    info_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        info_sprites.update(event)
    sp = text_about.split('. ')
    for n, i in enumerate(sp):
        text = font.render(i, True, (0, 0, 0))
        txt_rect = (int(width * 0.25), int(height * 0.3 + n * height * 0.03), 0, 0)
        screen.blit(text, txt_rect)
    info_sprites.update()
    pygame.display.flip()
    if menu:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


# Справка

# Настройки


class Btn_Choose(pygame.sprite.Sprite):
    image = load_image("btn_choose.png")

    def __init__(self):
        super().__init__(settings_sprites)
        self.image = Btn_Choose.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width * 0.3)
        self.rect.y = int(height * 0.7)

    def update(self, *args):
        global theme, CONST_SKIN_ID, CUSTOM_THEME
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0], args[0].pos[1])):
            CONST_SKIN_ID = theme.temp_const
            CUSTOM_THEME = {}
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


class Btn_Choose_Level_1(pygame.sprite.Sprite):
    image = load_image("button_1.png")

    def __init__(self):
        super().__init__(settings_sprites)
        self.image = Btn_Choose_Level_1.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width * 0.25)
        self.rect.y = int(height * 0.15)

    def update(self, *args):
        global theme, CONST_SKIN_ID, CUSTOM_THEME, level_game
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0], args[0].pos[1])):
            level_game = 0
            print(f"-------------------level = {level_game}")
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


class Btn_Choose_Level_2(pygame.sprite.Sprite):
    image = load_image("button_2.png")

    def __init__(self):
        super().__init__(settings_sprites)
        self.image = Btn_Choose_Level_2.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width * 0.67)
        self.rect.y = int(height * 0.15)

    def update(self, *args):
        global theme, CONST_SKIN_ID, CUSTOM_THEME, level_game
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0], args[0].pos[1])):
            level_game = 1
            print(f"-------------------level = {level_game}")
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


class Btn_My_Theme(pygame.sprite.Sprite):
    image = load_image("btn_my_theme.png")

    def __init__(self):
        super().__init__(settings_sprites)
        self.image = Btn_My_Theme.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width * 0.52)
        self.rect.y = int(height * 0.7)

    def update(self, *args):
        global CUSTOM_THEME
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0], args[0].pos[1])):
            CUSTOM_THEME = customize_game_theme()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


class Btn_Left(pygame.sprite.Sprite):
    image = load_image("btn_left.png")

    def __init__(self):
        super().__init__(settings_sprites)
        self.image = Btn_Left.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width * 0.15)
        self.rect.y = int(height * 0.5)

    def update(self, *args):
        global theme, CONST_COUNT_OF_SKINS
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0], args[0].pos[1])):
            if theme.temp_const == 0:
                theme.temp_const = CONST_COUNT_OF_SKINS - 1
            else:
                theme.temp_const -= 1
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


class Btn_Right(pygame.sprite.Sprite):
    image = load_image("btn_right.png")

    def __init__(self):
        super().__init__(settings_sprites)
        self.image = Btn_Right.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width * 0.78)
        self.rect.y = int(height * 0.5)

    def update(self, *args):
        global theme, CONST_COUNT_OF_SKINS
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint((args[0].pos[0], args[0].pos[1])):
            if theme.temp_const == CONST_COUNT_OF_SKINS - 1:
                theme.temp_const = 0
            else:
                theme.temp_const += 1
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)


class Theme(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__(settings_sprites)

        self.temp_const = 0
        self.image = load_image('skins/{}/theme.png'.format(self.temp_const))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,
                                            (self.rect.width, int(self.rect.height * 0.7)))
        self.rect.x = int(width * 0.235)
        self.rect.y = int(height * 0.29)

    def update(self, *args):
        self.image = load_image('skins/{}/theme.png'.format(self.temp_const))
        self.image = pygame.transform.scale(self.image,
                                            (self.rect.width, int(self.rect.height * 0.7)))


def settings_call():
    global running
    screen.fill((255, 255, 255))
    settings_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        settings_sprites.update(event)
    settings_sprites.update()
    pygame.display.flip()
    if menu:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


# Настройки

# Игра


class Pause(pygame.sprite.Sprite):
    image = load_image('pause.png')

    def __init__(self):
        super().__init__(pause_sprites)

        self.image = Pause.image
        self.rect = self.image.get_rect()
        self.rect.x = int(width / 2 - self.rect[2] / 2)
        self.rect.y = int(height / 2 - self.rect[3] / 2) + 50


GAMEBACK_0 = load_image('skins/{}/bgf.jpg'.format(CONST_SKIN_ID))


class GameBackgroundField(pygame.sprite.Sprite):  # фон меню
    def __init__(self):
        global game_sprites, GAMEBACK_0, CONST_SKIN_ID, CUSTOM_THEME, point_count, live_count
        super().__init__(game_sprites)
        self.i = 0
        point_count = 0
        live_count = 6
        if CUSTOM_THEME:
            GAMEBACK_0 = load_image(CUSTOM_THEME['фон'])
        else:
            GAMEBACK_0 = load_image('skins/{}/bgf.jpg'.format(CONST_SKIN_ID))
        self.image = GAMEBACK_0
        self.image = pygame.transform.scale(self.image, (int(width * 0.51), int(height * 0.52)))
        self.rect = self.image.get_rect()
        self.rect.x = int(width * 0.235)
        self.rect.y = int(height * 0.29)


WOLF = load_image('skins/{}/1.png'.format(CONST_SKIN_ID))
WOLF_1 = load_image('skins/{}/2.png'.format(CONST_SKIN_ID))
WOLF_2 = load_image('skins/{}/3.png'.format(CONST_SKIN_ID))
WOLF_3 = load_image('skins/{}/4.png'.format(CONST_SKIN_ID))


class Wolf(pygame.sprite.Sprite):
    """
    image = WOLF
    image2 = WOLF_1
    image3 = WOLF_2
    image4 = WOLF_3"""

    def __init__(self, n=0, kx=0.3, ky=0.5):
        global game_sprites, WOLF, WOLF_1, WOLF_2, WOLF_3, CONST_SKIN_ID
        super().__init__(game_sprites)
        WOLF = load_image('skins/{}/1.png'.format(CONST_SKIN_ID))
        WOLF_1 = load_image('skins/{}/2.png'.format(CONST_SKIN_ID))
        WOLF_2 = load_image('skins/{}/3.png'.format(CONST_SKIN_ID))
        WOLF_3 = load_image('skins/{}/4.png'.format(CONST_SKIN_ID))
        d = {0: WOLF, 1: WOLF_1, 2: WOLF_2, 3: WOLF_3}
        self.n = n
        self.image = d[n]
        self.image = pygame.transform.scale(self.image, (int(width * 0.2), int(height * 0.2)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = int(width * kx)
        self.y = int(height * ky)
        self.rect.x = self.x
        self.rect.y = self.y
        self.isShow = True

    def change_position(self, n=0, kx=0.3, ky=0.5):
        global WOLF, WOLF_1, WOLF_2, WOLF_3
        d = {0: WOLF, 1: WOLF_1, 2: WOLF_2, 3: WOLF_3}
        self.image = d[n]
        self.image = pygame.transform.scale(self.image, (int(width * 0.2), int(height * 0.2)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = int(width * kx)
        self.n = n
        self.y = int(height * ky)
        self.rect.x = self.x
        self.rect.y = self.y
        i = 0


RABBIT = load_image('skins/{}/rabbit.png'.format(CONST_SKIN_ID))


class Rabbit(pygame.sprite.Sprite):

    def __init__(self):
        global game_sprites, RABBIT, CUSTOM_THEME
        super().__init__(game_sprites)
        if CUSTOM_THEME:
            RABBIT = load_image(CUSTOM_THEME['заяц'])
        else:
            RABBIT = load_image('skins/{}/rabbit.png'.format(CONST_SKIN_ID))
        self.image = RABBIT
        self.image = pygame.transform.scale(self.image, (int(width * 0.1), int(height * 0.1)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = int(width * 0.295)
        self.y = int(height * 0.3)
        self.rect.x = -100
        self.rect.y = -100
        self.isShow = False
        self.long = 0

    def up(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.isShow = True

    def down(self):
        self.rect.x = -400
        self.rect.y = -400
        self.isShow = False


BALL = load_image('skins/{}/egg.png'.format(CONST_SKIN_ID))
BROKEN_EGG = load_image('skins/{}/broken_egg.png'.format(CONST_SKIN_ID))


class BrokenEgg(pygame.sprite.Sprite):
    def __init__(self, n=0):
        global game_sprites, BALL, CONST_SKIN_ID, CUSTOM_THEME
        super().__init__(game_sprites)
        if CUSTOM_THEME:
            BALL = load_image(CUSTOM_THEME['яйцо'])
        else:
            BALL = load_image('skins/{}/broken_egg.png'.format(CONST_SKIN_ID))
        self.image = BALL
        self.image = pygame.transform.scale(self.image, (int(width * 0.04), int(height * 0.04)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.k = 5
        if n == 0:
            self.x = int(width * 0.33)
            self.y = int(height * 0.7)

        else:
            self.x = int(width * 0.6)
            self.y = int(height * 0.7)
        self.rect.x = - 1000
        self.rect.y = - 1000

    def move(self):
        self.rect.y = self.y
        self.rect.x = self.x
        self.k = 0

    def update(self, *args, **kwargs) -> None:
        self.k += 1
        if self.k == FPS * 2:
            self.rect.x = - 1000
            self.rect.y = - 1000


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Ball(pygame.sprite.Sprite):

    def __init__(self, n):
        global game_sprites, BALL, CONST_SKIN_ID, CUSTOM_THEME, point_count
        super().__init__(game_sprites)
        if CUSTOM_THEME:
            BALL = load_image(CUSTOM_THEME['яйцо'])
        else:
            BALL = load_image('skins/{}/egg.png'.format(CONST_SKIN_ID))
        self.image = BALL
        self.image = pygame.transform.scale(self.image, (int(width * 0.025), int(height * 0.025)))
        self.sImage = self.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = int(width)
        self.rect.y = int(height)
        self.long = 3 * FPS
        self.wait = randrange(FPS * 2, FPS * 15)
        self.n = n
        print(n)
        self.isWolfCatch = False
        if n == 0:
            self.x = 0.265
            self.y = 0.58
            self.steps = [(30, 5), (25, 5), (45, 30)]
            self.step = 0
            self.k = 0
        elif n == 1:
            self.x = 0.265
            self.y = 0.465
            self.steps = [(30, 5), (25, 5), (45, 30)]
            self.step = 0
            self.k = 0
        elif n == 2:
            self.x = 0.69
            self.y = 0.58
            self.steps = [(-50, 14), (-50, 7), (-45, 0)]
            self.step = 0
            self.k = 0
        elif n == 3:
            self.x = 0.69
            self.y = 0.46
            self.steps = [(-50, 14), (-50, 7), (-45, 0)]
            self.step = 0
            self.k = 0
        self.isRun = False

    def change_position(self, x, y):
        self.rect.x = self.rect.x + x
        self.rect.y = self.rect.y + y

    def rotate(self, rot):
        self.image = pygame.transform.rotate(self.image, rot)
        self.mask = pygame.mask.from_surface(self.image)

    def start(self, tick):
        if self.k > self.wait and [first_ball.isRun,
                                   second_ball.isRun,
                                   third_ball.isRun,
                                   fourth_ball.isRun].count(True) < 3 + (2 * level_game):
            self.rect.x = int(width * self.x)
            self.rect.y = int(height * self.y)
            self.long = 3 * FPS - tick // 300
            if self.long < FPS // 2:
                self.long = FPS // 2
            self.image = self.sImage
            self.mask = pygame.mask.from_surface(self.image)
            self.isRun = True
            self.start_tick = tick
            print(self.long)
        self.k += 1

    def move(self, tick):
        if tick == self.start_tick + self.long // 3 * (self.step + 1):
            if self.step == 3:
                self.main_opt()
                self.fail()
            else:
                if self.step == 2 and wolf.n == self.n:
                    self.main_opt()
                    self.give_point()
                else:
                    self.change_position(*self.steps[self.step])
                    self.rotate([30, -30, 30, -30][self.n])
                    self.step += 1
        elif self.start_tick + self.long // 3 * 3 < tick < self.start_tick + self.long // 3 * 4 \
                and wolf.n == self.n:
            self.main_opt()
            self.give_point()

    def fail(self):
        global live_count
        if self.n in {0, 1}:
            broken.move()
        else:
            broken_2.move()
        if rabbit.isShow:
            live_count -= 1
        else:
            live_count -= 2
        if live_count <= 0:
            print(PLAYER_LOGIN, point_count)
            update_rating(PLAYER_LOGIN, level=level_game, score=point_count)
            pause(False)


    def main_opt(self):
        self.k = 0
        self.isRun = False
        self.wait = randrange(0, FPS * 5)
        self.step = 0
        self.isWolfCatch = False
        self.change_position(-1000, -1000)

    def give_point(self):
        global point_count
        point_count += 1
        if point_count % 100 == 0:
            self.long += FPS + randrange(FPS * -0.3, FPS * 0.3)


def pause(dr=True):
    global btn_back, info, settings, game, menu
    f = True
    while f:
        if dr:
            pause_sprites.draw(screen)
        back_btn_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and dr:
                if event.key == pygame.K_ESCAPE:
                    f = False
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    btn_back.rect.collidepoint((event.pos[0] + 22, event.pos[1] + 5)):
                info = False
                settings = False
                game = False
                menu = True
                f = False
                break
            pause_sprites.update(event)
            back_btn_sprites.update(event)
        pause_sprites.update()
        pygame.display.flip()


def game_call():
    global running, wolfs, wolf, point_count, live_count
    if wolfs[0]:
        wolf.change_position()
    elif wolfs[1]:
        wolf.change_position(1, 0.3, 0.5)
    elif wolfs[2]:
        wolf.change_position(2, 0.47, 0.5)
    else:
        wolf.change_position(3, 0.47, 0.5)
    set_game_background_field.i += 1
    screen.fill((255, 255, 255))
    print([first_ball.isRun,
           second_ball.isRun,
           third_ball.isRun,
           fourth_ball.isRun])
    if rabbit.isShow:
        rabbit.long += 1
    if rabbit.long > SEC_LONG * FPS + randrange(SEC_LONG * FPS // -2, SEC_LONG * FPS // 2):
        rabbit.long = 0
        rabbit.down()
    if set_game_background_field.i % \
            (SEC_START * FPS + randrange(SEC_START * FPS // -2, SEC_START * FPS // 2)) == 0:
        rabbit.up()

    if first_ball.isRun:
        first_ball.move(set_game_background_field.i)
    else:
        first_ball.start(set_game_background_field.i)
    if second_ball.isRun:
        second_ball.move(set_game_background_field.i)
    else:
        second_ball.start(set_game_background_field.i)
    if third_ball.isRun:
        third_ball.move(set_game_background_field.i)
    else:
        third_ball.start(set_game_background_field.i)
    if fourth_ball.isRun:
        fourth_ball.move(set_game_background_field.i)
    else:
        fourth_ball.start(set_game_background_field.i)

    game_sprites.draw(screen)
    draw_text(screen, str(point_count), 40, width // 2, height // 4 * 1 + height // 14, 'BLACK')
    draw_text(screen, ('lives - ' + str(live_count)), 40, width // 4 * 3 - width // 10, height // 4 * 1 + height // 14, 'RED')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause()
            if event.key == pygame.K_a:
                wolfs = [0 for i in range(4)]
                wolfs[0] = 1
            if event.key == pygame.K_q:
                wolfs = [0 for i in range(4)]
                wolfs[1] = 1
            if event.key == pygame.K_d:
                wolfs = [0 for i in range(4)]
                wolfs[2] = 1
            if event.key == pygame.K_e:
                wolfs = [0 for i in range(4)]
                wolfs[3] = 1
        game_sprites.update(event)
    game_sprites.update()
    pygame.display.flip()
    if menu:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


# Игра

# Рейтинг
IN_TOP_10 = False


def rating_call(font):
    global running, PLAYER_LOGIN, IN_TOP_10
    screen.fill((255, 255, 255))
    text = font.render('Топ 10 игроков( Позиция / Логин / Рекорд )', True, (0, 0, 0))
    txt_rect = text.get_rect(center=(int(width / 2),
                                     int(height / 2) * 0.7))
    rating_sprites.draw(screen)
    screen.blit(text, txt_rect)
    for n, i in enumerate(get_top10(1)):
        if PLAYER_LOGIN in i:
            IN_TOP_10 = True
        text = font.render(' '.join(map(str, list(i))), True, (0, 0, 0))
        txt_rect = text.get_rect(center=(int(width / 2),
                                         int(height / 2) * 0.8 + n * int(height / 2) * 0.08))
        screen.blit(text, txt_rect)
    if not IN_TOP_10:
        text = font.render(get_rank_player(PLAYER_LOGIN, 1), True, (0, 0, 0))
        txt_rect = text.get_rect(center=(int(width / 2),
                                         int(height / 2) * 1.6))
        screen.blit(text, txt_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        rating_sprites.update(event)
    rating_sprites.update()
    pygame.display.flip()
    if menu:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


# Рейтинг


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Wolf & Eggs')
    SIZE = width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    screen = pygame.display.set_mode(SIZE)
    running = True

    # Флаги, отвечающие за вызов функций и отрисовку окна
    log_in = True
    menu = False
    info = False
    settings = False
    game = False
    rate = False
    wolfs = [1, 0, 0, 0]

    temp_const = 0

    read_log = False
    read_pass = False
    FPS = 60
    # -----------------------------------------------------------------------------------------------------------

    # Группы спрайтов
    login_sprites = pygame.sprite.Group()
    menu_sprites = pygame.sprite.Group()
    game_sprites = pygame.sprite.Group()
    settings_sprites = pygame.sprite.Group()
    info_sprites = pygame.sprite.Group()
    pause_sprites = pygame.sprite.Group()
    rating_sprites = pygame.sprite.Group()
    back_btn_sprites = pygame.sprite.Group()
    # Группы спрайтов

    # Логин -------------------------------------------------------------------------------------------------------
    login_panel = Login_panel()
    input_login = Input_login()
    input_pass = Input_password()
    sign_up = Sign_in()
    register = Register()
    register.__init__()
    # Логин ------------------------------------------------------------------------------------------------------

    # Меню ------------------------------------------------------------------------------------------------------
    menu_background = Menu_Background()
    ''' 
    font = pygame.font.Font(None, 50)
    '''
    btn_start, btn_settings, btn_info = Btn_Start(), Btn_Settings(), Btn_Info()
    for n, i in enumerate([btn_start, btn_settings, btn_info]):
        i.rect.y = int(height * 0.4 + n * (i.rect[3] + int(height / 54)))
    cup = Cup()
    exit_btn = Exit_Btn()
    # Меню ----------------------------------------------------------------------------------------------------------

    # Игра -----------------------------------------------------------------------------------------------------
    set_game_background_field = GameBackgroundField()
    rabbit = Rabbit()
    wolf = Wolf()
    first_ball = Ball(0)
    second_ball = Ball(1)
    third_ball = Ball(2)
    fourth_ball = Ball(3)
    broken = BrokenEgg()
    broken_2 = BrokenEgg(1)
    pause_img = Pause()
    SEC_START = 5
    SEC_LONG = 5
    level_game = 1

    # Игра -----------------------------------------------------------------------------------------------------

    # Общие переменные
    btn_back = Back_Btn()
    # Общие переменные

    # Настройки -----------------------------------------------------------------------------------------------------
    btn_left = Btn_Left()
    btn_right = Btn_Right()
    btn_choose = Btn_Choose()
    btn_choose_level_1 = Btn_Choose_Level_1()
    btn_choose_level_2 = Btn_Choose_Level_2()
    btn_my_theme = Btn_My_Theme()
    theme = Theme()
    # Настройки -----------------------------------------------------------------------------------------------------

    # Справка -----------------------------------------------------------------------------------------------------
    # Справка -----------------------------------------------------------------------------------------------------

    clock = pygame.time.Clock()
    while running:
        if log_in:
            log_in_call()
        if menu:
            menu_call(pygame.font.Font(None, 50))
        if info:
            info_call(pygame.font.Font(None, 35))
        if settings:
            settings_call()
        if game:
            game_call()
        if rate:
            rating_call(pygame.font.Font(None, 60))
        clock.tick(FPS)
    pygame.quit()
