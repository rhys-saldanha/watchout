import pygame, sys, time, random, operator, math#, pygame._view
from pygame.locals import *
from operator import itemgetter

pygame.init()

FPS = 100
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((0,0), FULLSCREEN|RESIZABLE, 0)
screenx, screeny = DISPLAYSURF.get_size()
centrex = int(screenx/2)
centrey = int(screeny/2)
pygame.display.set_caption('Watch Out! -The Game')

#ICON = pygame.image.load('image\\

BLACK    = (  0,   0,   0)
WHITE    = (225, 225, 225)
RED      = (225,   0,   0)
GREEN    = (  0, 225,   0)
YELLOW   = (225, 225,   0)
BLUE     = (  0,   0, 225)
BACKBLUE = (  3,   4,  35)
MAROON   = (128,   0,   0)

pygame.mixer.music.load('\\files\\WatchOut.mp3')
musicPlaying = False

def aspect_scale(img,bx,by):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by
    sx = int(sx)
    sy = int(sy)
    return pygame.transform.scale(img, (sx,sy))

ROCK = pygame.image.load('\\images\\rock.png')
ROCK = pygame.transform.scale(ROCK, (60, 60))
ROCK_rect = ROCK.get_rect()

GOLDENROCK = pygame.image.load('\\images\\goldrock.png')
GOLDENROCK_rect = GOLDENROCK.get_rect()

STAR = pygame.image.load('\\images\\star.png')

STAR_BIG = pygame.transform.scale(STAR, (50,50))

STAR_MED = pygame.transform.scale(STAR, (30,30))

STAR_SMALL = pygame.transform.scale(STAR, (20,20))

#BACKGROUND = pygame.image.load('images\\background.jpg')
#BACKGROUND = pygame.transform.scale(BACKGROUND, (screenx,screeny))

PLAYER = pygame.image.load('\\images\\player.png')
PLAYER = pygame.transform.scale(PLAYER, (50, 50))
playerx = centrex
playery = centrey
PLAYER_rect = pygame.Rect((0,0),(50,50))

LOGO = pygame.image.load('\\images\\WatchOut.png')

STARTBUTTON = pygame.image.load('\\images\\start.png')
STARTBUTTON_rect = pygame.Rect((0,0),(200,50))

PAUSELOGO = aspect_scale(LOGO, 550, 550)

PAUSEBACKG = pygame.image.load('\\images\\pausebackg.png')
PAUSEBACKG = pygame.transform.scale(PAUSEBACKG, (600, 500))
PAUSEBACKG_rect = PAUSEBACKG.get_rect()

PAUSEQUIT = pygame.image.load('\\\images\\quit.png')
PAUSEQUIT_rect = PAUSEQUIT.get_rect()

PAUSERESUME = pygame.image.load('\\images\\resume.png')
PAUSERESUME_rect = PAUSERESUME.get_rect()

HIGHSCORES = pygame.image.load('\\images\\highscores.png')
HIGHSCORES_rect = HIGHSCORES.get_rect()

BACK = pygame.image.load('\\images\\back.png')
BACK_rect = BACK.get_rect()

move = 7

class Timer:
        def __init__(self):
                self.t = 0
                
        def Add(self, addition):
                self.t += addition

        def Reset(self):
                self.t = 0

        def Stop(self, stop):
                self.stop = stop

        def GetPast(self):
                return self.t

scoreTimer = Timer()
myfont = pygame.font.SysFont("monospace", 30)
myfontbig = pygame.font.SysFont("monospace", 35, bold=True)

def playermove(playerx, playery, movey, movex):
        global move
        if movex and movey:
                multiplier = ((math.sqrt(2))**(-1))
        else:
                multiplier = 1

        if movey == 'UP':
                playery -= (move * multiplier)
        if movey == 'DOWN':
                playery += (move * multiplier)
        if movex == 'LEFT':
                playerx -= (move * multiplier)
        if movex == 'RIGHT':
                playerx += (move * multiplier)
                        
        return playerx, playery

