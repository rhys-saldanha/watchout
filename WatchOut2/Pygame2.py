import pygame, sys, time, random, operator, math  # ,	pygame._view
from    pygame.locals import *
from    operator import itemgetter

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()

# DISPLAYSURF	=	pygame.display.set_mode((0,0),	FULLSCREEN|RESIZABLE,	0)
DISPLAYSURF = pygame.display.set_mode((800, 600), 0)

screenx, screeny = DISPLAYSURF.get_size()
centrex = int(screenx / 2)
centrey = int(screeny / 2)
pygame.display.set_caption('Watch	Out	2!	-The	Game')

speeds = []
for i in range(360):
    speeds += '0'
    speeds[i] = int(speeds[i])


class Ship():
    def __init__(self, placex=centrex, placey=centrey, angle=0, speeds=speeds):
        self.place = {'x': placex, 'y': placey}
        self.corner = {'x': 0, 'y': 0}
        self.angle = angle
        self.speed = 10
        self.speeds = speeds
        self.turningcircle = 10
        self.margin = 100
        self.image = pygame.image.load('shipPic.png')
        self.rotimage = pygame.transform.rotate(self.image, -(90))

    def Accel(self):
        angle = self.angle
        if self.speed <= 10:
            self.speed += 1
        self.speeds[angle] = self.speed

    def Decel(self, angle):
        self.speeds[angle] -= 1
        if self.speeds[angle] < 0:
            self.speeds[angle] = 0

    def Corner(self):
        shipRect = self.rotimage.get_rect()
        self.corner['x'] = self.place['x'] - (shipRect.height / 2)
        self.corner['y'] = self.place['y'] - (shipRect.width / 2)

    def KeepOnScreen(self):
        if self.place['x'] < (0 + self.margin):
            self.place['x'] = (0 + self.margin)
        if self.place['x'] > (screenx - self.margin):
            self.place['x'] = (screenx - self.margin)
        if self.place['y'] < (0 + self.margin):
            self.place['y'] = (0 + self.margin)
        if self.place['y'] > (screeny - self.margin):
            self.place['y'] = (screeny - self.margin)

    def moveFunc(self, angle):
        radangle = math.radians(angle)
        self.place['x'] += self.speeds[angle] * math.cos(radangle)
        self.place['y'] += self.speeds[angle] * math.sin(radangle)


def quit():
    pygame.quit()
    sys.exit()


class Game():
    def __init__(self):
        self.left = False
        self.right = False
        self.forwards = False
        self.thing = 0
        self.colours = {'BLACK': (000, 000, 000,)}
        self.ship = Ship()
        self.counter = 0

    def main(self):
        DISPLAYSURF.fill(self.colours['BLACK'])
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESC:
                    quit()
                if event.key == K_a:
                    self.left = True
                if event.key == K_d:
                    self.right = True
                if event.key == K_w:
                    self.forwards = True
            if event.type == KEYUP:
                if event.key == K_a:
                    self.left = False
                if event.key == K_d:
                    self.right = False
                if event.key == K_w:
                    self.forwards = False

        if self.left and not self.right:
            self.ship.angle -= self.ship.turningcircle
            self.ship.speed = 5
        elif self.right and not self.left:
            self.ship.angle += self.ship.turningcircle
            self.ship.speed = 5
        else:
            self.ship.speed = 15

        self.ship.angle = self.ship.angle % 360
        self.ship.rotimage = pygame.transform.rotate(self.ship.image, -(self.ship.angle + 90))

        if self.forwards:
            self.ship.Accel()

        for i in range(360):
            if not self.forwards:
                self.ship.Decel(i)
            elif i != self.ship.angle:
                self.ship.Decel(i)
            self.ship.moveFunc(i)
        self.ship.KeepOnScreen()
        self.ship.Corner()

        DISPLAYSURF.blit(self.ship.rotimage, (self.ship.corner['x'], self.ship.corner['y']))

        if self.counter > 10:
            self.counter = 0
            print    fpsClock.get_fps()

        pygame.display.update()
        fpsClock.tick(FPS)


# main	game	loop
game = Game()
while True:
    game.main()
