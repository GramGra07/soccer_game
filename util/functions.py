import pygame

from Python.pyGame.soccer.trackers.scores import Scores
from Python.pyGame.soccer.trackers.trackers import Tracker
from Python.pyGame.soccer.util.util import getDistance

screenwidth = 1000
screenheight = 667
screen = pygame.display.set_mode((screenwidth, screenheight))
def countDown():
    timer = pygame.time.Clock()
    t = 0
    while t < 3:
        t += timer.tick() / 1000
        if t < 1:
            image = pygame.image.load('images/3.png')
        elif t < 2:
            image = pygame.image.load('images/2.png')
        else:
            image = pygame.image.load('images/1.png')
        image = pygame.transform.scale(image, (100, 100))
        bg = pygame.image.load('images/background.png')
        screen.blit(bg, (0, 0))
        goalImage = pygame.image.load('images/goal.png')
        goalImage = pygame.transform.scale(goalImage, (120, 118))
        goalImage = pygame.transform.rotate(goalImage, 180)
        screen.blit(goalImage, (-50, screenheight / 2 - 55))
        goalImage = pygame.transform.rotate(goalImage, 180)
        screen.blit(goalImage, (screenwidth - 75, screenheight / 2 - 55))
        showScores()
        screen.blit(image, (screenwidth / 2 - 50, screenheight / 2 - 50))
        pygame.draw.rect(screen, (105, 105, 105), (screenwidth / 2 - 20, 0, 40, 30))
        pygame.display.update()

def show(pygame,screen,background,ball,opponents,selectedOp, team,selectedTeam,time):
    screen.blit(background, (0, 0))
    ball.show(screen)
    for opponent in opponents:
        opponent.show(screen)
    for player in team:
        player.show(screen)
    pygame.draw.circle(screen, (255,215,0), (opponents[selectedOp].centerX,opponents[selectedOp].centerY), 10)
    pygame.draw.circle(screen, (0, 215, 255), (team[selectedTeam].centerX, team[selectedTeam].centerY), 10)
    goalImage = pygame.image.load('images/goal.png')
    goalImage = pygame.transform.scale(goalImage, (120, 118))
    goalImage = pygame.transform.rotate(goalImage, 180)
    screen.blit(goalImage, (-50, screenheight / 2 - 55))
    goalImage = pygame.transform.rotate(goalImage, 180)
    screen.blit(goalImage, (screenwidth - 75, screenheight / 2 - 55))
    showScores()
    showTime(time)
    pygame.display.update()
def showScores():
    pygame.draw.rect(screen, (0, 0, 255), (screenwidth / 2 - 60, 0, 40, 30))
    pygame.draw.rect(screen, (255, 0, 0), (screenwidth / 2 + 20, 0, 40, 30))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(Scores.home), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (screenwidth / 2 - 50, 16)
    screen.blit(text, textRect)
    text = font.render(str(Scores.away), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (screenwidth / 2 + 50, 16)
    screen.blit(text, textRect)
def showTime(time):
    pygame.draw.rect(screen, (105,105,105), (screenwidth / 2 - 20, 0, 40, 30))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(time), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (screenwidth / 2, 16)
    screen.blit(text, textRect)
def collision(object1, object2):
    range = Tracker.range
    return getDistance(object1.left, object1.top, object2.left, object2.top) < object1.radius + object2.radius + range

def getWinner(home, away):
    return 'Home' if home > away else 'Away' if away > home else 'Draw'