def main():
        global DISPLAYSURF, playershift, mousetoggle, movex, movey, move, playerx, playery
        global collision, framecounter, FPS, stars, STAR_SMALL, STAR_MED, STAR_BIG
        global STAR_SMALL_rect, STAR_MED_rect, STAR_BIG_rect, screenx, screeny, margin
        global screenon, rocks, myfont, musicPlaying, GOLDENROCK, GOLDENROCK_rect
        global scoreMultiplier

        scoreTimer.Add(10 * scoreMultiplier)
        
        move = 7
        pygame.mouse.set_visible(False)
        
        DISPLAYSURF.fill(BACKBLUE)
        
        for event in pygame.event.get():
                if event.type == QUIT:
                        end()
                if event.type == KEYUP:
                        if event.key == K_LSHIFT or event.key == K_RSHIFT:
                                playershift = False
                        if event.key == K_w or event.key == K_UP and movey == 'UP':
                                movey = False
                        if event.key == K_s or event.key == K_DOWN and movey == 'DOWN':
                                movey = False
                        if event.key == K_a or event.key == K_LEFT and movex == 'LEFT':
                                movex = False
                        if event.key == K_d or event.key == K_RIGHT and movex == 'RIGHT':
                                movex = False
                if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                                collision = True
                        if event.key == K_LSHIFT or event.key == K_RSHIFT:
                                playershift = True
                        if event.key == K_w or event.key == K_UP:
                                movey = 'UP'
                        if event.key == K_s or event.key == K_DOWN:
                                movey = 'DOWN'
                        if event.key == K_a or event.key == K_LEFT:
                                movex = 'LEFT'
                        if event.key == K_d or event.key == K_RIGHT:
                                movex = 'RIGHT'
                        if event.key == K_y:
                                scoreTimer.Add(1000)
                        if event.key == K_m:
                                if musicPlaying:
                                    pygame.mixer.music.stop()
                                else:
                                    pygame.mixer.music.play(-1, 0.0)
                                musicPlaying = not musicPlaying
                        if event.key == K_p or event.key == K_SPACE:
                                pause()

        if playershift:
                move += 5
                
        #typeofstar - 0 = BIG; 1 = MED; 2 = SMALL
        for star in stars:
                typeofstar = random.randint(0, 2)
                starx = (random.randint(-5, (screenx / 60) + 5))*60
                stary = (random.randint(-5, (screenx / 60) + 5))*60

                star = [starx, stary, typeofstar]
                if len(stars) < int((screeny/30)):
                        stars.append(star)

        stars = sorted(stars, key=itemgetter(2), reverse=True)
                                           
        for star in stars:
                if star[1] < -100:
                        star[1] = screeny + 100
                        star[0] = (random.randint(-5, (screenx / 60) + 5))*60
                if star[1] > screeny + 100:
                        star[1] = -100
                        star[0] = (random.randint(-5, (screenx / 60) + 5))*60
                if star[0] < -100:
                        star[0] = screenx + 100
                        star[1] = (random.randint(-5, (screeny / 60) + 5))*60
                if star[0] > screenx + 100:
                        star[0] = -100
                        star[1] = (random.randint(-5, (screeny / 60) + 5))*60

        for star in stars:
                if star[2] == 2:
                        image = STAR_SMALL
                if star[2] == 1:
                        image = STAR_MED
                if star[2] == 0:
                        image = STAR_BIG
                        
                DISPLAYSURF.blit(image, (star[0], star[1]))
        
        #For typeofrock - (0 = UP),(1 = DOWN),(2 = LEFT),(3 = RIGHT) 
        if framecounter == 180 or framecounter == 0:
                framecounter = 0
                typeofrock = random.randint(0, 3)
                if typeofrock == 0:
                        tempx = random.randint(0, screenx)
                        tempy = screeny + 100
                elif typeofrock == 1:
                        tempx = random.randint(0, screenx)
                        tempy = -100
                elif typeofrock == 2:
                        tempx = screenx + 100
                        tempy = random.randint(0, screeny)
                elif typeofrock == 3:
                        tempx = -100
                        tempy = random.randint(0, screeny)

                speed = (len(rocks) % 10)*2
                if speed == 0:
                        speed = 2
                if speed > 10:
                        speed = 10

                rock = [tempx, tempy, typeofrock, speed]

                if len(rocks) < 8:
                        rocks.append(rock)

        if len(rocks) > 0:
                for rock in rocks:
                        ROCK_rect.topleft = (rock[0],rock[1])
                        PLAYER_rect.topleft = (playerx,playery)
                        if PLAYER_rect.colliderect(ROCK_rect):
                                collision = True

        for rock in golden:
                chance = random.randint(1, 100000000)
                if chance == 69:
                        rockx = 200
                        rocky = 500
                        rock = [rockx, rocky]
                        if len(golden) < 1:
                                golden.append(rock)

        if len(golden) > 0:
                for gold in golden:
                        GOLDENROCK_rect.topleft = (gold[0],gold[1])
                        PLAYER_rect.topleft = (playerx, playery)
                        if PLAYER_rect.colliderect(GOLDENROCK_rect):
                                scoreMultiplier += 1
                                typeofgold = 0
                                if typeofgold == 0:
                                        gold[0] = random.randint(-100, (screenx + 100))
                                        gold[1] = random.randint(-1000, -100)
                                if typeofgold == 1:
                                        rock[0] = random.randint(-100, screenx + 100)
                                        rock[1] = random.randint(screeny + 100, screeny + 1000)
                                if typeofgold == 2:
                                        rock[0] = random.randint(-1000, -100)
                                        rock[1] = random.randint(-100, screeny + 100)
                                if typeofgold == 3:
                                        rock[0] = random.randint(screenx + 100, screenx + 1000)
                                        rock[1] = random.randint(-100, screeny + 100)
        
        for rock in rocks:
                if rock[2] == 0:
                        rock[1] -= rock[3]
                elif rock[2] == 1:
                        rock[1] += rock[3]
                elif rock[2] == 2:
                        rock[0] -= rock[3]
                elif rock[2] == 3:
                        rock[0] += rock[3]
        
        #playerx, playery = playermove(playerx, playery, movey, movex, playershift)


        if movey == 'UP':
                if playery >= ((screeny / 2)- margin):
                        playerx, playery = playermove(playerx, playery, movey, movex)
                if playery <= ((screeny / 2)- margin):
                        playery = ((screeny / 2)- margin)
                        for rock in golden:
                                rock[1] += move - 2
                        for rock in rocks:
                                rock[1] += move - 2
                        for star in stars:
                                if star[2] == 0:
                                        star[1] += move - 3
                                if star[2] == 1:
                                        star[1] += move - 5
                                if star[2] == 2:
                                        star[1] += move - 6
        if movey == 'DOWN':
                if playery <= ((screeny / 2)+ margin):
                        playerx, playery = playermove(playerx, playery, movey, movex)
                if playery >= ((screeny / 2)+ margin):
                        playery = ((screeny / 2)+ margin)
                        for rock in golden:
                                rock[1] -= move - 2
                        for rock in rocks:
                                rock[1] -= move - 2
                        for star in stars:
                                if star[2] == 0:
                                        star[1] -= move - 3
                                if star[2] == 1:
                                        star[1] -= move - 5
                                if star[2] == 2:
                                        star[1] -= move - 6
        if movex == 'LEFT':
                if playerx >= ((screenx / 2)- margin):
                        playerx, playery = playermove(playerx, playery, movey, movex)
                if playerx <= ((screenx / 2)- margin):
                        playerx = ((screenx / 2)- margin)
                        for rock in golden:
                                rock[0] += move - 2
                        for rock in rocks:
                                rock[0] += move - 2
                        for star in stars:
                                if star[2] == 0:
                                        star[0] += move - 3
                                if star[2] == 1:
                                        star[0] += move - 5
                                if star[2] == 2:
                                        star[0] += move - 6
        if movex == 'RIGHT':
                if playerx <= ((screenx / 2)+ margin):
                        playerx, playery = playermove(playerx, playery, movey, movex)
                if playerx >= ((screenx / 2)+ margin):
                        playerx = ((screenx / 2)+ margin)
                        for rock in golden:
                                rock[0] -= move - 2
                        for rock in rocks:
                           rock[0] -= move - 2
                        for star in stars:
                                if star[2] == 0:
                                        star[0] -= move - 3
                                if star[2] == 1:
                                        star[0] -= move - 5
                                if star[2] == 2:
                                        star[0] -= move - 6

        for rock in rocks:
                if rock[1] < -100:
                        rock[1] = screeny + 100
                        rock[0] = random.randrange(0, screenx)
                if rock[1] > screeny + 100:
                        rock[1] = -100
                        rock[0] = random.randrange(0, screenx)
                if rock[0] < -100:
                        rock[0] = screenx + 100
                        rock[1] = random.randrange(0, screeny)
                if rock[0] > screenx + 100:
                        rock[0] = -100
                        rock[1] = random.randrange(0, screeny)
                DISPLAYSURF.blit(ROCK, (rock[0], rock[1]))

        for rock in golden:
                if rock[1] < -2000:
                        rock[1] = screeny + 100
                        rock[0] = random.randrange(0, screenx)
                if rock[1] > screeny + 2000:
                        rock[1] = -100
                        rock[0] = random.randrange(0, screenx)
                if rock[0] < -2000:
                        rock[0] = screenx + 100
                        rock[1] = random.randrange(0, screeny)
                if rock[0] > screenx + 2000:
                        rock[0] = -100
                        rock[1] = random.randrange(0, screeny)
                DISPLAYSURF.blit(GOLDENROCK, (rock[0], rock[1]))

        framecounter += 1

        

        score = myfont.render('Score: ' + (str(scoreTimer.GetPast())), 1, GREEN)
        DISPLAYSURF.blit(score, (0, 0))
        multiplier = myfont.render('Multiplier: ' + str(scoreMultiplier), 1, GREEN)
        DISPLAYSURF.blit(multiplier, (screenx - 300, 0))

        DISPLAYSURF.blit(PLAYER, (playerx, playery))

