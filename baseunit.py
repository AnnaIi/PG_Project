import pygame

from config import *


class Action:
    mirror = False

    def __init__(self, sprite):
        self.frame_id = 0
        self.sprite = sprite
        self.create_sprites()
        self.frames_count = SET_SPRITE_ACTION_COUNT * len(self.sprites)
        self.sprite.image = self.sprites[0]
        if not hasattr(self.sprite, 'rect'):
            # при первом создании экшена создаю ему поле rect и копирую позицию
            self.sprite.rect = self.sprite.image.get_rect()
            self.sprite.rect.x = self.sprite.position[0]
            self.sprite.rect.y = self.sprite.position[1]

    def next_frame(self):
        # каждый вызов меняет frame_id, если нужно, переключает спрайт.
        # На последнем Frames_count возвращает False
        self.frame_id += 1
        mirror = False
        if (self.sprite.direction == 1 and self.mirror) or (self.sprite.direction == -1 and not self.mirror):
            mirror = True
        self.sprite.image = pygame.transform.flip(self.sprites[self.frame_id // SET_SPRITE_ACTION_COUNT - 1],
                                                  mirror,
                                                  False)
        if self.frame_id >= self.frames_count:
            self.frame_id = 0
            return False
        return True


class BaseUnit(pygame.sprite.Sprite):
    def __init__(self, group, **kwargs):
        super().__init__(group)
        # запреты на совершение действий
        self.vertical_move_locked = False
        self.horisontal_move_locked = False
        self.action_move_locked = False
        # свершается ли действие
        self.horisontal_move = False
        self.vertical_move = False
        self.action_move = False
        # направление в котором смотрит юнит
        self.direction = 1
        self.vertical_direction = 0
        self.position = (100, 100)
        # сделала из-за того, что не все спрайты смотрят в одну сторону
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.create_actions()

    def create_actions(self):
        # обязательно для создания в классе-наследнике
        # если не создать, не будет картинки и rect
        pass

    def move(self, x=0, y=0):
        # if self.horisontal_move_locked:
        #     x = 0
        # if self.vertical_move_locked:
        #     y = 0
        # self.rect = self.rect.move(x * self.direction, y * self.vertical_direction)
        if self.vertical_move and not self.vertical_move_locked:
            self.rect.y += y * self.vertical_direction
        if self.horisontal_move and not self.horisontal_move_locked:
            self.rect.x += x * self.direction
