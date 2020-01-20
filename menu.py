import pygame
from helpers import *
from config import *


class Menu():
    def __init__(self, screen, clock, backround_image, position_x, position_y, params=[]):
        self.backround_image = backround_image
        self.screen = screen
        self.clock = clock
        self.position_id = 0
        self.position_x = position_x
        self.position_y = position_y
        self.params = params
        self.font = pygame.font.Font('data/fonts/3614.ttf', 50)
        self.cursor = pygame.image.load('data/img/sh_1.png')

    def run(self):
        running = True
        print('ok')
        while running:
            self.screen.fill([255, 255, 255])
            self.screen.blit(self.backround_image, (0, 0))
            for id, value in enumerate(self.params):
                string = self.font.render(value['name'], 1, pygame.Color('red'))
                self.screen.blit(string, (self.position_x, self.position_y + id * 60))
                if id == self.position_id:
                    self.screen.blit(self.cursor, (self.position_x - 60, self.position_y + id * 60))
            for event in pygame.event.get():
                # при закрытии окна
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if self.position_id < len(self.params) - 1:
                            self.position_id += 1
                    if event.key == pygame.K_UP:
                        if self.position_id > 0:
                            self.position_id -= 1
                    if event.key == pygame.K_SPACE:
                        return self.params[self.position_id]['params']

            pygame.display.flip()
            self.clock.tick(FPS)
