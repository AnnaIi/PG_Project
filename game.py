import pygame
from config import *
import sys
from helpers import *
from zombie import Zombie
from hitokiri import Hitokiri
import random


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.backround_image = pygame.image.load('data/img/background.png')
        self.clock = pygame.time.Clock()
        self.zombie_sprites = pygame.sprite.Group()
        self.hitokiri_sprites = pygame.sprite.Group()
        self.weapont_sprites = pygame.sprite.Group()

    def run(self):
        running = True
        self.hitokiri = Hitokiri(self.hitokiri_sprites, position=(300, 290), horisontal_move=False,
                                 weapont_sprites=self.weapont_sprites)
        font = pygame.font.Font(None, 30)
        while running:
            self.screen.fill([255, 255, 255])
            self.screen.blit(self.backround_image, (0, 0))
            ss = random.randint(1, 100)
            if ss == 2:
                Zombie(self.zombie_sprites, horisontal_move=True, position=(20, 280), hitokiri=self.hitokiri,
                       weapont_sprites=self.weapont_sprites, hitokiri_sprites=self.hitokiri_sprites)
            if ss == 3:
                Zombie(self.zombie_sprites, direction=-1, horisontal_move=True, position=(WIDTH - 20, 280),
                       hitokiri=self.hitokiri,
                       weapont_sprites=self.weapont_sprites, hitokiri_sprites=self.hitokiri_sprites)
            for event in pygame.event.get():
                # при закрытии окна
                if event.type == pygame.QUIT:
                    running = False

                # меняем состояние хитокири:
                if event.type == pygame.KEYDOWN:
                    self.hitokiri.set_state_down(event)
                if event.type == pygame.KEYUP:
                    self.hitokiri.set_state_up(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    pass
            self.weapont_sprites.update()
            self.weapont_sprites.draw(self.screen)
            self.hitokiri_sprites.update()
            self.zombie_sprites.update()
            self.zombie_sprites.draw(self.screen)
            self.hitokiri_sprites.draw(self.screen)
            text_m = font.render(f'Убитых зомби: {self.hitokiri.zomby_kill} '
                                 f'Убитых хитокири: {self.hitokiri.life_kill}',
                                 0, (255, 255, 255))
            self.screen.blit(text_m, (20, 20))
            pygame.display.flip()
            self.clock.tick(FPS)
