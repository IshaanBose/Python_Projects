"""
A* GUI Program
==============

NOTE: This is a WIP, currently this program only creates the main menu GUI and the maze GUI.

This is a program that implements the A* path finding algorithm using GUI.

Input is to be given in the form of 'x y'. All input is given in terms of number of cells and not pixels, so when we give 'Maze Dimensions'
as '10 10', it means 10 cells by 10 cells and not 10px by 10px. Checking 'Yes' for 'Show Exploration' will show the exploration path of 
the program. Due to the amount of changes being made to the GUI, this will cause the program to work slower than if 'Show Exploration' 
was checked as 'No'.

Once at the maze GUI, you can click on the cells to create/remove obstacles. Once you have added/removed the desired amount of obstacles, 
you press the RETURN key to start the execution of the program.
"""

from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import SOLID
from tkinter import Radiobutton
from tkinter import font as tkfont
from tkinter import BooleanVar
from tkinter.messagebox import showwarning
import pygame
from pygame.locals import *
from pygame import draw as pdraw
import math

class Node:
    def __init__(self, pos, parent=None, g=0, h=0):
        self.pos = pos
        self.parent = parent
        self.g = g
        self.h = h
        self.f = self.g + self.h
        
class AugList(list):
    def __init__(self, l):
        list.__init__(self, l)
        
    def inlist(self, node):
        for i in range(len(self)):
            if self[i].pos == node.pos:
                return [True, i]
        return [False, i]
    
    def inlist2(self, node):
        for i in range(len(self)):
            if self[i].pos == node:
                return True
        return False

