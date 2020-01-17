import pygame

from baseunit import BaseUnit, Action
from config import *
from helpers import Spritesheet


class ZombieMove(Action):
    def create_sprites(self):
        zombie_spritesheet = Spritesheet('data/img/zombi1.png')
        self.sprites = zombie_spritesheet.images_at((
            (0, 170, 90, 95),
            (90, 170, 90, 95),
            # (180, 170, 90, 95),
            (270, 170, 90, 95),
            # (3, 85, 48, 72),
        ), -1)

    vertical_move_len = 20
    horisontal_move_len = 4


class ZombieKill(Action):
    # не используется, сделать группу спрайтов для умирающих зомби
    def create_sprites(self):
        zombie_spritesheet = Spritesheet('data/img/zombi1.png')
        self.sprites = zombie_spritesheet.images_at((
            (0, 170, 90, 95),
            (0, 190, 90, 75),
            (0, 210, 90, 55),
            (0, 230, 90, 35),
        ), -1)

    vertical_move_len = 20
    horisontal_move_len = 0


class Zombie(BaseUnit):
    def create_actions(self):
        self.move_action = ZombieMove(self)
        self.kill_action = ZombieKill(self)
        self.start_action = self.move_action

    def update(self, *args):
        # если зомби дошёл до конца экрана
        if self.rect.x > WIDTH - 50 and self.direction == 1 or self.rect.x < 50 and self.direction == -1:
            self.horisontal_move_locked = True
            self.vertical_direction = 1
            self.vertical_move = False
            self.vertical_move_locked = False
        # если зомби пересёкся со спрайтом удара и не остановился
        if pygame.sprite.spritecollideany(self, self.weapont_sprites) and not self.horisontal_move_locked:
            self.hitokiri.zomby_kill += 1
            self.kill()
        # усли зомби пересёкся со спрайтом хитокири
        if pygame.sprite.spritecollideany(self, self.hitokiri_sprites):
            self.hitokiri.life_kill += 1
            self.kill()
        # если зомби вышел за границы экрана
        if self.horisontal_move_locked:  # and not self.kill_action.next_frame():
            self.kill()
        # Если зомби может идти, он идёт (меняется картинка)
        if self.horisontal_move and not self.horisontal_move_locked:
            self.start_action.next_frame()
        self.move(self.move_action.horisontal_move_len, self.move_action.vertical_move_len)