def start():
        global screenx, screeny, STARTBUTTON, STARTBUTTON_rect, screenon, LOGO
        global finalScore, musicPlaying, centrex, centrey, HIGHSCORES, HIGHSCORES_rect
        global centrex, centrey, SPLASH

        DISPLAYSURF.fill(BACKBLUE)

        startx = (centrex-100)
        starty = (centrey+75)
        STARTBUTTON_rect.topleft = (startx, starty)
        HIGHSCORES_rect.topleft = (centrex-100, centrey+125)

        pygame.mouse.set_visible(True)

        for event in pygame.event.get():
                if event.type == QUIT:
                        end()
                if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                                end()
                        if event.key == K_RETURN:
                                screenon = 'main'
                                scoreTimer.Reset()
                        if event.key == K_h:
                                screenon = 'highscores'
                        if event.key == K_m:
                                if musicPlaying:
                                    pygame.mixer.music.stop()
                                else:
                                    pygame.mixer.music.play(-1, 0.0)
                                musicPlaying = not musicPlaying
                
                if event.type == MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if STARTBUTTON_rect.collidepoint(pos):
                                screenon = 'main'
                                scoreTimer.Reset()
                        if HIGHSCORES_rect.collidepoint(pos):
                                screenon = 'highscores'
        
        score = myfont.render('Score: ' + str(finalScore), 1, GREEN)

        DISPLAYSURF.blit(SPLASH, (0, screeny - 100))
        DISPLAYSURF.blit(score, (0, 0))
        DISPLAYSURF.blit(STARTBUTTON, (startx, starty))
        DISPLAYSURF.blit(HIGHSCORES, (centrex-100, centrey+125))
        DISPLAYSURF.blit(LOGO, (centrex - 500, centrey - 200))

