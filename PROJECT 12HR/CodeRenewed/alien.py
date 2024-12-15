import pygame
from os.path import join

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path = 'images/enemy/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.mask = pygame.mask.from_surface(self.image)

        #points
        if color == 'Larvea': self.value = 100
        elif color == 'Finsta': self.value = 200
        else: self.value = 300

    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        # self.image = pygame.image.load(join('images','enemy','extra.png')).convert_alpha()
        self.image = pygame.image.load(join('images','enemy','Cleaf.png')).convert_alpha()

        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            self.image = pygame.transform.flip(self.image, True,False)
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x, 40))

    def update(self):
        self.rect.x += self.speed