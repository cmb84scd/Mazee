import pygame
import random
import os
from player import Player
#from monster import Monster
from wall import Wall

os.environ['SDL_VIDEO_CENTERED'] = '1'
#Initalise pygame
pygame.init()

#Colours required
black = (0,0,0)
blue = (0,0,255)
green = (0,200,0)
red = (255,0,0)
orange = (255,200,0)
bright_green = (0,255,0)
light_blue = (170,180,255)
white = (255,255,255)

#Set up the display
width = 640
height = 512 #480 + 32 to allow for info bar at top
screen = pygame.display.set_mode((width, height))
caption = pygame.display.set_caption('Mazee!')
clock = pygame.time.Clock()

#Load game images
background = pygame.image.load('Images/path.png')
playerImg = pygame.image.load('Images/player.png')
monsterImg = pygame.image.load('Images/monster.png')
#wallImg = pygame.image.load('Images/hedge.png')
finishImg = pygame.image.load('Images/gate.png')
lifeImg = pygame.image.load('Images/life.png')

#Set the icon (image on top left of game window)
pygame.display.set_icon(playerImg)

class Monster(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1]+32, 32, 32)
        self.image = monsterImg
        self.dist = 3
        self.direction = random.randint(0, 3) #Random direction
        self.steps = random.randint(3, 9) * 32 #Random no of steps to take before changing direction

    def move(self):
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

#Class for end rect
class Finish(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1]+32, 32, 32)
        self.image = finishImg

#Variables
currentLevel = 0
lives = 3

#Holds the level layout in a list of strings
levels = [[
'WWWWWWWWWWWWWWWWWWWW',
'WP          W      W',
'W         WWWWWW   W',
'W   WWWW       W   W',
'W   W        WWWW  W',
'W WWW  WWWW        W',
'W   WM    W W      W',
'W   W     W   WWW WW',
'W   WWW WWW   W W  W',
'W     W   W   W W  W',
'WWW   W   WWWWW W  W',
'W W      WW        W',
'W W   WWWW   WWWWWWW',
'W     W           FW',
'WWWWWWWWWWWWWWWWWWWW',
],
[
'WWWWWWWWWWWWWWWWWWWW',
'W W     W     W   FW',
'W W     W     W    W',
'W W  W  W  W  W  WWW',
'W W  W  W  W  W    W',
'W W  W  W  W  W    W',
'W W  W  W  W  W  W W',
'W    W  M  W  W  W W',
'W    W     W  W  WWW',
'WWW  WWWWWWW  W    W',
'W      W      W    W',
'W      W  WWWWWWW  W',
'WWWWW  W           W',
'WP     W           W',
'WWWWWWWWWWWWWWWWWWWW',
],
[
'WWWWWWWWWWWWWWWWWWWW',
'WP W           W   W',
'W  W  WWWW  WWWW W W',
'W  W     W       W W',
'W  WWWW  W    WWWW W',
'W     W  W  WW     W',
'W     W  W  W  WWWWW',
'WWWW  W  W MW     FW',
'W  W  W  W  WWWWWWWW',
'W  W     W         W',
'W  W     W         W',
'W  W  WWWWWWWWWWW  W',
'W   M           W  W',
'W               W  W',
'WWWWWWWWWWWWWWWWWWWW',
],
[
'WWWWWWWWWWWWWWWWWWWW',
'W     W            W',
'W     W        M   W',
'W  W  W  WWWWWWWW  W',
'W  W  W  W         W',
'W  W  W  W         W',
'W  W  W  W  WWWWWWWW',
'WP W  W  W         W',
'WWWW  W  W         W',
'W     W  WWWWWWWW  W',
'W     W  W         W',
'W  WWWW  W         W',
'W        W  WWWWWWWW',
'WM       W        FW',
'WWWWWWWWWWWWWWWWWWWW',
],
[
'WWWWWWWWWWWWWWWWWWWW',
'W  W   M    W     FW',
'W  W        WWW W  W',
'W  W  WWWW    W WWWW',
'W  W     W    W    W',
'W  WWWW  WWWW W  W W',
'W    MW     W WWWW W',
'W     W     W      W',
'W  W  WWWW  WWWWWWWW',
'W  W     W       M W',
'W  W     W         W',
'WWWW  W  WWWWWWWW  W',
'W     W            W',
'WP    W            W',
'WWWWWWWWWWWWWWWWWWWW',
],
[
'WWWWWWWWWWWWWWWWWWWW',
'WP     W     W   W W',
'WWWWW  W     W W W W',
'W  W  W  WWWWWWW W W',
'W W  W M W         W',
'WW  W  W W WWWWW   W',
'W  W   W W     W WWW',
'W  WWWWW WWWWW W WFW',
'W      W       W W W',
'WWWWWW W WWWWWWW W W',
'W      W WM      W W',
'W W  WWW W       W W',
'W W      W WWWWWWW W',
'W WM     W         W',
'WWWWWWWWWWWWWWWWWWWW',
]]

def load_level(level):
    walls = []
    players = []
    monsters = []
    finishes = []

    #Parse the level string above. W = wall, F = exit, P = player, M = monster
    x = y = 0
    for row in levels[level]:
        for col in row:
            if col == 'W':
                walls.append(Wall((x, y)))
            if col == 'P':
                players.append(Player((x, y)))
            if col == 'M':
                monsters.append(Monster((x, y)))
            if col == 'F':
                finishes.append(Finish((x, y)))
            x += 32
        y += 32
        x = 0
    return walls, players, monsters, finishes

walls, players, monsters, finishes = load_level(currentLevel)
Highest_level = len(levels)-1 #index of last level

