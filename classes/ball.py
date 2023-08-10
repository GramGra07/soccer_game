
from trackers.trackers import Tracker
from util.functions import collision
from util.util import placeByPointAngle


class Ball:
    def __init__(self, startX, startY, imagefile, dx=0, dy=0):
        self.shape = imagefile
        self.top = startY - self.shape.get_height() / 2
        self.left = startX - self.shape.get_width() / 2
        self.width = self.shape.get_width()
        self.height = self.shape.get_height()
        self.radius = self.width / 2
        self.lastX = startX
        self.lastY = startY
        self.dx = dx
        self.dy = dy
        self.isPossessed = False
        self.centerX = self.left + self.radius
        self.centerY = self.top + self.radius
        self.bottom = self.top + self.height

    def show(self, surface):
        surface.blit(self.shape, (self.left, self.top))

    def UpdateCoords(self, x, y):
        self.left = x - self.shape.get_width() / 2
        self.top = y - self.shape.get_height() / 2
        self.lastX = x
        self.lastY = y
        self.centerX = self.left + self.radius
        self.centerY = self.top + self.radius

    def checkCollision(self, object1, object2, angle):
        if collision(object1, object2):
            if not object1.isPossessed:
                object1.dx = 0
                object1.dy = 0
                placeByPointAngle(object1, object2, angle)
            object1.isPossessed = True
        else:
            object1.isPossessed = False
    def collided(self, object1, object2):
        if collision(object1, object2):
            if object2.imageName == 'op1.png':
                Tracker.opponentPossession = True
            else:
                Tracker.teamPossession = True
            return True
        else:
            return False
