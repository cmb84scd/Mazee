import pygame

wallImg = pygame.image.load('Images/hedge.png')

class Wall(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1]+32, 32, 32)
        self.image = wallImg