def load_first_level(): #To load level 1
    global walls, players, monsters, finishes, currentLevel
    currentLevel = 0
    walls, players, monsters, finishes = load_level(currentLevel)
    
def load_current_level(): #To reload the level you are on
    screen.fill(blue)
    global walls, players, monsters, finishes
    walls, players, monsters, finishes = load_level(currentLevel)

def quitgame():
    pygame.quit()
    quit()

def button(msg,x,y,w,h,ic,ac,action=None):
    clicked = False
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
            clicked = True
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
        
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+int(w/2)), (y+int(h/2)))
    screen.blit(textSurf, textRect)

    return clicked

def tbutton(msg,x,y,w,h,c):
    pygame.draw.rect(screen, c, (x,y,w,h))
        
    smallText = pygame.font.Font("freesansbold.ttf", 50)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+int(w/2)), (y+int(h/2)))
    screen.blit(textSurf, textRect)
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def unpause():
    global pause
    pause = False

def paused():
    largeText = pygame.font.Font('freesansbold.ttf', 100)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((width/2),(height/2)-80)
    screen.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Continue",150,350,100,50,green,bright_green,unpause)
        button("Quit",390,350,100,50,green,bright_green,quitgame)
        
        pygame.display.update()
        clock.tick(15)

def level_dis(count):
    font = pygame.font.Font("freesansbold.ttf", 20)
    text = font.render('Level: ' + str(count), True, white)
    screen.blit(text, (50,6))

def life_dis(screen,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x+37*i
        img_rect.y = y
        screen.blit(img, img_rect)
   
def win():
    screen.fill(blue)
    largeText = pygame.font.Font('freesansbold.ttf', 70)
    TextSurf, TextRect = text_objects('Congratulations!', largeText)
    TextRect.center = (int((width/2)), int((height/2)-150))
    screen.blit(TextSurf, TextRect)

    play_again = False
    while not play_again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        tbutton('You Escaped!!',270,200,100,50,blue)
        play_again = button('Play Again',150,350,110,50,green,bright_green,load_first_level)
        button('Quit',390,350,100,50,green,bright_green,quitgame)
        
        pygame.display.update()
        clock.tick(15)

def game_over():
    screen.fill(red)
    largeText = pygame.font.Font('freesansbold.ttf', 70)
    TextSurf, TextRect = text_objects('Game Over!', largeText)
    TextRect.center = (int((width/2)), int((height/2)-160))
    screen.blit(TextSurf, TextRect)

    play_again = False
    while not play_again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button('The monsters got the',220,215,200,20,red,red,None)
        button('better of you and you',220,239,200,20,red,red,None)
        button('ran out of lives.',220,263,200,20,red,red,None)
        play_again = button('Play Again',150,350,110,50,green,bright_green,load_first_level)
        button('Quit',390,350,100,50,green,bright_green,quitgame)
        pygame.display.update()
        clock.tick(15)

def game_intro():
    play = False
    while not play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(light_blue)
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects('Welcome to', largeText)
        TextRect.center = (int((width/2)), int((height/2)-150))
        screen.blit(TextSurf, TextRect)

        tbutton('Mazee!',270,130,100,50,light_blue)
        button('Escape from the mazes',270,215,100,20,light_blue,light_blue,None)
        button('without getting caught',270,239,100,20,light_blue,light_blue,None)
        button('by the monsters!',270,263,100,20,light_blue,light_blue,None)
        play = button('Play!',150,350,110,50,green,bright_green,load_first_level)
        button('Quit',390,350,100,50,green,bright_green,quitgame)
        
        pygame.display.update()
        clock.tick(15)

#Game loop
def game_loop():
    global walls, players, monsters, finishes, currentLevel, lives, pause
    level = 1 #Starting level
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        screen.fill(blue)        
        level_dis(level) #To enable level no to be displayed

        #Move the player if an arrow key is pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-2, 0, walls)
            player.image = pygame.transform.flip(playerImg, True, False)
        if key[pygame.K_RIGHT]:
            player.move(2, 0, walls)
            player.image = playerImg
        if key[pygame.K_UP]:
            player.move(0, -2, walls)
            player.image = pygame.transform.rotate(playerImg, 90)
        if key[pygame.K_DOWN]:
            player.move(0, 2, walls)
            player.image = pygame.transform.rotate(playerImg, -90)
        if key[pygame.K_p]:
            pause = True
            paused()
            
        #Move monster
        for monster in monsters:
            monster.move()

        #Moving to next level/win
        for player in players:
            for finish in finishes:
                if player.rect.colliderect(finish.rect):
                    if currentLevel < Highest_level:
                        currentLevel +=1
                        level +=1
                        walls, players, monsters, finishes = load_level(currentLevel)
                    else:
                        win()
                        level = 1
                        lives = 3
                            
        #Getting caught by the monster
        for player in players:
            for monster in monsters:
                if player.rect.colliderect(monster.rect):
                    load_current_level()
                    lives -=1
                    if lives == 0:
                        game_over()
                        level = 1
                        lives = 3

        #Draw the scene
        screen.blit(background, (0,32))
        for wall in walls:
            #pygame.draw.rect(screen, green, wall.rect)
            screen.blit(wall.image, wall.rect)
        for player in players:
            #pygame.draw.rect(screen, orange, player.rect)
            screen.blit(player.image, player.rect)
        for monster in monsters:
            #pygame.draw.rect(screen, bright_green, monster.rect)
            screen.blit(monster.image, monster.rect)
        for finish in finishes:
            #pygame.draw.rect(screen, red, finish.rect)
            screen.blit(finish.image, finish.rect)
        life_dis(screen,500,0,lives,lifeImg)
        pygame.display.update()

game_intro()
game_loop()
pygame.quit()
quit()