class PygameMaze():
    """
    This class creates the maze GUI and contains functions that implements the A* algorithm.
    """
    def __init__(self, maze_dim, start_node, goal_node, show_exp):
        """
        Initialises the maze GUI.
        
        Parameter
        ---------
        `maze_dim: list/tuple`
            Dimensions of the maze in cells.
            
        `start_node: list/tuple`
            Co-ordinates of starting node.
            
        `goal_node: list/tuple`
            Co-ordinates of goal node.
            
        `show_exp: bool`
            If True, shows the exploration path. If False, directly shows the path from starting node to goal node.
        """
        self._running = False
        self._display = None
        self.show_exp = show_exp
        self.start_node = (start_node[0] * 20, start_node[1] * 20)
        self.goal_node = (goal_node[0] * 20, goal_node[1] * 20)
        self.blocked = list()
        self.colours = {'black' : (0, 0, 0), 'white' : (255, 255, 255), 'green':(0, 255, 0), 'mustard yellow':(255, 208, 0), 'light pink': (255, 122, 251)}
        self.size = self.width, self.height = maze_dim[0] * 20, maze_dim[1] * 20
        
    def on_init(self):
        """
        For initialising data before the display surface is shown and drawing all static elements of the maze.
        """
        self._display = pygame.display.set_mode(self.size, HWSURFACE | DOUBLEBUF)
        
        self.draw_maze()
        
        self._running = True
        pygame.init()
        
    def on_event(self, event):
        """
        For handling all events on the dislpay surface.
        """
        if event.type == QUIT:
            self._running = False
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.find_path()
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.draw_obstacle(pos)
    
    def find_path(self):
        AVAILABLE = AugList(list())
        VISITED = AugList(list())
        currnode = Node(self.start_node, h=math.sqrt((self.start_node[0] - self.goal_node[0])**2 + (self.start_node[1] - self.goal_node[1])**2))
        goal = Node(self.goal_node)
        AVAILABLE.append(currnode)
        
        while len(AVAILABLE) != 0:
            currnode = AVAILABLE[0]
            for node in AVAILABLE:
                if node.f < currnode.f:
                    currnode = node
            
            VISITED.append(currnode)
            
            if currnode.pos == goal.pos:
                path = list()
                while currnode:
                    path.append(currnode.pos)
                    currnode = currnode.parent
                return self.show_path(list(reversed(path)))
            
            children = list()
            for i in [[-20, -20], [-20, 0], [-20, 20], [0, -20], [0, 20], [20, -20], [20, 0], [20, 20]]:
                if currnode.pos[0] + i[0] < 0 or currnode.pos[1] + i[1] < 0 or currnode.pos[0] + i[0] >= self.width or currnode.pos[1] + i[1] >= self.height:
                    continue
                
                if currnode.pos in self.blocked:
                    continue
                
                if i in [[-20, -20], [-20, 20], [20, -20], [20, 20]]:
                    child = Node((currnode.pos[0] + i[0], currnode.pos[1] + i[1]), currnode, 1.414)
                else:
                    child = Node((currnode.pos[0] + i[0], currnode.pos[1] + i[1]), currnode, 1)
                children.append(child)
                
            for child in children:
                if not VISITED.inlist(child)[0]: # heuristic is consistent, so no need to re-visit nodes
                    if not AVAILABLE.inlist(child)[0]:
                        child.g += currnode.g
                        child.f = child.g + math.sqrt((child.pos[0] - goal.pos[0])**2 + (child.pos[1] - goal.pos[1])**2)
                        AVAILABLE.append(child)
                    else:
                        openchild = AVAILABLE[AVAILABLE.inlist(child)[1]] # if the node is already available to visit, we want to check if there is a better path for it
                        if openchild.g > child.g + currnode.g:
                            openchild.g = child.g + currnode.g
                            openchild.f = openchild.g + math.sqrt((child.pos[0] - goal.pos[0])**2 + (child.pos[1] - goal.pos[1])**2)
                            openchild.parent = currnode
                            
            AVAILABLE.remove(currnode)
        
        print('No path found.')
        return
    
    def show_path(self, path):
        if self.show_exp:
            self.draw_maze()
        
        for i in path:
            if i != self.start_node and i != self.goal_node:
                pdraw.rect(self._display, self.colours['light pink'], (i[0] + 1, i[1] + 1, 19, 19))
    
    def draw_maze(self):
        self._display.fill(self.colours['white'])
        
        for i in range(0, self.width + 1, 20):
            pdraw.line(self._display, self.colours['black'], (i, 0), (i, self.height))
        for i in range(0, self.height + 1, 20):
            pdraw.line(self._display, self.colours['black'], (0, i), (self.width, i))
        
        pdraw.rect(self._display, self.colours['mustard yellow'], (self.start_node[0] + 1, self.start_node[1] + 1, 19, 19))
        pdraw.rect(self._display, self.colours['green'], (self.goal_node[0] + 1, self.goal_node[1] + 1, 19, 19))
    
    def draw_obstacle(self, mouse_pos):
        stop = False
        topx, topy = 0, 0
        for i in range(0, self.width - 19, 20):
            for j in range(0, self.height - 19, 20):
                if (mouse_pos[0] >= i and mouse_pos[1] >= j) and (mouse_pos[0] <= i + 20 and mouse_pos[1] <= j + 20) and (i, j) not in self.blocked and (i, j) not in [self.start_node, self.goal_node]:
                    topx, topy = i, j
                    self.blocked.append((i, j))
                    stop = True
                    break
            if stop:
                break
        
        if stop:
            pdraw.rect(self._display, self.colours['black'], (topx, topy, 20, 20))
            print(self.blocked)
    
    def on_loop(self):
        """
        For computing changes in the display surface.
        """
        pass
    
    def on_render(self):
        """
        For rendering the graphics on the display surface.
        """
        pygame.display.update()
    
    def on_cleanup(self):
        """
        For handling all operations to be done before the game loop is broken.
        """
        pygame.quit()
    
    def on_execute(self):
        """
        For handling all operations to be done while executing the program.
        """
        self.on_init()
        
        while self._running:
            for event in pygame.event.get():
                
                self.on_event(event)
                
            self.on_loop()
            self.on_render()
            
        self.on_cleanup()