def highscores():
        global screenx, screeny, highScores, screenon, myfont, displayHighScores
        global displayHighScoresLine, musicPlaying, centrex, centrey, BACK, BACK_rect

        DISPLAYSURF.fill(BACKBLUE)

        loadScores()

        pygame.mouse.set_visible(True)

        for event in pygame.event.get():
                if event.type == QUIT:
                        end()
                if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                                screenon = 'start'
                        if event.key == K_m:
                                if musicPlaying:
                                    pygame.mixer.music.stop()
                                else:
                                    pygame.mixer.music.play(-1, 0.0)
                                musicPlaying = not musicPlaying
                if event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if BACK_rect.collidepoint(pos):
                        screenon = 'start'

        if len(highScores) < 10:
                for i in range(0, len(highScores)):
                        score = myfont.render(str(highScores[i]), 1, GREEN)
                        DISPLAYSURF.blit(score, (centrex - 40, 200 + (30 * i)))
        else:
                for i in range(0, 9):
                        score = myfont.render(str(highScores[i]), 1, GREEN)
                        DISPLAYSURF.blit(score, (centrex - 40, 200 + (30 * i)))

        DISPLAYSURF.blit(BACK, (centrex-100, centrey+125))
        BACK_rect.topleft = (centrex-100, centrey+125)
        
def end():
        pygame.quit()
        sys.exit()

def saveScore(score):
        f = open('files\\SCORES.txt', 'r+')
        f.readlines()
        score = str(score)
        f.write(score + ' ')
        f.close()

