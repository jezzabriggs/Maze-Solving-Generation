import random
import copy
from cmu_112_graphics import *  # this is imported from

# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
from tkinter import *
from mazeGenerator import Maze
from mazeGenerator import Cell
from MazeSolverReal import Node, MazeSolver
from scrollModeClasses import Player, Enemy, Star, Background, Door, Clock, Tree, Cloud

# this code is adapted from http://reeborg.ca/docs/en/reference/mazes.html
# and https://github.com/boppreh/maze/blob/master/maze.py


# cached image code used several times from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# the code is:
'''
    def getCachedPhotoImage(mode, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage
'''
# parts of this code are adapted from the code written for HW9 (Side-Scrolling Game)



##
#globals
#########################################

haveBonus = True

#########################################

class Square(object):
    # intitalizing object square to represent player in future
    def __init__(self, col, row, size):
        self.col = col
        self.row = row
        self.size = size
        self.hasKey = False


class IntroScreen(Mode):
    def appStarted(mode):
        mode.playGame = False
        mode.highScore = False
        mode.quit = False
        playerName = mode.getUserInput("Please enter your name")
        playerNames = open('highscores.txt', 'a')
        playerNames.write(f'\n{playerName}:')
        playerNames.close()
        mode.playGameLoc = (2*mode.width // 6, 2*mode.height // 6)
        mode.highScoreLoc = (4*mode.width // 6, 2*mode.height // 6)
        mode.controlLoc = (2*mode.width//6, 4 *mode.height//6)
        mode.quitLoc = (4*mode.width // 6, 4 * mode.height // 6)
        mode.buttonSize = (mode.width // 4, mode.height // 10)
        mode.highScoreFill = 'green'
        mode.controlFill = 'green'
        mode.quitFill = 'green'
        mode.playGameFill = 'green'
        url = 'https://imgur.com/E0YuaaC.png'
        mode.backgroundImage = mode.loadImage(url)

    def mousePressed(mode, event):
        sizeX, sizeY = mode.buttonSize
        playGameX, playGameY = mode.playGameLoc
        highScoreX, highScoreY = mode.highScoreLoc
        controlX, controlY = mode.controlLoc
        quitX, quitY = mode.quitLoc
        if (
            playGameX - sizeX / 2 <= event.x <= playGameX + sizeX / 2
            and playGameY - sizeY / 2 <= event.y <= playGameY + sizeY / 2
        ):
            mode.playGameFill = 'green'
            mode.app.setActiveMode(mode.app.scrollMode)
        elif (
            highScoreX - sizeX / 2 <= event.x <= highScoreX + sizeX / 2
            and highScoreY - sizeY / 2 <= event.y <= highScoreY + sizeY / 2
        ):
            mode.highScoreFill = 'green'
            mode.app.setActiveMode(mode.app.highScore)
        elif (controlX - sizeX/2 <= event.x <= controlX + sizeX/2 and controlY - sizeY/2 <= event.y <= controlY + sizeY/2):
            mode.controlFill = 'green'
            mode.app.setActiveMode(mode.app.controlsMode)
        elif (
            quitX - sizeX / 2 <= event.x <= quitX + sizeX / 2
            and quitY - sizeY / 2 <= event.y <= quitY + sizeY / 2
        ):
            mode.quitFill = 'green'
            playerNames = open('highscores.txt','a')
            playerNames.write(f"{mode.app.score}\n")
            playerNames.close()
            mode.app._running = False
            mode.app._root.quit()

    def mouseMoved(mode, event):
        sizeX, sizeY = mode.buttonSize
        playGameX, playGameY = mode.playGameLoc
        highScoreX, highScoreY = mode.highScoreLoc
        controlX, controlY = mode.controlLoc
        quitX, quitY = mode.quitLoc
        if (
            playGameX - sizeX / 2 <= event.x <= playGameX + sizeX / 2
            and playGameY - sizeY / 2 <= event.y <= playGameY + sizeY / 2
        ):
            mode.playGameFill = 'purple'
        elif (
            highScoreX - sizeX / 2 <= event.x <= highScoreX + sizeX / 2
            and highScoreY - sizeY / 2 <= event.y <= highScoreY + sizeY / 2
        ):
            mode.highScoreFill = 'purple'
        elif (controlX - sizeX/2 <= event.x <= controlX + sizeX/2 and\
                controlY - sizeY/2 <= event.y <= controlY + sizeY/2):
            mode.controlFill = 'purple'
        elif (
            quitX - sizeX / 2 <= event.x <= quitX + sizeX / 2
            and quitY - sizeY / 2 <= event.y <= quitY + sizeY / 2
        ):
            mode.quitFill = 'purple'
        else:
            mode.playGameFill = 'green'
            mode.quitFill = 'green'
            mode.controlFill = 'green'
            mode.highScoreFill = 'green'

    def getCachedPhotoImage(mode, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    def drawPlayGame(mode, canvas):
        xTemp, yTemp = mode.playGameLoc
        xSize, ySize = mode.buttonSize
        x1, y1 = xTemp - xSize / 2, yTemp - ySize / 2
        x2, y2 = xTemp + xSize / 2, yTemp + ySize / 2
        canvas.create_rectangle(x1, y1, x2, y2, fill=mode.playGameFill)
        canvas.create_text(xTemp, yTemp, text="Play Game", font="FixedSys 17 bold")

    def drawHighScore(mode, canvas):
        xTemp, yTemp = mode.highScoreLoc
        xSize, ySize = mode.buttonSize
        x1, y1 = xTemp - xSize / 2, yTemp - ySize / 2
        x2, y2 = xTemp + xSize / 2, yTemp + ySize / 2
        canvas.create_rectangle(x1, y1, x2, y2, fill=mode.highScoreFill)
        canvas.create_text(xTemp, yTemp, text="High Score", font="FixedSys 17 bold")

    def drawControlsMode(mode, canvas):
        xTemp, yTemp = mode.controlLoc
        xSize, ySize = mode.buttonSize
        x1, y1 = xTemp - xSize / 2, yTemp - ySize / 2
        x2, y2 = xTemp + xSize / 2, yTemp + ySize / 2
        canvas.create_rectangle(x1, y1, x2, y2, fill=mode.controlFill)
        canvas.create_text(xTemp, yTemp, text="Controls", font="FixedSys 17 bold")

    def drawQuit(mode, canvas):
        xTemp, yTemp = mode.quitLoc
        xSize, ySize = mode.buttonSize
        x1, y1 = xTemp - xSize / 2, yTemp - ySize / 2
        x2, y2 = xTemp + xSize / 2, yTemp + ySize / 2
        canvas.create_rectangle(x1, y1, x2, y2, fill=mode.quitFill)
        canvas.create_text(xTemp, yTemp, text="Quit", font="FixedSys 17 bold")

    def drawBackground(mode, canvas):
        canvas.create_image(mode.width//2, mode.height//2, image = mode.getCachedPhotoImage(mode.backgroundImage))

    def redrawAll(mode, canvas):
        mode.drawBackground(canvas)
        mode.drawPlayGame(canvas)
        mode.drawHighScore(canvas)
        mode.drawControlsMode(canvas)
        mode.drawQuit(canvas)

class ScrollMode(Mode):
    def appStarted(mode):
        mode.count = 0
        mode.player = Player(mode)
        mode.curEnemy = Enemy(mode)
        mode.star = Star(mode)
        mode.door = Door(mode)
        mode.background = Background(mode)
        mode.gameOver = False
        mode.clock = Clock(mode)
        mode.tree = Tree(mode)
        mode.cloud = Cloud(mode)

    def moveSprites(mode):
        if mode.count % 2 == 0:
            mode.player.spriteCounter = \
                (1 + mode.player.spriteCounter) % len(mode.player.sprites)

    def move(mode, move):
        mode.player.cx += move

    def jump(mode):
        jumpHeight = -10
        if mode.player.cy + jumpHeight > 0:
            mode.player.dy += jumpHeight
        
    def movePlayer(mode, pathTop):
        # move player
        if (mode.player.startY - mode.player.cy) > mode.player.jumpHeight:
            mode.player.dy = -mode.player.dy  
        if mode.player.cy > pathTop:
            mode.player.cy = pathTop
            mode.player.dy = 0
        mode.player.cy += mode.player.dy
        mode.player.cx += mode.player.dx
        if mode.player.cx > mode.width:
            mode.player.cx = mode.width
        elif mode.player.cx < 0:
            mode.player.cx = 0

    def moveEnemy(mode, pathTop):
        if mode.curEnemy.cy < mode.curEnemy.jumpHeight:
            mode.curEnemy.cy = mode.curEnemy.jumpHeight
            mode.curEnemy.dy = -mode.curEnemy.dy
        elif mode.curEnemy.cy > pathTop:
            mode.curEnemy.cy = pathTop
            mode.curEnemy.dy = -mode.curEnemy.dy
        mode.curEnemy.cy += mode.curEnemy.dy
        mode.curEnemy.scrollX += mode.curEnemy.dx

    def checkIntersectionStar(mode):
        starSizeX, starSizeY = 19, 19
        starY1, starY2 = mode.star.cy - starSizeY, mode.star.cy + starSizeY
        starX1, starX2 = mode.star.cx - mode.star.scrollX - starSizeX, mode.star.cx - mode.star.scrollX + starSizeX
        playerTop = mode.player.cy + 40
        playerBottom = mode.player.cy - 40
        playerLeft = mode.player.cx - 20
        playerRight = mode.player.cx + 20
        if starY1 <= playerTop <= starY2 and (starX1 <= playerLeft <= starX2 or\
            starX1 <= playerRight <= starX2):
            mode.app.score += 1
            mode.star.checkIntersection = True
            mode.star = Star(mode)
        elif starY1 <= playerBottom <= starY2 and (starX1 <= playerLeft <= starX2 or\
            starX1 <= playerRight <= starX2):
            mode.app.score += 1
            mode.star.checkIntersection = True
            mode.star = Star(mode)

    def checkIntersectionEnemies(mode):
        enemySizeX, enemySizeY = 20, 20
        enemyY1, enemyY2 = mode.curEnemy.cy - enemySizeY, mode.curEnemy.cy + enemySizeY
        enemyX1, enemyX2 = mode.curEnemy.cx - mode.curEnemy.scrollX - enemySizeX, mode.curEnemy.cx - mode.curEnemy.scrollX + enemySizeX
        playerTop = mode.player.cy + 40
        playerBottom = mode.player.cy - 40
        playerLeft = mode.player.cx - 20
        playerRight = mode.player.cx + 20
        if enemyY1 <= playerTop <= enemyY2 and (enemyX1 <= playerLeft <= enemyX2 or\
            enemyX1 <= playerRight <= enemyX2):
            mode.gameOver = True
        elif enemyY1 <= playerBottom <= enemyY2 and (enemyX1 <= playerLeft <= enemyX2 or\
            enemyX1 <= playerRight <= enemyX2):
            mode.gameOver = True

    def checkIntersectionDoor(mode):
        doorSizeX, doorSizeY = 46, 46
        doorY1, doorY2 = mode.door.cy - doorSizeY, mode.door.cy + doorSizeY
        doorX1, doorX2 = mode.door.cx - mode.door.scrollX - doorSizeX, mode.door.cx - mode.door.scrollX + doorSizeX
        playerTop = mode.player.cy + 40
        playerBottom = mode.player.cy - 40
        playerLeft = mode.player.cx - 20
        playerRight = mode.player.cx + 20
        if doorX1 <= playerLeft <= doorX2 and (doorY1 <= playerBottom <= doorY2):
            mode.restartGame()
            mode.app.mazeMode = MazeMode()
            mode.app.setActiveMode(mode.app.mazeMode)
        elif doorX1 <= playerRight <= doorX2 and doorY1 <= playerBottom <= doorY2:
            mode.restartGame()
            mode.app.mazeMode = MazeMode()
            mode.app.setActiveMode(mode.app.mazeMode)

    def checkIntersectionClock(mode):
        clockSizeX, clockSizeY = 30, 30
        clockY1, clockY2 = mode.clock.cy - clockSizeY, mode.clock.cy + clockSizeY
        clockX1, clockX2 = mode.clock.cx - mode.clock.scrollX - clockSizeX, mode.clock.cx - mode.clock.scrollX + clockSizeX
        playerTop = mode.player.cy + 40
        playerBottom = mode.player.cy - 40
        playerLeft = mode.player.cx - 20
        playerRight = mode.player.cx + 20
        if clockY1 <= playerTop <= clockY2 and (clockX1 <= playerLeft <= clockX2 or\
            clockX1 <= playerRight <= clockX2):
            haveBonus = True
            mode.clock = Clock(mode)
        elif clockY1 <= playerBottom <= clockY2 and (clockX1 <= playerLeft <= clockX2 or\
            clockX1 <= playerRight <= clockX2):
            haveBonus = True
            mode.clock = Clock(mode)

    def isEnemyPresent(mode):
        if mode.curEnemy.cx - mode.curEnemy.scrollX < 0:
            return True
        return False
    
    def isDoorPresent(mode):
        if mode.door.cx - mode.door.scrollX < 0:
            return True
        return False

    def isStarPresent(mode):
        if mode.star.cx - mode.star.scrollX < 0:
            return True
        return False
    
    def isClockPresent(mode):
        if mode.clock.cx - mode.clock.scrollX < 0:
            return True
        return False

    def isTreePresent(mode):
        if mode.tree.cx - mode.tree.scrollX < 0:
            return True
        return False

    def isCloudPresent(mode):
        if mode.cloud.cx - mode.cloud.scrollX < 0:
            return True
        return False

    def spawnDoor(mode):
        mode.door.dx = 6
        if mode.door.cx - mode.door.scrollX < 0:
            mode.door = Door(mode)

    def restartGame(mode):
        mode.player.cx = mode.player.startX
        mode.player.cy = mode.player.startY
        mode.player.dy = 0
        mode.star = Star(mode)
        mode.curEnemy = Enemy(mode)
        mode.door = Door(mode)
        mode.clock = Clock(mode)

    def spawnItem1(mode):
        posList = ['star', 'enemy', 'door']
        choice = random.choice(posList)
        if choice == 'star' and mode.isStarPresent():
            mode.star = Star(mode)
        elif choice == 'enemy' and mode.isEnemyPresent():
            mode.curEnemy = Enemy(mode)
        elif choice == 'door' and mode.isDoorPresent():
            mode.door = Door(mode)

    def spawnItem2(mode):
        posList = ['star', 'enemy', 'door']
        choice = random.choice(posList)
        if choice == 'star' and mode.isStarPresent():
            mode.star = Star(mode)
        elif choice == 'enemy' and mode.isEnemyPresent():
            mode.curEnemy = Enemy(mode)
        elif choice == 'door' and mode.isDoorPresent():
            mode.door = Door(mode)

    def spawnItem3(mode):
        posList = ['star', 'enemy', 'door']
        choice = random.choice(posList)
        if choice == 'star' and mode.isStarPresent():
            mode.star = Star(mode)
        elif choice == 'enemy' and mode.isEnemyPresent():
            mode.curEnemy = Enemy(mode)
        elif choice == 'door' and mode.isDoorPresent():
            mode.door = Door(mode)

    def timerFired(mode):
        if mode.gameOver == True:
            mode.app.setActiveMode(mode.app.gameOverMode)
        mode.count += 1
        mode.star.scrollX += mode.star.dx
        mode.door.scrollX += mode.door.dx
        mode.tree.scrollX += mode.door.dx
        mode.cloud.scrollX += mode.cloud.dx
        mode.cloud.dx = 4
        mode.curEnemy.dx = 6
        mode.star.dx = 7
        mode.door.dx = 5
        mode.tree.dx = 3
        mode.clock.dx = 9
        if mode.app.score > 5:
            if mode.star.cy > mode.player.cy:
                mode.star.dy = 5
            elif mode.star.cy < mode.player.cy - mode.player.jumpHeight:
                mode.star.dy = -5
        if mode.app.score > 10:
            if mode.curEnemy.cy > mode.player.cy:
                mode.curEnemy.dy = 8
            elif mode.curEnemy.cy < mode.player.cy - mode.player.jumpHeight:
                mode.curEnemy.dy = -4
        mode.star.cy -= mode.star.dy
        mode.curEnemy.cy -= mode.curEnemy.dy
        mode.clock.scrollX += mode.clock.dx
        mode.moveSprites()
        pathTop = mode.player.startY
        mode.movePlayer(pathTop)
        mode.moveEnemy(pathTop)
        if mode.count % 5 == 0: 
            mode.checkIntersectionStar()
        mode.checkIntersectionEnemies()
        mode.checkIntersectionDoor()
        if (mode.count % 10) == 0:
            mode.spawnItem1()
        if ((mode.count % 10) - 2) == 0:
            mode.spawnItem2()
        if ((mode.count % 10)-3) == 0:
            mode.spawnItem3()
        if mode.isClockPresent() and mode.count % 250 == 0:
            mode.clock = Clock(mode)
        mode.checkIntersectionClock()
        if mode.isTreePresent():
            mode.tree = Tree(mode)
        if mode.isCloudPresent():
            mode.cloud = Cloud(mode)

    def keyPressed(mode, event):
        if event.key == "Up":
            mode.jump()
        elif event.key == "Right":
            move = 5
            mode.move(move)
        elif event.key == "Left":
            move = -10
            mode.move(move)

    def getCachedPhotoImage(mode, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    def drawBackground(mode, canvas):
        x1 = mode.background.cx
        y1 = mode.background.cy
        image = mode.background.image
        canvas.create_image(x1, y1, image = mode.getCachedPhotoImage(image))

    def drawScore(mode, canvas):
        x = 7*mode.width//8
        y = 30
        canvas.create_text(x, y, text = f'Score: {mode.app.score}', 
        font = "FixedSys 20 bold")

    def drawPlayer(mode, canvas):
        sprite = mode.player.sprites[mode.player.spriteCounter]
        canvas.create_image(mode.player.cx, mode.player.cy, 
                            image=mode.getCachedPhotoImage(sprite))

    def drawStar(mode, canvas):
        x1 = mode.star.cx
        y1 = mode.star.cy
        x1 -= mode.star.scrollX
        image = mode.star.image
        canvas.create_image(x1, y1, image = mode.getCachedPhotoImage(image))

    def drawEnemy(mode, canvas):
        x1 = mode.curEnemy.cx
        y1 = mode.curEnemy.cy
        x1 -= mode.curEnemy.scrollX
        image = mode.curEnemy.image
        canvas.create_image(x1, y1, 
                    image=mode.getCachedPhotoImage(image))
    
    def drawDoor(mode, canvas):
        x1 = mode.door.cx
        y1 = mode.door.cy
        x1 -= mode.door.scrollX
        image = mode.door.image
        canvas.create_image(x1, y1, image = mode.getCachedPhotoImage(image))

    def drawClock(mode, canvas):
        x1 = mode.clock.cx
        y1 = mode.clock.cy
        x1 -= mode.clock.scrollX
        image = mode.clock.image
        canvas.create_image(x1, y1, image = mode.getCachedPhotoImage(image))

    def drawTree(mode, canvas):
        x1 = mode.tree.cx
        y1 = mode.tree.cy
        x1 -= mode.tree.scrollX
        image = mode.tree.image
        canvas.create_image(x1, y1, image = mode.getCachedPhotoImage(image))

    def drawCloud(mode, canvas):
        x1 = mode.cloud.cx
        y1 = mode.cloud.cy
        x1 -= mode.cloud.scrollX
        image = mode.cloud.image
        canvas.create_image(x1, y1, image = mode.getCachedPhotoImage(image))

    def redrawAll(mode, canvas):
        mode.drawBackground(canvas)
        mode.drawScore(canvas)
        mode.drawTree(canvas)
        if not mode.star.checkIntersection:
            mode.drawStar(canvas)
        mode.drawEnemy(canvas)
        mode.drawDoor(canvas)
        mode.drawClock(canvas)
        mode.drawPlayer(canvas)
        mode.drawCloud(canvas)

class MazeMode(Mode):
    def appStarted(mode):
        mode.initBools()
        mode.initMaze()
        mode.initCharacters()
        mode.initMazeSolving()
        mode.initKey()
        mode.count = 0
        mode.pathIndex1, mode.pathIndex2 = 0, 0
        mode.enemyPathSolver = MazeSolver(mode.maze.rows, mode.maze.cols, mode.mazeCells, mode.startCell, mode.squareCell)
        mode.enemyPath = mode.enemyPathSolver.solve()
        url = "https://imgur.com/ud2bc4O.png"
        scale = 1/(mode.maze.cols)
        mode.keyImage = mode.loadImage(url) 
        mode.keyImage = mode.scaleImage(mode.keyImage, scale)
        mode.loadFinishImage()
        if mode.keyMode:
            mode.placeKey()

    
    def loadFinishImage(mode):
        url = "https://imgur.com/CIWZzIi.png"
        if mode.maze.cols < 10:
            scale = 1/4
        elif 10 <= mode.maze.cols < 20:
            scale = 1/8
        else:
            scale = 1/12
        mode.flagImage = mode.loadImage(url) 
        mode.flagImage = mode.scaleImage(mode.flagImage, scale)      
        
    def initMaze(mode):
        if mode.app.score == 0:
            mode.maze = Maze(5, 5)
            if haveBonus:
                mode.timer = 10
            else: mode.timer = 7
            mode.keyFind = False
            mode.keyMode = False
            mode.drawKey = False
            mode.gate = False
        elif 5 >= mode.app.score > 0:
            mode.maze = Maze(7, 7)
            if haveBonus:
                mode.timer = 20
            else: mode.timer = 10
            mode.keyFind = False
            mode.keyMode = False
            mode.drawKey = False
            mode.gate = False
        elif 10 >= mode.app.score > 5:
            mode.maze = Maze(10, 10)
            mode.keyFind = True
            mode.keyMode = True
            mode.drawKey = True
            mode.gate = True
            if haveBonus:
                mode.timer = 35
            else: mode.timer = 30
        elif 20 >= mode.app.score > 10:
            mode.haveEnemy = True
            mode.maze = Maze(15, 15)
            if haveBonus:
                mode.timer = 50
            else: mode.timer = 40
            mode.keyFind = False
            mode.keyMode = False
            mode.drawKey = False
            mode.gate = False
        elif 45 >= mode.app.score > 20:
            mode.maze = Maze(20, 20)
            mode.haveEnemy = True
            mode.keyFind = True
            mode.keyMode = True
            mode.drawKey = True
            mode.gate = True
            if haveBonus:
                mode.timer = 65
            else: mode.timer = 50
        else:
            mode.maze = Maze(25, 25)
            mode.haveEnemy = True
            mode.keyFind = True
            mode.keyMode = True
            mode.drawKey = True
            mode.gate = True
            if haveBonus:
                mode.timer = 80
            else: mode.timer = 60
        mode.mazeCells = Maze.createMaze(mode.maze.cols, mode.maze.rows)
        mode.oldMazeCells = copy.deepcopy(mode.mazeCells)
    
    def initCharacters(mode):
        mode.square = Square(0, 0, mode.width // (mode.maze.cols + 3))
        mode.squareSize = mode.width // (mode.maze.cols)
        mode.enemy = Square(mode.maze.cols - 1, 0, mode.width // (mode.maze.cols + 3))
        mode.loadEnemySprite()
    
    def loadEnemySprite(mode):
        url = "https://i.imgur.com/dZ0UdVj.png"
        mode.enemy.sprites = []
        mode.enemy.spriteCounter = 0
        spritestrip = mode.loadImage(url)
        imageScale = 2
        spritestrip = mode.scaleImage(spritestrip, imageScale)
        imageSizeX1, imageSizeX2 = 0, 27
        imageIncrement = 33
        imageTop, imageBottom = 0, 100
        mode.spriteCounter = 0
        numPics = 8
        for i in range(numPics):
            sprite = spritestrip.crop(
                (
                    imageSizeX1 + imageIncrement * i,
                    imageTop,
                    imageSizeX2 + imageIncrement * i,
                    imageBottom,
                )
            )
            mode.enemy.sprites.append(sprite)

    def initMazeSolving(mode):
        mode.startCell = mode.mazeCells[mode.enemy.col][mode.enemy.row]
        mode.finishCell = mode.mazeCells[mode.maze.rows - 1][mode.maze.cols - 1]
        mode.squareCell = mode.mazeCells[mode.square.col][mode.square.row]
        mode.cellsVisited = [(mode.square.row, mode.square.col)]
        mode.alreadySeenCells = set()
        mode.backtrackSolution = []

    def initBools(mode):
        mode.squarehaskey = False
        mode.backtrack = False
        mode.haveEnemy = False
        mode.drawGetKey = False

    def initKey(mode):
        mode.keyCol = 0
        mode.keyRow = mode.maze.rows

    def getDirection(mode, direction):
        if direction == "north":
            return (-1, 0)
        elif direction == "south":
            return (+1, 0)
        elif direction == "east":
            return (0, +1)
        elif direction == "west":
            return (0, -1)

    def isValidMove(mode, row, col, drow, dcol, direction):
        if not (
            0 <= row + drow <= mode.maze.rows - 1
            and 0 <= col + dcol <= mode.maze.cols - 1
        ):
            return False
        cell = mode.mazeCells[col][row]
        return direction not in cell.walls

    def solveMaze(mode, row, col):
        if mode.keyMode:
            mode.drawGetKey = True
        if mode.squarehaskey:
            if row == mode.finishCell.row and col == mode.finishCell.col:
                return mode.cellsVisited
        # recursive case
            cell = mode.mazeCells[col][row]
            posDirs = set()
            for direction in ["north", "south", "east", "west"]:
                posDirs.add(direction)
            for direction in posDirs:
                drow, dcol = mode.getDirection(direction)
                newRow, newCol = row + drow, col + dcol
                if (
                    mode.isValidMove(row, col, drow, dcol, direction)
                    and (newRow, newCol) not in mode.alreadySeenCells
                ):
                    mode.cellsVisited.append((cell.row + drow, cell.col + dcol))
                    mode.alreadySeenCells.add((cell.row + drow, cell.col + dcol))
                    posSolution = mode.solveMaze(row + drow, col + dcol)
                    if posSolution != None:
                        return posSolution
                    mode.cellsVisited.pop()
            return None
        else:
            mazeSolver = MazeSolver(mode.maze.rows, mode.maze.cols, mode.mazeCells, mode.squareCell, mode.finishCell)
            path = mazeSolver.solve()
            return path

    def placeKey(mode):
        posList = mode.mazeCells[:-3]
        cell = posList[random.randint(0, len(mode.mazeCells) - 3)][random.randint(0, len(mode.mazeCells[0])-1)]
        row, col = cell.row, cell.col
        mode.keyRow, mode.keyCol = row, col

    def addGate(mode):
        oldWalls = mode.finishCell.walls
        neighbours = mode.enemyPathSolver.getNeighbours(mode.finishCell)
        for cell in neighbours:
            cell = mode.mazeCells[cell.col][cell.row]
            cell.walls.add(cell.cellDirection(mode.finishCell))
        for wall in ['north', 'south', 'east', 'west']:
            if wall not in oldWalls:
                mode.finishCell.walls.add(wall)

    def removeGate(mode):
        mode.mazeCells = mode.oldMazeCells

    def checkSquareHasKey(mode):
        return mode.square.row == mode.keyRow and mode.square.col == mode.keyCol
        
    def checkGameOver(mode):
        return (mode.square.col == mode.enemy.col and mode.square.row == mode.enemy.row)
        
    def checkMazeSolved(mode):
        if (mode.square.col == mode.finishCell.col and mode.square.row == mode.finishCell.row):
            mode.square = Square(0, 0, mode.width // (mode.maze.cols + 3))
            mode.app.score = mode.app.score + 0.75*mode.maze.cols//1
            haveBonus = False
            mode.app.setActiveMode(mode.app.scrollMode)

    def moveSprites(mode):
        if mode.count % 2 == 0:
            mode.enemy.spriteCounter = \
                (1 + mode.enemy.spriteCounter) % len(mode.enemy.sprites)

    def timerFired(mode):
        mode.count += 1
        mode.moveSprites()
        if mode.enemy.row < len(mode.mazeCells) and mode.enemy.col < len(mode.mazeCells[0]):
            mode.squareCell = mode.mazeCells[mode.square.col][mode.square.row]
            mode.startCell = mode.mazeCells[mode.enemy.col][mode.enemy.row]
        if mode.haveEnemy:
            if mode.checkGameOver():
                mode.app.setActiveMode(mode.app.gameOverMode)
        if mode.count % 2 == 0:
            mode.pathIndex1 += 1
            if mode.haveEnemy:
                mode.pathIndex2 += 1
            if mode.pathIndex2 < len(mode.enemyPath):
                (row, col) = mode.enemyPath[mode.pathIndex2]
                mode.enemy.row, mode.enemy.col = row, col
            if mode.backtrackSolution != None and 0 < len(mode.backtrackSolution) and mode.pathIndex1 < len(
                mode.backtrackSolution
            ):
                mode.square.row, mode.square.col = mode.backtrackSolution[
                    mode.pathIndex1
                ]
            if mode.backtrackSolution != None and mode.pathIndex1 > len(mode.backtrackSolution):
                mode.pathIndex1 -= 1
        if mode.checkSquareHasKey():
            mode.drawKey = False
            mode.drawGate = False
            mode.gate = False
            mode.keyMode = False
            mode.squarehaskey = True
            mode.removeGate()
        if mode.gate:
            mode.addGate()
        mode.checkMazeSolved()
        if mode.count % 25 == 0:
            mode.timer -= 1
        if mode.timer == 0:
            mode.app.setActiveMode(mode.app.gameOverMode)
        if mode.backtrack:
            if mode.drawGetKey and mode.count % 50 == 0:
                mode.drawGetKey = False

    def doMove(mode, dx, dy):
        # moves square and prevents movements across walls
        if mode.squareCell != mode.startCell:
            mode.enemyPathSolver = MazeSolver(mode.maze.rows, mode.maze.cols, mode.mazeCells, mode.startCell, mode.squareCell)
            mode.enemyPath = mode.enemyPathSolver.solve()
            mode.pathIndex2 = 0
        curCell = mode.mazeCells[mode.square.col][mode.square.row]
        if dx > 0 and dy == 0:
            if "east" not in curCell.walls:
                mode.square.col += dx
        elif dx < 0 and dy == 0:
            if "west" not in curCell.walls:
                mode.square.col += dx
        elif dx == 0 and dy > 0:
            if "south" not in curCell.walls:
                mode.square.row += dy
        elif dx == 0 and dy < 0:
            if "north" not in curCell.walls:
                mode.square.row += dy
        if mode.haveEnemy:
            mode.squareCell = mode.mazeCells[mode.square.col][mode.square.row]
            mode.enemyPathSolver = MazeSolver(mode.maze.rows, mode.maze.cols, mode.mazeCells, mode.startCell, mode.squareCell)
            mode.enemyPath = mode.enemyPathSolver.solve()

    def keyPressed(mode, event):
        # changes the co-ordinates of square according to key press
        if event.key == "Right" and mode.square.col + 1 < mode.maze.cols:
            mode.doMove(+1, 0)
        elif event.key == "Left" and mode.square.col > 0:
            mode.doMove(-1, 0)
        elif event.key == "Up" and mode.square.row > 0:
            mode.doMove(0, -1)
        elif event.key == "Down" and mode.square.row + 1 < mode.maze.rows:
            mode.doMove(0, +1)
        elif event.key == "s":
            mode.backtrackSolution = mode.solveMaze(mode.squareCell.row, mode.squareCell.col)
            if mode.backtrackSolution == None:
                mode.backtrack = False
            mode.backtrack = not mode.backtrack
            mode.haveEnemy = False
        elif event.key == "r":
            mode.haveEnemy = not mode.haveEnemy

    def cellDirection(mode, row1, col1, row2, col2):
        # returns the direction of the common wall between the two input cells
        if not abs(col1 - col2) + abs(row1 - row2) == 1:
            return False
        elif row2 > row1:
            return "south"
        elif row2 < row1:
            return "north"
        elif col2 < col1:
            return "west"
        elif col2 > col1:
            return "east"
        else:
            return False

    def getCachedPhotoImage(mode, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    def drawCells(mode, canvas):
        for i in range(len(mode.mazeCells)):
            for j in range(len(mode.mazeCells[0])):
                cell = mode.mazeCells[i][j]
                if cell == mode.mazeCells[-1][-1] and mode.gate: fill = 'red'
                else: fill = 'blue'
                x = mode.squareSize * cell.col
                y = mode.squareSize * cell.row
                for wall in cell.walls:
                    if wall == "north":
                        canvas.create_line(
                            x, y, x + mode.squareSize, y, fill=fill, width=5
                        )
                    if wall == "south":
                        canvas.create_line(
                            x,
                            y + mode.squareSize,
                            x + mode.squareSize,
                            y + mode.squareSize,
                            fill="blue",
                            width=5,
                        )
                    if wall == "west":
                        canvas.create_line(
                            x, y, x, y + mode.squareSize, fill=fill, width=5
                        )
                    if wall == "east":
                        canvas.create_line(
                            x + mode.squareSize,
                            y,
                            x + mode.squareSize,
                            y + mode.squareSize,
                            fill=fill,
                            width=5,
                        )

    def drawSquare(mode, canvas):
        # gets co-ordinates for drawing the square and draws it
        r1 = mode.squareSize // (mode.maze.cols//2)
        r2 = mode.squareSize//(mode.maze.cols//1.5)
        x = mode.square.col * mode.squareSize + mode.squareSize//2
        y = mode.square.row * mode.squareSize + mode.squareSize//2
        canvas.create_oval(x - r1, y-r1, x+r1, y+r1, fill="brown")
        canvas.create_oval(x - r2, y - r2, x+r2, y+r2, fill = 'yellow')

    def drawEnemy(mode, canvas):
        sprite = mode.enemy.sprites[mode.enemy.spriteCounter]
        x = mode.enemy.col * mode.squareSize + mode.squareSize//2
        y = mode.enemy.row * mode.squareSize + mode.squareSize
        canvas.create_image(x, y, 
                            image=mode.getCachedPhotoImage(sprite))

    def drawFinish(mode, canvas):
        image = mode.flagImage
        x = mode.finishCell.col * mode.squareSize + mode.squareSize/2
        y = mode.finishCell.row * mode.squareSize + mode.squareSize/2
        canvas.create_image(x, y, image=mode.getCachedPhotoImage(image))

    def drawingKey(mode, canvas):
        x = (mode.keyCol)*mode.squareSize + mode.squareSize/2
        y = (mode.keyRow)*mode.squareSize + mode.squareSize/2
        image = mode.keyImage
        canvas.create_image(x, y, image = mode.getCachedPhotoImage(image))

    def drawNorth(mode, canvas, row1, col1, row2, col2):
        x1 = col1 * mode.squareSize + mode.squareSize / 2
        y1 = row1 * mode.squareSize + mode.squareSize / 2
        x2 = col2 * mode.squareSize + mode.squareSize / 2
        y2 = row2 * mode.squareSize + mode.squareSize / 2
        canvas.create_line(x1, y1, x2, y2, fill="green", width=3)

    def drawSouth(mode, canvas, row1, col1, row2, col2):
        x1 = col1 * mode.squareSize + mode.squareSize / 2
        y1 = row1 * mode.squareSize + mode.squareSize / 2
        x2 = col2 * mode.squareSize + mode.squareSize / 2
        y2 = row2 * mode.squareSize + mode.squareSize / 2
        canvas.create_line(x1, y1, x2, y2, fill="green", width=3)

    def drawEast(mode, canvas, row1, col1, row2, col2):
        x1 = col1 * mode.squareSize + mode.squareSize / 2
        y1 = row1 * mode.squareSize + mode.squareSize / 2
        x2 = col2 * mode.squareSize + mode.squareSize / 2
        y2 = row2 * mode.squareSize + mode.squareSize / 2
        canvas.create_line(x1, y1, x2, y2, fill="green", width=3)

    def drawWest(mode, canvas, row1, col1, row2, col2):
        x1 = col1 * mode.squareSize + mode.squareSize / 2
        y1 = row1 * mode.squareSize + mode.squareSize / 2
        x2 = col2 * mode.squareSize + mode.squareSize / 2
        y2 = row2 * mode.squareSize + mode.squareSize / 2
        canvas.create_line(x1, y1, x2, y2, fill="green", width=3)

    def drawBacktrackPath(mode, canvas):
        for index in range(1, mode.pathIndex1):
            (row1, col1) = mode.backtrackSolution[index - 1]
            (row2, col2) = mode.backtrackSolution[index]
            direction = mode.cellDirection(row1, col1, row2, col2)
            if direction == "north":
                mode.drawNorth(canvas, row1, col1, row2, col2)
            elif direction == "south":
                mode.drawSouth(canvas, row1, col1, row2, col2)
            elif direction == "east":
                mode.drawEast(canvas, row1, col1, row2, col2)
            elif direction == "west":
                mode.drawWest(canvas, row1, col1, row2, col2)

    def drawTimer(mode, canvas):
        x = 7*mode.width//8
        y = 25
        canvas.create_text(x, y, text = f'Time:{mode.timer}', 
                    font = 'FixedSys 18 bold', fill = 'white') 

    def drawgetKey(mode, canvas):
        x = mode.width//2
        y = mode.height//2
        canvas.create_text(x, y, text = "Get Key First!",
            font = 'FixedSys 24 bold', fill = 'white')

    def redrawAll(mode, canvas):
        # draws the square and the maze
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="orange")
        mode.drawCells(canvas)
        mode.drawSquare(canvas)
        mode.drawFinish(canvas)
        if mode.haveEnemy:
            mode.drawEnemy(canvas)
        if mode.backtrackSolution != None and mode.backtrack == True:
            mode.drawBacktrackPath(canvas)
        if mode.drawKey:
            mode.drawingKey(canvas)
        mode.drawTimer(canvas)
        if mode.backtrack and mode.drawGetKey:
            mode.drawgetKey(canvas)

class ControlsMode(Mode):
    def appStarted(mode):
        mode.backButtonLoc = (mode.width//7, 100)
        mode.buttonSize = (mode.width//16, mode.width//24)
        mode.buttonFill = 'green'
        mode.loadImages()

    def loadImages(mode):
        url1 = "https://i.imgur.com/rvKz6JI.png"
        url2 = "https://imgur.com/EKbDEkj.png"
        url3 = "https://imgur.com/gH92X7Z.png"
        url4 = "https://i.imgur.com/2v6yc8O.png"
        mode.image1 = mode.loadImage(url1)
        mode.image2 = mode.loadImage(url2)
        mode.image3 = mode.loadImage(url3)
        mode.image4 = mode.loadImage(url4)
        mode.image4 = mode.scaleImage(mode.image4, 1/4)

    def mouseMoved(mode, event):
        sizeX, sizeY = mode.buttonSize
        buttonLocX, buttonLocY = mode.backButtonLoc
        if buttonLocX - sizeX <= event.x <= buttonLocX + sizeX and\
            buttonLocY - sizeY <= event.y <= buttonLocY + sizeY:
            mode.buttonFill = 'purple'
        else:
            mode.buttonFill = 'green'

    def mousePressed(mode, event):
        sizeX, sizeY = mode.buttonSize
        buttonLocX, buttonLocY = mode.backButtonLoc
        if buttonLocX - sizeX <= event.x <= buttonLocX + sizeX and\
            buttonLocY - sizeY <= event.y <= buttonLocY + sizeY:
            mode.buttonFill = 'green'
            mode.app.setActiveMode(mode.app.introScreen)

    def createBackButton(mode, canvas):
        buttonLocX, buttonLocY = mode.backButtonLoc
        sizeX, sizeY = mode.buttonSize
        canvas.create_rectangle(buttonLocX - sizeX, buttonLocY - sizeY,
                                buttonLocX + sizeX, buttonLocY + sizeY,
                                fill = mode.buttonFill)
        canvas.create_text(buttonLocX, buttonLocY, text = 'Back',
                            font = 'FixedSys 17 bold')

    def getCachedPhotoImage(mode, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'pink')
        canvas.create_text(mode.width//2, mode.height//2, text = 
        ''' 
        While Scrolling:
        Use the right and left arrow Keys \n \tto move forward and backwards
        Use the up arrow key to jump
\n
\n
\n

        While in Maze:
        Use the arrow keys to navigate through \n \tthe maze and reach the finish flag.\n
        Press the 's' button for the computer to solve the Maze for you!
        ''', font = 'FixedSys 17 bold')
        image1 = mode.image1
        image2 = mode.image2
        image3 = mode.image3
        image4 = mode.image4
        canvas.create_image(mode.width//3, mode.height//2, image = mode.getCachedPhotoImage(image1))
        canvas.create_image(2*mode.width//3, mode.height//2, image = mode.getCachedPhotoImage(image3))
        canvas.create_image(mode.width//3, 5*mode.height//6, image = mode.getCachedPhotoImage(image2))
        canvas.create_image(2*mode.width//3, 5*mode.height//6, image = mode.getCachedPhotoImage(image4))
        mode.createBackButton(canvas)


class GameOverMode(Mode):
    def appStarted(mode):
        playerNames = open('highscores.txt','a')
        playerNames.write(f"{mode.app.score}\n")
        playerNames.close()


    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
        canvas.create_text(
            mode.width // 2, mode.height // 2, text="Game Over!", 
            fill="white", font = "FixedSys 40 bold")


class HighScoreMode(Mode):
    def appStarted(mode):
        playerNames = open('highscores.txt', 'r')
        mode.highDict = mode.createDict(playerNames)
        mode.backButtonLoc = (mode.width//7, 100)
        mode.buttonSize = (mode.width//16, mode.width//24)
        mode.buttonFill = 'green'
    
    def mouseMoved(mode, event):
        sizeX, sizeY = mode.buttonSize
        buttonLocX, buttonLocY = mode.backButtonLoc
        if buttonLocX - sizeX <= event.x <= buttonLocX + sizeX and\
            buttonLocY - sizeY <= event.y <= buttonLocY + sizeY:
            mode.buttonFill = 'purple'
        else:
            mode.buttonFill = 'green'

    def mousePressed(mode, event):
        sizeX, sizeY = mode.buttonSize
        buttonLocX, buttonLocY = mode.backButtonLoc
        if buttonLocX - sizeX <= event.x <= buttonLocX + sizeX and\
            buttonLocY - sizeY <= event.y <= buttonLocY + sizeY:
            mode.buttonFill = 'green'
            mode.app.setActiveMode(mode.app.introScreen)
    
    def createDict(mode, playerNames):
        highDict = dict()
        for line in playerNames.readlines():
            allParts = []
            for parts in line.split(":"):
                allParts.append(parts)
            name = allParts[0]
            score = allParts[-1].strip()
            if name not in highDict and score.isdigit():
                highDict[name] = int(score)
            elif name not in highDict and not score.isdigit():
                highDict[name] = 0
            elif name in highDict and score.isdigit():
                if highDict[name] < int(score):
                    highDict[name] = int(score)
        highDictReal = dict()
        sortList = []
        for key in highDict:
            sortList.append((highDict[key], key))
        sortList = sorted(sortList)
        sortList = sortList[::-1]
        if len(sortList) > 10:
            sortList = sortList[:10]
        for values in sortList:
            score = values[0]
            name = values[1]
            highDictReal[name] = score
        return highDictReal   

    def createBackButton(mode, canvas):
        buttonLocX, buttonLocY = mode.backButtonLoc
        sizeX, sizeY = mode.buttonSize
        canvas.create_rectangle(buttonLocX - sizeX, buttonLocY - sizeY,
                                buttonLocX + sizeX, buttonLocY + sizeY,
                                fill = mode.buttonFill)
        canvas.create_text(buttonLocX, buttonLocY, text = 'Back',
                            font = 'FixedSys 17 bold')            

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'pink')
        num = 0
        for key in mode.highDict:
            startY = mode.height//(len(mode.highDict.values()))
            inc = mode.height/(len(mode.highDict.values()) + 1)
            x = mode.width//2
            y = startY + inc*num
            canvas.create_text(x, y, text = f'{key.upper()}:{mode.highDict[key]}',
                font = "FixedSys 20 bold")
            num += 1
        mode.createBackButton(canvas)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.score = 7
        app.introScreen = IntroScreen()
        app.scrollMode = ScrollMode()
        app.mazeMode = MazeMode()
        app.highScore = HighScoreMode()
        app.gameOverMode = GameOverMode()
        app.controlsMode = ControlsMode()
        app.setActiveMode(app.introScreen)
        app.timerDelay = 25

app = MyModalApp(width = 1000, height = 1000)