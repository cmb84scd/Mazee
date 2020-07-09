import pygame

finishImg = pygame.image.load('Images/gate.png')

class Finish(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1]+32, 32, 32)
        self.image = finishImg
