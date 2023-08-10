import pygame

from util.Sizes import Sizes
from trackers.trackers import Tracker

screenwidth, screenheight = (1000, 667)


class Player:

    def __init__(self, startX, startY, isOpponent):
        imageName = 'images/op1.png' if isOpponent else 'images/team.png'
        imagefile = pygame.image.load(imageName)
        if isOpponent:
            imagefile = pygame.transform.scale(imagefile, (Sizes.opSize, Sizes.opSize))
        else:
            imagefile = pygame.transform.scale(imagefile, (Sizes.playerSize, Sizes.playerSize))
        self.shape = imagefile
        self.image = imagefile
        self.imageName = imageName
        self.top = startY - self.shape.get_height() / 2
        self.bottom = self.top + self.shape.get_height()
        self.right = startX + self.shape.get_width() / 2
        self.left = startX - self.shape.get_width() / 2
        self.width = self.shape.get_width()
        self.height = self.shape.get_height()
        self.radius = self.width / 2
        self.centerX = self.left + self.radius
        self.centerY = self.top + self.radius
        self.dx = 0
        self.dy = 0
        self.lastX = startX
        self.lastY = startY
        self.startX = startX
        self.startY = startY
        if Tracker.leftHome:
            self.angle = 180 if self.imageName == 'images/op1.png' else 0
        else:
            self.angle = 0 if self.imageName == 'images/op1.png' else 180

    def show(self, surface):
        surface.blit(self.shape, (self.left, self.top))

    def UpdateCoords(self, x, y):
        self.left = x - self.shape.get_width() / 2
        self.top = y - self.shape.get_height() / 2
        self.right = x + self.shape.get_width() / 2
        self.bottom = y + self.shape.get_height() / 2
        self.lastX = x
        self.lastY = y
        self.centerX = self.left + self.radius
        self.centerY = self.top + self.radius

    def reset(self):
        self.UpdateCoords(self.startX, self.startY)
        self.dx = 0
        self.dy = 0
        if Tracker.leftHome:
            self.angle = 180 if self.imageName == 'images/op1.png' else 0
        else:
            self.angle = 0 if self.imageName == 'images/op1.png' else 180
    def toString(self):
        return self.imageName.replace('images/', '').replace('.png', '').replace('op', 'Away ').replace('team', 'Home ').replace('1', '')