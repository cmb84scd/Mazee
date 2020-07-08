import pygame

playerImg = pygame.image.load('Images/player.png')

class Player(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1]+32, 32, 32) #x-axis, y-axis, width, height
        self.image = playerImg

    def move(self, dx, dy):
        #Move each axis separately. NB this checks for collisions both times
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        #Move the rect
        self.rect.x += dx
        self.rect.y += dy

        #If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: #Moving right, hit the left side of wall
                    self.rect.right = wall.rect.left
                if dx < 0: #Moving left, hit the right side of wall
                    self.rect.left = wall.rect.right
                if dy > 0: #Moving down, hit the top side of wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: #Moving up, hit the bottom side of wall
                    self.rect.top = wall.rect.bottom
