from cmu_112_graphics import *  # this is imported from

# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
from tkinter import *
from PIL import Image
import random


class Background(object):
    def __init__(self, mode):
        self.mode = mode
        self.cx = mode.width // 2
        self.cy = mode.height // 2
        self.createImage()

    def createImage(self):
        url = "https://imgur.com/HshlLcI.png"
        image = self.mode.loadImage(url)
        imageScale = 1
        image = self.mode.scaleImage(image, imageScale)
        self.image = image


class Player(object):
    # player class
    def __init__(self, mode):
        self.mode = mode
        self.startX, self.startY = 100, 750
        self.cx = self.startX
        self.cy = self.startY
        self.dx, self.dy = 0, 0
        self.jumpHeight = 150
        self.createSprite(mode)

    # sprite creating code adapted from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    def createSprite(self, mode):
        self.sprites = []
        self.spriteCounter = 0
        url = "https://imgur.com/1Q18wIZ.png"
        spritestrip = self.mode.loadImage(url)
        imageScale = 1 / 2
        spritestrip = self.mode.scaleImage(spritestrip, imageScale)
        imageSizeX1, imageSizeX2 = 0, 40
        imageIncrement = 50
        imageTop, imageBottom = 0, 80
        self.spriteCounter = 0
        numPics = 3
        for i in range(numPics):
            sprite = spritestrip.crop(
                (
                    imageSizeX1 + imageIncrement * i,
                    imageTop,
                    imageSizeX2 + imageIncrement * i,
                    imageBottom,
                )
            )
            self.sprites.append(sprite)


class Enemy(object):
    # enemy class
    def __init__(self, mode):
        self.mode = mode
        startPos = 1.2
        self.startX, self.startY = (
            1200,
            random.randint(self.mode.player.cy - 100, self.mode.player.cy + 50),
        )
        self.cx = self.startX
        self.cy = self.startY
        self.scrollX = 0
        self.dx, self.dy = 0, 0
        self.enemyPresent = False
        self.jumpHeight = 100
        self.createImage(mode)

    def createImage(self, mode):
        url = "https://i.imgur.com/dvBr9HO.png"
        image = self.mode.loadImage(url)
        imageScale = 1 / 3
        image = self.mode.scaleImage(image, imageScale)
        self.image = image


class Star(object):
    # stars to increase score
    def __init__(self, mode):
        self.mode = mode
        self.hasPowerUp = False
        self.startX, self.startY = 1500, random.randint(600, 700)
        self.cx = self.startX
        self.cy = self.startY
        self.scrollX = 0
        self.dx = 0
        self.dy = 0
        self.checkIntersection = False
        self.itemPresent = False
        self.createImage(mode)

    def createImage(self, mode):
        url = "https://imgur.com/GCIZP88.png"
        image = self.mode.loadImage(url)
        imageScale = 1 / 6
        image = self.mode.scaleImage(image, imageScale)
        self.image = image


class Door(object):
    def __init__(self, mode):
        self.mode = mode
        self.startX, self.startY = 2000, random.randint(700, 750)
        self.cx = self.startX
        self.cy = self.startY
        self.scrollX = 0
        self.dx = 0
        self.dy = 0
        self.checkIntersection = False
        self.itemPresent = False
        self.createImage(mode)

    def createImage(self, mode):
        url = "https://imgur.com/vEJbkIv.png"
        image = self.mode.loadImage(url)
        imageScale = 1 / 2
        image = self.mode.scaleImage(image, imageScale)
        self.image = image


class Clock(object):
    def __init__(self, mode):
        self.mode = mode
        self.startX, self.startY = 2000, random.randint(600, 700)
        self.cx = self.startX
        self.cy = self.startY
        self.scrollX = 0
        self.dx = 0
        self.dy = 0
        self.checkIntersection = False
        self.itemPresent = False
        self.createImage(mode)

    def createImage(self, mode):
        url = "https://i.imgur.com/CtGmdGa.png"
        image = self.mode.loadImage(url)
        imageScale = 1 / 6
        image = self.mode.scaleImage(image, imageScale)
        self.image = image


class Tree(object):
    def __init__(self, mode):
        self.mode = mode
        self.startX, self.startY = 1100, 650
        self.cx = self.startX
        self.cy = self.startY
        self.scrollX = 0
        self.dx = 0
        self.dy = 0
        self.checkIntersection = False
        self.itemPresent = False
        self.createImage(mode)

    def createImage(self, mode):
        url = "https://i.imgur.com/KJmawuw.png"
        image = self.mode.loadImage(url)
        imageScale = 1 / 2
        image = self.mode.scaleImage(image, imageScale)
        self.image = image


class Cloud(object):
    def __init__(self, mode):
        self.mode = mode
        self.startX, self.startY = 1200, 200
        self.cx = self.startX
        self.cy = self.startY
        self.scrollX = 0
        self.dx = 0
        self.dy = 0
        self.checkIntersection = False
        self.itemPresent = False
        self.createImage(mode)

    def createImage(self, mode):
        url = "https://i.imgur.com/FdJqq1S.png"
        image = self.mode.loadImage(url)
        imageScale = 1 / 3
        image = self.mode.scaleImage(image, imageScale)
        self.image = image
