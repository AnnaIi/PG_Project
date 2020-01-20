import sys
import pygame


def terminate():
    # выключение системы
    pygame.quit()
    sys.exit()


class Spritesheet(object):
    # https://www.pygame.org/wiki/Spritesheet
    # класс для деления картинки на спрайты
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
        # загрузка общей картинки спрайтов

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        "создаём прямоугольник"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # получение нескольких картинок
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
