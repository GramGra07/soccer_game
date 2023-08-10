import math


def getDistance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def getAngle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


def getAngleDegrees(x1, y1, x2, y2):
    return math.degrees(getAngle(x1, y1, x2, y2))


def getAngleFromDegrees(degrees):
    return math.radians(degrees)


def getPointFromAngleDistance(x, y, angle, distance):
    return x + math.cos(angle) * distance, y + math.sin(angle) * distance


def toDegrees(angle):
    return math.degrees(angle)


def toRadians(angle):
    return math.radians(angle)


def placeByPointAngle(object1, object2, angle):
    distance = 9 + object2.radius
    object1.UpdateCoords(object2.centerX + distance * (math.cos(angle)),
                         (object2.centerY + distance * (math.sin(angle))))
