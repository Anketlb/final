import pygame
from os.path import join

class Block(pygame.sprite.Sprite):
    def __init__(self, size, color,x,y):
        super().__init__()
        # self.image = pygame.Surface((size,size))
        # self.image.fill(color)
        self.image = pygame.image.load(join('images', 'player', 'meteor.png'))
        self.image = pygame.transform.scale(self.image, (size + 2,size + 2))
        self.rect = self.image.get_rect(topleft = (x,y))

shape = [
    '  xxxxxxx',
    ' xxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx']
