import pygame
import random

monsterImg = pygame.image.load('Images/monster.png')

class Monster(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1]+32, 32, 32)
        self.image = monsterImg
        self.dist = 3
        self.direction = random.randint(0, 3) #Random direction
        self.steps = random.randint(3, 9) * 32 #Random no of steps to take before changing direction

    def move(self, walls):
        direction_list = ((-1,0), (1,0), (0,-1), (0,1))
        dx, dy = direction_list[self.direction]
        self.rect.x += dx
        self.rect.y += dy

        collide = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                collide = True
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

        self.steps -= 1
        if collide or self.steps == 0:
            #New random direction and no of steps
            self.direction = random.randint(0, 3)
            self.steps = random.randint(3, 9) * 32
