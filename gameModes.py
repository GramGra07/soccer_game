from time import sleep

import pygame

from Python.pyGame.soccer.main import main
from Python.pyGame.soccer.trackers.trackers import Tracker


class Button:
    def __init__(self, rect, text, action):
        self.rect = rect
        self.text = text
        self.action = action


def buildGameModes():
    Tracker.l_text = ""

    def updateLabel():
        return font.render(str(Tracker.l_text), True, font_color)

    def increaseScore():
        Tracker.ScoreLimit += 1
        updateScore()

    def decreaseScore():
        if Tracker.ScoreLimit > 1:
            Tracker.ScoreLimit -= 1
        updateScore()
    def scorePressed():
        Tracker.Score = True
        Tracker.l_text = 1
        updateButtonText(b3, "Increase Score", increaseScore)
        updateButtonText(b2, "Decrease Score", decreaseScore)
        updateButtonText(b4, "Play", playPressed)
        updateLabel()

    def timePressed():
        Tracker.Time = True
        Tracker.l_text = str(Tracker.TimeLimit) + " seconds"
        updateButtonText(b3, "Increase Time", increaseTime)
        updateButtonText(b2, "Decrease Time", decreaseTime)
        updateButtonText(b4, "Next", halfTimePressed)
        updateLabel()

    def updateButtonText(button, text, action):
        button.text = font.render(text, True, font_color)
        button.action = action

    def increaseTime():
        Tracker.TimeLimit += 1
        updateTime()

    def decreaseTime():
        if Tracker.TimeLimit > 1:
            Tracker.TimeLimit -= 1
        updateTime()

    def updateTime():
        Tracker.l_text = str(Tracker.TimeLimit) + " seconds"

    def updateScore():
        Tracker.l_text = Tracker.ScoreLimit

    def playPressed():
        Tracker.Running = False

    def halfTimePressed():
        updateButtonText(b2, "Yes", yesHalf)
        updateButtonText(b3, "No", noHalf)
        updateButtonText(b4, "", None)
        Tracker.l_text = "Half Time?"
        updateLabel()


    def yesHalf():
        Tracker.HalfTime = True
        playPressed()

    def noHalf():
        Tracker.HalfTime = False
        playPressed()

    def cancel():
        Tracker.Running = False

    pygame.init()
    width = 200
    height = 100
    window = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Game Selection")

    background_color = (0, 0, 0)
    font_color = (255, 255, 255)

    font = pygame.font.Font(None, 36)

    l = font.render("Select Game Mode", True, font_color)
    l_rect = l.get_rect()
    l_rect.center = (300, 100)
    window.blit(l, l_rect)

    num = font.render(Tracker.l_text, True, font_color)
    num_rect = num.get_rect()
    num_rect.center = (300, 250)
    window.blit(num, num_rect)

    b2_rect = pygame.Rect(75, 400, width, height)
    b2 = Button(b2_rect, "", timePressed)
    updateButtonText(b2, "Time Limit", timePressed)

    b3_rect = pygame.Rect(275, 400, width, height)
    b3 = Button(b3_rect, "", scorePressed)
    updateButtonText(b3, "Score Limit", scorePressed)

    b4_rect = pygame.Rect(475, 400, width, height)
    b4 = Button(b4_rect, "", cancel)
    updateButtonText(b4, "Cancel", cancel)

    buttons = [b2, b3, b4]

    while Tracker.Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Tracker.Running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(x, y):
                        button.action()

        window.fill(background_color)
        surface = updateLabel()
        window.blit(surface, num_rect.topleft)
        window.blit(l, l_rect)
        for button in buttons:
            if not Tracker.Running:
                break
            pygame.draw.rect(window, background_color, button.rect)
            button_rect = button.rect
            window.blit(button.text, button_rect)

        pygame.display.flip()
    if not Tracker.Running:
        main()

