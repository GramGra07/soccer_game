import random
from datetime import datetime
from time import sleep

import sys

import math
from classes.player import Player
from classes.ball import Ball
from util.Sizes import Sizes
from util.functions import *
from util.logger import log
from util.playerPositions import *
from trackers.scores import *
from trackers.trackers import *
from util.util import placeByPointAngle, toRadians


def main():
    # get time and date
    Tracker.fileName = 'logs/' + str(datetime.now().date())+' ' + str(datetime.now().time().hour)+':'+str(datetime.now().time().minute) + '.txt'
    def placePlayers(yDiv):
        position = positions[totalPlayers - 1]
        for i in range(len(position)):
            if Tracker.leftHome:
                x, y = position[i]
                y -= screenheight / yDiv
                teammates.append(Player(x, y, False))
                opponents.append(Player(screenwidth - x, y, True))
            else:
                x, y = position[i]
                teammates.append(Player(screenwidth - x, y, False))
                opponents.append(Player(x, y, True))

    def resetHalfTime():
        opponents.clear()
        teammates.clear()
        Tracker.leftHome = False
        placePlayers(8)
        ball.UpdateCoords(screenwidth / 2, screenheight / 2)
        countDown()
        ball.dx = pDx
        Tracker.time -= totalWait
        Tracker.t = Tracker.time

    def goal():
        log('\n')
        if ball.centerX < screenwidth / 2:
            if Tracker.leftHome:
                ball.UpdateCoords(10, ball.centerY)
                Scores.away += 1
                primaryDx = -pDx
                if 'Home' in pastPossession.toString():
                    log('Own goal! ' + str(Scores.home) + ' - ' + str(Scores.away))
                else:
                    log('Goal! ' + str(Scores.home) + ' - ' + str(Scores.away))
                log('Scored by ' + pastPossession.toString() + str(selectedOpponent))
            else:
                ball.UpdateCoords(10, ball.centerY)
                Scores.home += 1
                primaryDx = pDx
                if 'Away' in pastPossession.toString():
                    log('Own goal! ' + str(Scores.home) + ' - ' + str(Scores.away))
                else:
                    log('Goal! ' + str(Scores.home) + ' - ' + str(Scores.away))
                log('Scored by ' + pastPossession.toString() + str(selectedTeam))
        else:
            if Tracker.leftHome:
                ball.UpdateCoords(screenwidth - 10, ball.centerY)
                Scores.home += 1
                primaryDx = pDx
                if 'Away' in pastPossession.toString():
                    log('Own goal! ' + str(Scores.home) + ' - ' + str(Scores.away))
                else:
                    log('Goal! ' + str(Scores.home) + ' - ' + str(Scores.away))
                log('Scored by ' + pastPossession.toString() + str(selectedTeam))
            else:
                ball.UpdateCoords(screenwidth - 10, ball.centerY)
                Scores.away += 1
                primaryDx = -pDx
                if 'Home' in pastPossession.toString():
                    log('Own goal! ' + str(Scores.home) + ' - ' + str(Scores.away))
                else:
                    log('Goal! ' + str(Scores.home) + ' - ' + str(Scores.away))
                log('Scored by ' + pastPossession.toString() + str(selectedOpponent))
        log('Scored in the ' + str(Tracker.time) + ' second from ' + str(math.ceil(
            getDistance(ball.centerX, ball.centerY, pastPossession.lastX, pastPossession.lastY))) + ' pixels away\n')
        show(pygame, screen, background, ball, opponents, selectedOpponent, teammates, selectedTeam, Tracker.time)

        ball.isPossessed = False
        ball.dx = 0
        ball.dy = 0
        goalImage = pygame.image.load('images/point.png')
        goalImage = pygame.transform.scale(goalImage, (500, 500))
        screen.blit(goalImage, (screenwidth / 2 - 250, screenheight / 2 - 250))
        pygame.display.update()
        sleep(totalWait / 2)
        for opponent in opponents:
            opponent.reset()
        for teammate in teammates:
            teammate.reset()
        ball.UpdateCoords(screenwidth / 2, screenheight / 2)
        countDown()
        Tracker.time -= totalWait
        Tracker.t = Tracker.time
        ball.dx = primaryDx

    pygame.key.set_repeat(100)
    pygame.init()
    background = pygame.image.load('images/background.png')
    screenwidth, screenheight = (1000, 667)
    screen = pygame.display.set_mode((screenwidth, screenheight))
    framerate = 60
    pygame.mouse.set_visible(0)
    pygame.display.set_caption('Soccer')

    ballImage = pygame.image.load('images/ball.png')
    ballImage = pygame.transform.scale(ballImage, (Sizes.ballSize, Sizes.ballSize))
    ball = Ball(screenwidth / 2, screenheight / 2, ballImage)

    totalPlayers = Tracker.totalPlayers
    opponents = []
    teammates = []

    placePlayers(4)

    _left = 39
    _top = 25
    _width = 961
    _height = 644

    selectedTeam = 0
    selectedOpponent = 0

    pDx = 3
    primaryDx = pDx
    if random.randrange(1, 3) == 1:
        primaryDx *= -1
        if Tracker.leftHome:
            possession = teammates[selectedTeam]
            Tracker.opponentPossession = False
            log('Home starts with the ball')
        else:
            possession = opponents[selectedOpponent]
            Tracker.opponentPossession = True
            log('Away starts with the ball')
    else:
        if Tracker.leftHome:
            possession = opponents[selectedOpponent]
            Tracker.opponentPossession = True
            log('Away starts with the ball')
        else:
            possession = teammates[selectedTeam]
            Tracker.opponentPossession = False
            log('Home starts with the ball')
    ball.dx = primaryDx
    ball.dy = 0
    pastPossession = 'Kickoff'

    speed = 3
    ballSpeed = 5
    rotateSpeed = 15

    countDown()
    clock = pygame.time.Clock()
    timeLimit = Tracker.TimeLimit if Tracker.Time else 60
    totalWait = 6
    half = False
    condition = True

    log('Players a Side: ' + str(Tracker.totalPlayers))
    log('Game Started')
    if Tracker.Time:
        log('Time Limit: ' + str(Tracker.TimeLimit))
        log('Half Time: ' + str(Tracker.HalfTime))
    if Tracker.Score:
        log('Score Limit: ' + str(Tracker.ScoreLimit))
    log('\n')
    while condition:
        Tracker.t += clock.tick(framerate) / 1000
        Tracker.time = math.floor(Tracker.t)
        time = Tracker.time
        if Tracker.Time:
            condition = time < timeLimit
        if Tracker.HalfTime and Tracker.Time:
            if time == Tracker.TimeLimit / 2:
                if not half:
                    Tracker.leftHome = False
                    log('Half Time')
                    log('Score: ' + str(Scores.home) + ' - ' + str(Scores.away))
                    show(pygame, screen, background, ball, opponents, selectedOpponent, teammates, selectedTeam, time)
                    image = pygame.image.load('images/half.png')
                    image = pygame.transform.scale(image, (450, 185))
                    screen.blit(image, (screenwidth / 2 - 450 / 2, screenheight / 2 - 185 / 2))
                    pygame.display.update()
                    sleep(totalWait / 2)
                    resetHalfTime()
                    Tracker.time -= totalWait
                    time = Tracker.time
                    half = True
        if Tracker.Score:
            condition = Scores.home < Tracker.ScoreLimit and Scores.away < Tracker.ScoreLimit
        for event in pygame.event.get():
            keys = [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_u, pygame.K_o, pygame.K_w, pygame.K_s,
                    pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e, pygame.K_RETURN, pygame.K_CAPSLOCK, pygame.K_LSHIFT,
                    pygame.K_RSHIFT]
            if event.type == pygame.KEYDOWN:
                if event.key == keys[14] and ball.isPossessed or event.key == keys[15] and ball.isPossessed:
                    if Tracker.opponentPossession and event.key == keys[15]:
                        angle = opponents[selectedOpponent].angle
                        ball.dx = ballSpeed * math.cos(toRadians(angle))
                        ball.dy = ballSpeed * math.sin(toRadians(angle))
                        ball.UpdateCoords(ball.lastX + ball.dx * 10, ball.lastY + ball.dy * 10)
                        pastPossession = opponents[selectedOpponent]
                        log(pastPossession.toString() + str(selectedOpponent) + ' has passed the ball')
                    elif not Tracker.opponentPossession and event.key == keys[14]:
                        angle = teammates[selectedTeam].angle
                        ball.dx = ballSpeed * math.cos(toRadians(angle))
                        ball.dy = ballSpeed * math.sin(toRadians(angle))
                        ball.UpdateCoords(ball.lastX + ball.dx * 10, ball.lastY + ball.dy * 10)
                        pastPossession = teammates[selectedTeam]
                        log(pastPossession.toString() + str(selectedTeam) + ' has passed the ball')
                if event.key == keys[0]:
                    opponents[selectedOpponent].dy = -speed
                if event.key == keys[1]:
                    opponents[selectedOpponent].dy = speed
                if event.key == keys[2]:
                    opponents[selectedOpponent].dx = -speed
                if event.key == keys[3]:
                    opponents[selectedOpponent].dx = speed
                if event.key == keys[4]:
                    opponents[selectedOpponent].angle -= rotateSpeed
                if event.key == keys[5]:
                    opponents[selectedOpponent].angle += rotateSpeed
                if event.key == keys[12]:
                    if not Tracker.opponentPossession:
                        selectedOpponent = random.randint(0, totalPlayers - 1)

                if event.key == keys[6]:
                    teammates[selectedTeam].dy = -speed
                if event.key == keys[7]:
                    teammates[selectedTeam].dy = speed
                if event.key == keys[8]:
                    teammates[selectedTeam].dx = -speed
                if event.key == keys[9]:
                    teammates[selectedTeam].dx = speed
                if event.key == keys[10]:
                    teammates[selectedTeam].angle -= rotateSpeed
                if event.key == keys[11]:
                    teammates[selectedTeam].angle += rotateSpeed
                if event.key == keys[13]:
                    if Tracker.opponentPossession:
                        selectedTeam = random.randint(0, totalPlayers - 1)

            if event.type == pygame.KEYUP:
                if event.key == keys[0]:
                    opponents[selectedOpponent].dy = 0
                if event.key == keys[1]:
                    opponents[selectedOpponent].dy = 0
                if event.key == keys[2]:
                    opponents[selectedOpponent].dx = 0
                if event.key == keys[3]:
                    opponents[selectedOpponent].dx = 0
                if event.key == keys[6]:
                    teammates[selectedTeam].dy = 0
                if event.key == keys[7]:
                    teammates[selectedTeam].dy = 0
                if event.key == keys[8]:
                    teammates[selectedTeam].dx = 0
                if event.key == keys[9]:
                    teammates[selectedTeam].dx = 0

            if event.type == pygame.QUIT:
                sys.exit()
        for i in range(totalPlayers):
            if ball.collided(ball, opponents[i]) or ball.collided(ball, teammates[i]):
                if ball.collided(ball, teammates[i]):
                    if pastPossession == 'Kickoff':
                        log('Kickoff! ' + teammates[i].toString() + str(i) + ' has the ball')
                        pastPossession = teammates[i]
                        break
                    if 'Away' in pastPossession.toString():
                        pastPossession = teammates[i]
                        log('Turnover! ' + pastPossession.toString() + str(selectedTeam) + ' has the ball')
                    if teammates[i] != pastPossession:
                        log(teammates[i].toString() + str(
                            i) + ' receives the ball from ' + pastPossession.toString() + str(selectedTeam))
                        pastPossession = teammates[i]
                    selectedTeam = i
                    possession = teammates[i]
                    Tracker.opponentPossession = False
                    ball.isPossessed = True
                if ball.collided(ball, opponents[i]):
                    if pastPossession == 'Kickoff':
                        log('Kickoff! ' + opponents[i].toString() + str(i) + ' has the ball')
                        pastPossession = opponents[i]
                        break
                    if 'Home' in pastPossession.toString():
                        pastPossession = opponents[i]
                        log('Turnover! ' + pastPossession.toString() + str(selectedOpponent) + ' has the ball')
                    if opponents[i] != pastPossession:
                        log(opponents[i].toString() + str(
                            i) + ' receives the ball from ' + pastPossession.toString() + str(selectedOpponent))
                        pastPossession = opponents[i]
                    selectedOpponent = i
                    possession = opponents[i]
                    Tracker.opponentPossession = True
                    ball.isPossessed = True
                break
            else:
                ball.isPossessed = False
        angle = possession.angle
        angle = toRadians(angle)
        if ball.isPossessed:
            placeByPointAngle(ball, possession, angle)
        ball.UpdateCoords(ball.lastX + ball.dx, ball.lastY + ball.dy)
        ttag = False
        if teammates[selectedTeam].top < _top:
            teammates[selectedTeam].UpdateCoords(teammates[selectedTeam].lastX + teammates[selectedTeam].dx,
                                                 _top + teammates[selectedTeam].radius)
            ttag = True
        if teammates[selectedTeam].left < _left:
            teammates[selectedTeam].UpdateCoords(_left + teammates[selectedTeam].radius,
                                                 teammates[selectedTeam].lastY + teammates[selectedTeam].dy)
            ttag = True
        if teammates[selectedTeam].bottom > _height:
            teammates[selectedTeam].UpdateCoords(teammates[selectedTeam].lastX + teammates[selectedTeam].dx,
                                                 _height - teammates[selectedTeam].radius)
            ttag = True
        if teammates[selectedTeam].right > _width:
            teammates[selectedTeam].UpdateCoords(_width - teammates[selectedTeam].radius,
                                                 teammates[selectedTeam].lastY + teammates[selectedTeam].dy)
            ttag = True
        if not ttag:
            teammates[selectedTeam].UpdateCoords(teammates[selectedTeam].lastX + teammates[selectedTeam].dx,
                                                 teammates[selectedTeam].lastY + teammates[selectedTeam].dy)
        optag = False
        if opponents[selectedOpponent].top < _top:
            opponents[selectedOpponent].UpdateCoords(opponents[selectedOpponent].lastX + opponents[selectedOpponent].dx,
                                                     _top + opponents[selectedOpponent].radius)
            optag = True
        if opponents[selectedOpponent].left < _left:
            opponents[selectedOpponent].UpdateCoords(_left + opponents[selectedOpponent].radius,
                                                     opponents[selectedOpponent].lastY + opponents[selectedOpponent].dy)
            optag = True
        if opponents[selectedOpponent].bottom > _height:
            opponents[selectedOpponent].UpdateCoords(opponents[selectedOpponent].lastX + opponents[selectedOpponent].dx,
                                                     _height - opponents[selectedOpponent].radius)
            optag = True
        if opponents[selectedOpponent].right > _width:
            opponents[selectedOpponent].UpdateCoords(_width - opponents[selectedOpponent].radius,
                                                     opponents[selectedOpponent].lastY + opponents[selectedOpponent].dy)
            optag = True
        if not optag:
            opponents[selectedOpponent].UpdateCoords(opponents[selectedOpponent].lastX + opponents[selectedOpponent].dx,
                                                     opponents[selectedOpponent].lastY + opponents[selectedOpponent].dy)
        if (ball.top < _top) or (ball.top - ball.radius * 2 > _height - _top * 3) or (ball.left < _left) or (
                ball.left + ball.radius * 2 > _width):
            # check if ball is a goal
            _goalTop = 432
            _goalLeft = 39 + ball.radius + 2
            _goalRight = 960 - ball.radius - 2
            _goalBottom = 290
            # check if ball is in goal
            if _goalTop > ball.centerY > _goalBottom:
                goal()
                pastPossession = 'Kickoff'
                Tracker.time -= totalWait
                continue
            if (ball.left < _left) or (ball.left + ball.radius * 2 > _width - _left):
                ball.dx *= -1
            if (ball.top < _top) or (ball.top - ball.radius * 2 > _height - _top * 3):
                ball.dy *= -1
        show(pygame, screen, background, ball, opponents, selectedOpponent, teammates, selectedTeam, time)
        Tracker.time = time

    else:
        log('Game Over!')
        log('Final Score: ' + str(Scores.home) + ' - ' + str(Scores.away))
        log('Winner: ' + getWinner(Scores.home, Scores.away))

        show(pygame, screen, background, ball, opponents, selectedOpponent, teammates, selectedTeam, Tracker.time)
        end = pygame.image.load('images/end.png')
        end = pygame.transform.scale(end, (300, 300))
        screen.blit(end, (screenwidth / 2 - 150, screenheight / 2 - 150))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.K_r:
                    main()