class TKMainMenu():
    """
    Creates the main menu using tkinter.
    """
    def __init__(self, max_width = 70, max_height = 35):
        """
        Parameter
        ---------
        `max_width: int, optional`
            Defines the maximum width, in terms of cells, allowed for the creation of the maze.
            
        `max_height: int, optional`
            Defines the maximum height, in terms of cells, allowed for the creation of the maze.
        """
        self.main = Tk()
        self.max_width = max_width
        self.max_height = max_height
        self.show_exp = BooleanVar()
        self.title_font = tkfont.Font(family='Times', size=32, weight='bold')
        self.label_font = tkfont.Font(family='Times', size=16)
        self.button_font = tkfont.Font(family='Times', size=13)
        
        self.main.title('Create Maze')
        self.main.geometry('500x410')
        self.main.resizable(False, False)
        self.show_exp.set(False)
        
        self._add_widgets()
        
        self.main.mainloop()
    
    def _add_widgets(self):
        """
        Adds all widgets to the GUI.
        """
        # Label: A* GUI Program
        Label(self.main, text='A* GUI Program', font=self.title_font).grid(row=0, column=0, columnspan=3, ipadx=75, ipady=30)
        # Label: Maze Dimensions
        Label(self.main, text='Maze Dimensions:', font=self.label_font).grid(row=1, column=0, ipadx=30, ipady=10)
        # Entry: for getting maze dimensions
        maze_dim = Entry(self.main, width=40, bd=1, relief=SOLID)
        maze_dim.grid(row=1, column=1, columnspan=2)
        #Label: Start Node:
        Label(self.main, text='Start Node:', font=self.label_font).grid(row=2, column=0, ipady=10)
        #Entry: for getting starting node
        start_node = Entry(self.main, width=40, bd=1, relief=SOLID)
        start_node.grid(row=2, column=1, columnspan=2)
        #Label: Goal Node:
        Label(self.main, text='Goal Node:', font=self.label_font).grid(row=3, column=0, ipady=10)
        #Entry: for getting goal node
        goal_node = Entry(self.main, width=40, bd=1, relief=SOLID)
        goal_node.grid(row=3, column=1, columnspan=2)
        #Label: Show Exploration:
        Label(self.main, text='Show Exploration:', font=self.label_font).grid(row=4, column=0)
        #Radiobutton: configurations for radio buttons
        r1 = Radiobutton(self.main, text='Yes', variable=self.show_exp, value=True)
        r2 = Radiobutton(self.main, text='No', variable=self.show_exp, value=False)
        r1['font'] = r2['font'] = self.label_font
        r1.grid(row=4, column=1)
        r2.grid(row=4, column=2)
        #Button: configuration for button
        button = Button(self.main, text='Create Maze', width=20, bg='white', bd=1, relief=SOLID, 
                        command=lambda: self.check_maze_constraints(maze_dim.get(), start_node.get(), goal_node.get()))
        button['font'] = self.button_font
        button.grid(row=5, column=0, columnspan=3, ipady=5, pady=30)

    def check_maze_constraints(self, maze_dim, start_node, goal_node):
        """
        Checks the maze constraints entered by user to make sure they are vaiid for the creation of the maze. 
        """
        error = [False, '']
        maze_dim = [int(i) for i in maze_dim.split()]
        start_node = [int(i) for i in start_node.split()]
        goal_node = [int(i) for i in goal_node.split()]
        
        if maze_dim[0] > self.max_width or maze_dim[1] > self.max_height:
            error[1] += 'Max maze dimension allowed: 70 35! '
            error[0] = True
        if start_node[0] > maze_dim[0] or start_node[1] > maze_dim[1]:
            error[1] += 'Start node must be within maze dimensions! '
            error[0] = True
        if goal_node[0] > maze_dim[0] or goal_node[1] > maze_dim[1]:
            error[1] += 'Goal node must be within maze dimensions! '
            error[0] = True
        
        if error[0]:
            showwarning("Invalid maze constraints!", error[1])
        else:
            self.main.destroy()
            PygameMaze(maze_dim, start_node, goal_node, self.show_exp.get()).on_execute()

if __name__ == '__main__':
    TKMainMenu()
