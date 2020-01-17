import pygame

from baseunit import BaseUnit, Action
from config import *
from helpers import Spritesheet


class HitokiriSleep(Action):
    def create_sprites(self):
        spritesheet = Spritesheet('data/img/Samurai.png')
        self.sprites = spritesheet.images_at(((0, 400, 60, 80),),
                                             colorkey=-1)
        self.mirror = False

    vertical_move_len = 0
    horisontal_move_len = 0


class HitokiriMove(Action):
    def create_sprites(self):
        spritesheet = Spritesheet('data/img/Samurai.png')
        self.mirror = True
        self.sprites = spritesheet.images_at((
            (60, 400, 55, 80),
            (120, 400, 47, 80),
            (157, 400, 44, 80),
            (202, 400, 44, 80),
            (245, 400, 55, 80),
            (290, 400, 47, 80),
            # (237, 400, 55, 80),
        ), colorkey=-1)

    vertical_move_len = 0
    horisontal_move_len = 10


class HitokiriSword(Action):
    def create_sprites(self):
        spritesheet = Spritesheet('data/img/Samurai.png')
        self.mirror = False
        self.sprites = spritesheet.images_at((
            (0, 400, 60, 80),
            (60, 510, 65, 80),
            (75, 510, 95, 80),
            (175, 510, 95, 80),
        ), colorkey=-1, )

    vertical_move_len = 0
    horisontal_move_len = 0


class WeapontSprite(pygame.sprite.Sprite):
    def __init__(self, group, hitokiri):
        super().__init__(group)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        if hitokiri.direction == -1:
            self.rect = pygame.Rect(hitokiri.rect.x - 20, hitokiri.rect.y, 20, 70)
        else:
            self.rect = pygame.Rect(hitokiri.rect.x + 75, hitokiri.rect.y, 40, 70)
        # координаты спрайта удара


class Hitokiri(BaseUnit):
    zomby_kill = 0  # счетчик зомби
    life_kill = 0  # счетчик потерянных жизней

    def create_actions(self):
        self.sleep_action = HitokiriSleep(self)
        self.move_action = HitokiriMove(self)
        self.sword_action = HitokiriSword(self)
        self.start_action = self.sleep_action  # начальное действие
        self.sword = None  # спрайт меча

    def update(self):
        if self.rect.x > WIDTH - 100 and self.direction == 1 or self.rect.x < 100 and self.direction == -1:
            self.horisontal_move = False  # хитокири не может уйти за границы дисплея
        if self.action_move:
            if not self.sword:
                self.sword = WeapontSprite(self.weapont_sprites, self)
                # print(self.sword)
            if not self.sword_action.next_frame():
                self.action_move = False
                self.horisontal_move_locked = False
                self.vertical_move_locked = False
                self.sword.kill()
                self.sword = None
                # print(self.sword)
        elif self.horisontal_move:
            self.move_action.next_frame()
        else:
            self.sleep_action.next_frame()
        self.move(self.move_action.horisontal_move_len, self.move_action.vertical_move_len)
        # print(self.life_kill, self.zomby_kill)

    def set_state_down(self, event):
        # при нажатой кнопке
        if event.key == pygame.K_LEFT:
            self.direction = -1
            self.horisontal_move = True
        if event.key == pygame.K_RIGHT:
            self.direction = 1
            self.horisontal_move = True
        if event.key == pygame.K_SPACE:
            self.action_move = True
            self.vertical_move_locked = True
            self.horisontal_move_locked = True

    def set_state_up(self, event):
        # отпускаем кнопку
        if event.key == pygame.K_LEFT:
            self.horisontal_move = False
        if event.key == pygame.K_RIGHT:
            self.horisontal_move = False
        if event.key == pygame.K_SPACE:
            pass
