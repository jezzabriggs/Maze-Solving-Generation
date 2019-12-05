from mazeGenerator import Maze, Cell
from cmu_112_graphics import *
from tkinter import *
import random
import heapq

# code adapted from https://github.com/laurentluce/python-algorithms/blob/master/algorithms/a_star_path_finding.py


class Node(object):
    def __init__(self, row, col, walls):
        self.row = row
        self.col = col
        self.walls = walls
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return (
            isinstance(self, Node)
            and isinstance(other, Node)
            and (
                self.row == other.row
                and self.col == other.col
                and self.walls == other.walls
            )
        )

    def __repr__(self):
        return f"Node{self.row, self.col}"

    def __gt__(self, other):
        if self.f > other.f:
            return True
        return False

    def __hash__(self):
        hashables = (self.row, self.col, self.parent)
        return hash(hashables)


class MazeSolver(object):
    def __init__(self, rows, cols, maze, start, finish):
        self.openList = []
        heapq.heapify(self.openList)
        self.closedSet = set()
        self.nodes = []
        self.rows = rows
        self.cols = cols
        self.maze = maze
        self.startNode = Node(start.row, start.col, start.walls)
        self.endNode = Node(finish.row, finish.col, finish.walls)
        self.createGrid()

    def createGrid(self):
        self.nodes = [[0] * self.cols for _ in range(self.rows)]
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                cell = self.maze[i][j]
                self.nodes[j][i] = Node(cell.row, cell.col, cell.walls)

    def getDirection(self, row, col, node):
        row1, col1 = node.row, node.col
        row2, col2 = row, col
        if row1 - row2 < 0 and col1 == col2:
            return "south"
        elif row1 - row2 > 0 and col1 == col2:
            return "north"
        elif col1 - col2 > 0 and row1 == row2:
            return "west"
        elif col1 - col2 < 0 and row1 == row2:
            return "east"

    def getNeighbours(self, node):
        neighboursList = []
        node = self.nodes[node.row][node.col]
        tempNeighbours = [
            (node.row - 1, node.col),
            (node.row + 1, node.col),
            (node.row, node.col - 1),
            (node.row, node.col + 1),
        ]
        for neighbour in tempNeighbours:
            (row, col) = neighbour
            if 0 <= row < self.rows and 0 <= col < self.cols:
                direction = self.getDirection(row, col, node)
                if direction not in node.walls:
                    neighboursList.append(neighbour)
        nodalNeighboursList = []
        for neighbour in neighboursList:
            (row, col) = neighbour
            node = self.nodes[row][col]
            nodalNeighboursList.append(node)
        return nodalNeighboursList

    def getH(self, node):
        return abs(node.col - self.endNode.col) + abs(node.row - self.endNode.row)

    def makePath(self):
        node = self.endNode
        path = [(node.row, node.col)]
        while node.parent is not self.startNode:
            node = node.parent
            if node != None:
                path.append((node.row, node.col))
        # add start nodes as they were not added earlier
        path.append((self.startNode.row, self.startNode.col))
        path = path[::-1]
        return path

    def addValueToNode(self, node, neighbour):
        neighbour.g = node.g + 1
        neighbour.h = self.getH(neighbour)
        neighbour.parent = node
        neighbour.f = neighbour.g + neighbour.h

    def solve(self):
        heapq.heappush(self.openList, (self.startNode.f, self.startNode))
        while len(self.openList) > 0:
            # chose the last node to process
            f, node = heapq.heappop(self.openList)
            # add to the closed list so that you know what you have from before
            self.closedSet.add(node)
            if node == self.endNode:
                self.endNode = node
                return self.makePath()
            neighbours = self.getNeighbours(node)
            for neighbour in neighbours:
                if neighbour not in self.closedSet:
                    if (neighbour.f, neighbour) in self.openList:
                        # checking to see if this path is better
                        if neighbour.g > node.g + 1:
                            self.addValueToNode(node, neighbour)
                    else:
                        self.addValueToNode(node, neighbour)
                        # add this node to open heap
                        heapq.heappush(self.openList, (neighbour.f, neighbour))