def loadScores():
        global highScores
        highScores = []
        f = open('files\\SCORES.txt', 'r+')
        highScoreslist = f.readlines()
        highScoreslist = highScoreslist[0]
        highScoreslist = highScoreslist.split()
        for i in highScoreslist:
                i = int(i)
                highScores.append(i)
        highScores = sorted(highScores, reverse=True)
        f.close()

def loadSplashes():
        f = open('files\\SPLASHES.txt', 'r')
        while True:
                splash = str(f.readline())
                if not splash:
                    break
                splashes.append(splash[:(len(splash)-1)])
                

def pause():
        global screenx, screeny, screenon, LOGO, PAUSEBACKG, centrex, centrey
        global PAUSEBACKG_rect, collision, PAUSEBACK, PAUSEBACK_rect
        global PAUSEQUIT, PAUSEQUIT_rect, PAUSERESUME, PAUSERESUME_rect
        global HIGHSCORES, HIGHSCORES_rect, PAUSELOGO, highScores
        loadScores()
        highscoredisplay = False
        pause = True
        while pause:
                DISPLAYSURF.blit(PAUSEBACKG, (centrex - 300, 100))
                PAUSEBACKG_rect.topleft = (centrex - 300, 100)
                
                pygame.mouse.set_visible(True)
                for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP:
                                pos = pygame.mouse.get_pos()
                                if PAUSEQUIT_rect.collidepoint(pos):
                                        end()
                                if HIGHSCORES_rect.collidepoint(pos):
                                        highscoredisplay = not highscoredisplay
                                if PAUSERESUME_rect.collidepoint(pos):
                                        pause = False
                        if event.type == QUIT:
                                end()
                        if event.type == KEYDOWN:
                                if event.key == K_ESCAPE:
                                        collision = True
                                        pause = False
                                if event.key == K_p:
                                           pause = False

                if not highscoredisplay:
                        DISPLAYSURF.blit(PAUSELOGO, (centrex - 280, 150))
                if highscoredisplay:
                        if len(highScores) < 4:
                                for i in range(0, len(highScores)):
                                        score = myfontbig.render(str(highScores[i]), 1, GREEN)
                                        DISPLAYSURF.blit(score, (centrex - 50, 200 + (30 * i)))
                        else:
                                for i in range(0, 3):
                                        score = myfontbig.render(str(highScores[i]), 1, GREEN)
                                        DISPLAYSURF.blit(score, (centrex - 50, 200 + (30 * i)))

                DISPLAYSURF.blit(PAUSEQUIT, (centrex - 100, 450))
                PAUSEQUIT_rect.topleft = (centrex - 100, 450)
                DISPLAYSURF.blit(PAUSERESUME, (centrex - 100, 350))
                PAUSERESUME_rect.topleft = (centrex - 100, 350)
                DISPLAYSURF.blit(HIGHSCORES, (centrex - 100, 400))
                HIGHSCORES_rect.topleft = (centrex - 100, 400)

                pygame.display.update()#PAUSEBACKG_rect)
                fpsClock.tick(FPS)

margin = 0
playershift = False
mousetoggle = False
movey = 'NONE'
movex = 'NONE'
framecounter = 0
rocks = []
golden = [[200,500]]
stars = []
typeofstar = random.randint(0, 2)
starx = random.randint(0, screenx)
stary = random.randint(0, screeny)
star = [starx, stary, typeofstar]
stars.append(star)

finalScore = "You haven't played yet!"
scoreMultiplier = 2
highScores = []
displayHighScores = []
displayHighScoresLine = 10

collision = False
screenon = 'start'

splashes = []
loadSplashes()
splash = splashes[random.randint(0, (len(splashes) - 1))]

while True:
        if (not pygame.display.get_active() or not pygame.key.get_focused()) and  screenon == 'main':
                pause()
        if screenon == 'start':
                oldsplash = splash
                while oldsplash == splash:
                    splash = splashes[random.randint(0, (len(splashes) - 1))]
                SPLASH = myfont.render(splash, 1, GREEN)
                screenon = 'startscreen'
        if screenon == 'startscreen':
                start()
        elif screenon == 'highscores':
                highscores()
        elif collision:
                finalScore = scoreTimer.GetPast()
                saveScore(finalScore)
                loadScores()
                framecounter = 0
                scoreMultiplier = 2
                rocks = []
                movex = False
                movey = False
                playershift = False
                DISPLAYSURF.fill(BACKBLUE)
                collision = False
                screenon = 'start'
        else:
                main()

        pygame.display.update()
        fpsClock.tick(FPS)
