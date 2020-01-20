import pygame
from config import *
import sys
from helpers import *
from zombie import Zombie
from hitokiri import Hitokiri, Hart
from menu import Menu
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
        self.menu = Menu(
            self.screen,
            self.clock,
            self.backround_image,
            450,
            100,
            [
                {'name': 'EASY', 'params': {'random': 150, 'life': 15, 'fps': 0.8}},
                {'name': 'NORMAL', 'params': {'random': 100, 'life': 10, 'fps': 1}},
                {'name': 'HARD', 'params': {'random': 60, 'life': 3, 'fps': 2}}
            ]
        )
        self.font_zombie = pygame.font.Font('data/fonts/Creepster-Regular.ttf', 130)

    def start_screen(self):
        running = True
        font_hitokiri = pygame.font.Font('data/fonts/3614.ttf', 150)
        string_hitokiri = font_hitokiri.render('H I T O K I R I', 1, pygame.Color('red'))
        font_vs = pygame.font.Font(None, 130)
        string_vs = font_vs.render('VS', 1, (255, 255, 255))
        font_zombie = self.font_zombie
        string_zombie = font_zombie.render('ZOMBIE', 1, pygame.Color('green'))
        while running:
            self.screen.fill([255, 255, 255])
            self.screen.blit(self.backround_image, (0, 0))
            self.screen.blit(string_hitokiri, (100, 60))
            self.screen.blit(string_zombie, (340, 170))
            self.screen.blit(string_vs, (460, 150))
            for event in pygame.event.get():
                # при закрытии окна
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    running = False
            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self):
        self.start_screen()
        params = self.menu.run()
        running = True
        self.hitokiri = Hitokiri(self.hitokiri_sprites, position=(300, 290), horisontal_move=False,
                                 weapont_sprites=self.weapont_sprites, life=params['life'])
        self.hart = Hart(self.screen, self.hitokiri)
        font = pygame.font.Font(None, 30)
        while running:
            self.screen.fill([255, 255, 255])
            self.screen.blit(self.backround_image, (0, 0))
            ss = random.randint(1, params['random'])  # параметр из меню
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
                    terminate()

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
            text_m = font.render(f'SIZE: {self.hitokiri.zomby_kill} ',
                                 0, (255, 255, 255))
            self.hart.write(10, 10) # жизни
            self.screen.blit(text_m, (10, 50)) # очки
            # если жизни кончились, то выходим из цикла
            if self.hitokiri.life < 1:
                running = False
            pygame.display.flip()
            self.clock.tick(FPS * params['fps'])
        # концовка, экран не перерисовывается
        # сверху пишется "game over"
        text_go = self.font_zombie.render('GAME OVER', 1, (255, 215, 0))
        self.screen.blit(text_go, (280, 130))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    terminate()

