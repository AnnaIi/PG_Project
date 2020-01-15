import pygame


class Spritesheet(object):
    # https://www.pygame.org/wiki/Spritesheet
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None, mirror=False):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return pygame.transform.flip(image, mirror, False)

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None, mirror=False):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey, mirror) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Pagoda(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        spritesheet = Spritesheet('img/pagoda.png')
        self.image = spritesheet.image_at((0, 0, 580, 326), -1)
        self.rect = self.image.get_rect()


class Hitokiri(pygame.sprite.Sprite):
    sprites = {'run_left': [], 'run_right': [], 'sleep_left': [], 'sleep_right': [], 'sword_right': [],
               'sword_left': []}

    def mirror(self):
        self.image = False

    def get_postfix(self):
        if self.way == 1:
            return '_right'
        else:
            return '_left'

    def set_sprite(self):

        self.sprite_id += 1
        if self.sprite_id >= len(self.sprites[self.type_sprite + self.get_postfix()]):
            self.sprite_id = 0

        self.image = self.sprites[self.type_sprite + self.get_postfix()][self.sprite_id]

    def __init__(self, group):
        super().__init__(group)
        spritesheet = Spritesheet('img/Samurai.png')
        self.way = 0  # left лево, right право
        self.move_action = 0  # перемещение 0 или 1
        self.sword = 0  # удар мечем 0 или 1
        self.sword_action = 0  # номер действия удара 0 - 3

        self.sprite_id = 0  # id отображаемого спрайта
        self.type_sprite = 'sleep'
        self.sprites['sleep_right'] = self.sprites['sleep_left'] = spritesheet.images_at(((0, 400, 60, 80),),
                                                                                         colorkey=-1)
        self.sprites['sleep_left'] = spritesheet.images_at(((0, 400, 60, 80),), colorkey=-1, mirror=True)

        self.sprites['run_left'] = spritesheet.images_at((
            (60, 400, 55, 80),
            (120, 400, 47, 80),
            (157, 400, 44, 80),
            (202, 400, 44, 80),
            (245, 400, 55, 80), (290, 400, 47, 80),
            (237, 400, 55, 80),
        ), colorkey=-1)
        self.sprites['run_right'] = spritesheet.images_at((
            (60, 400, 55, 80),
            (120, 400, 47, 80),
            (157, 400, 44, 80),
            (202, 400, 44, 80),
            (245, 400, 55, 80), (290, 400, 47, 80),
            (237, 400, 55, 80),
        ), colorkey=-1, mirror=True)
        self.sprites['sword_right'] = spritesheet.images_at((
            (0, 400, 60, 80),
            (60, 510, 65, 80),
            (75, 510, 95, 80),
            (175, 510, 95, 80),
        ), colorkey=-1)
        self.sprites['sword_left'] = spritesheet.images_at((
            (0, 400, 60, 80),
            (60, 510, 65, 80),
            (75, 510, 95, 80),
            (175, 510, 95, 80),
        ), colorkey=-1, mirror=True)
        self.image = self.sprites['sleep_left'][0]
        self.rect = self.image.get_rect()
        # self.sprites['move'] = pygame.transform.scale(self.image, (20, 20))
        self.rect.x = 500
        self.rect.y = 196

    def set_state_down(self, event):
        if event.key == pygame.K_LEFT:
            self.way = -1
        if event.key == pygame.K_RIGHT:
            self.way = 1
        if event.key == pygame.K_UP:
            self.flight = 1
        if event.key == pygame.K_SPACE:
            self.sword = 1

    def set_state_up(self, event):
        if event.key == pygame.K_LEFT:
            self.way = 0
        if event.key == pygame.K_RIGHT:
            self.way = 0
        if event.key == pygame.K_UP:
            self.flight = 0
        if event.key == pygame.K_SPACE:
            self.sword = 0

    def update(self, *args):
        if self.sword_action > 0 and self.sword_action < 4:
            self.sword_action += 1
        elif self.sword == 1:
            self.type_sprite = 'sword'
            self.sword_action = 1
        elif self.sword_action == 4:
            self.sword_action = 0
            self.type_sprite = 'sleep'

        if self.type_sprite in ('run', 'sleep') and self.way == 0:
            self.sprite_id = 0
            self.type_sprite = 'sleep'
        if self.way in (-1, 1):
            if self.type_sprite == 'sleep':
                self.type_sprite = 'run'
            self.rect.x = self.rect.x + self.way * 20
        self.set_sprite()
        # self.way = 0


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((580, 326))
        self.screen.fill((255, 255, 255))
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        move_sprites = pygame.sprite.Group()
        Pagoda(move_sprites)
        hitokiri = Hitokiri(move_sprites)

        move_sprites.draw(self.screen)
        # move_sprites.update()
        while running:
            self.screen.fill((255, 255, 255))
            move_sprites.draw(self.screen)
            move_sprites.update()

            for event in pygame.event.get():
                # при закрытии окна

                if event.type == pygame.QUIT:
                    running = False
                # при новом клике мыши

                if event.type == pygame.KEYDOWN:
                    pass
                    hitokiri.set_state_down(event)
                if event.type == pygame.KEYUP:
                    pass
                    hitokiri.set_state_up(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    pass
            self.clock.tick(10)
            pygame.display.flip()


game = Game()
game.run()
