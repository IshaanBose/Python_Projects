"""
A* GUI Program
==============

This is a program that implements the A* path finding algorithm using GUI.

Input is to be given in the form of 'x y'. Input for 'Maze Dimensions' is given in terms of cells, not pixels. Checking 'Yes' for 
'Show Exploration' will show the exploration path of the algorithm. Due to the amount of changes being made to the GUI, this will cause 
the program to work slower than if 'Show Exploration' was checked as 'No'.

Once at the maze GUI, you can click on the cells to create/remove obstacles. Once you have added/deleted the desired amount of obstacles, 
you press the `RETURN` key to start the execution of the program. Pressing `Space` will clear the maze of any obstacles and paths. 
Pressing `Ctrl+Space` will clear only paths while keeping obstacles. Closing the maze screen allows you to go back to the maze creation screen.
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
from _datastructs import *
import path_finding as pf

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
        self.colours = {'black' : (0, 0, 0), 'white' : (255, 255, 255), 'green':(0, 255, 0), 'mustard yellow':(255, 208, 0),
                        'light pink': (255, 122, 251), 'red': (255, 0, 0), 'dark blue': (2, 68, 173)}
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
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                pf.astar_path(self)
            elif event.key == K_SPACE and pygame.key.get_mods() & KMOD_CTRL:
                self.draw_maze()
                self.redraw_obstacles()
            elif event.key == K_SPACE:
                self.blocked.clear()
                self.draw_maze()
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.modify_obstacle(pos)
    
    def pump_events(self):
        """
        This function gives event control to OS to prevent application crashing while it's showing exploration.
        """
        for event in pygame.event.get(): # to make sure app doesn't crash and that no events are pushed into event queue during execution of A*
                pygame.event.pump()
    
    def tk_popup(self, title, message):
        """"
        This function is used to bring up a popup window using Tkinter.
        """
        temp = Tk()
        temp.geometry('0x0')
        showwarning(title, message)
        temp.destroy()
    
    def render_exploration(self, point, rtype):
        """
        This function is used to show how nodes are explored when A* runs.
        """
        if rtype == 'visited':
            pdraw.rect(self._display, self.colours['red'], (point[0] + 1, point[1] + 1, 19, 19))
        elif rtype == 'available':
            pdraw.rect(self._display, self.colours['green'], (point[0] + 1, point[1] + 1, 19, 19))
        
        pygame.time.wait(100)
        pygame.display.update()
    
    def show_path(self, path):
        """
        This function is used to show the final path from the start node to goal node.
        """
        if self.show_exp:
            pygame.time.wait(1000) # giving time for user to look at finished exploration, time is given in ms
            self.draw_maze()
            self.redraw_obstacles()
        
        for i in path:
            if i != self.start_node and i != self.goal_node:
                pdraw.rect(self._display, self.colours['light pink'], (i[0] + 1, i[1] + 1, 19, 19))
    
    def draw_maze(self):
        """
        This function is used to draw/redraw the maze.
        """
        self._display.fill(self.colours['white'])
        
        for i in range(0, self.width + 1, 20):
            pdraw.line(self._display, self.colours['black'], (i, 0), (i, self.height))
        for i in range(0, self.height + 1, 20):
            pdraw.line(self._display, self.colours['black'], (0, i), (self.width, i))
        
        pdraw.rect(self._display, self.colours['mustard yellow'], (self.start_node[0] + 1, self.start_node[1] + 1, 19, 19)) # start node
        pdraw.rect(self._display, self.colours['dark blue'], (self.goal_node[0] + 1, self.goal_node[1] + 1, 19, 19)) # goal node
    
    def redraw_obstacles(self):
        """
        This function is used to redraw the obstacles after redrawing the maze.
        """
        for i in self.blocked:
            pdraw.rect(self._display, self.colours['black'], (i[0], i[1], 20, 20))
    
    def modify_obstacle(self, mouse_pos):
        """
        This function is used to draw/remove an obstacle on the square the user clicks on.
        """
        for i in range(0, self.width - 19, 20):
            for j in range(0, self.height - 19, 20):
                if (mouse_pos[0] >= i and mouse_pos[1] >= j) and (mouse_pos[0] <= i + 20 and mouse_pos[1] <= j + 20) and (i, j) not in [self.start_node, self.goal_node]:
                    if (i, j) not in self.blocked:
                        self.blocked.append((i, j))
                        pdraw.rect(self._display, self.colours['black'], (i, j, 20, 20))
                        return
                    else:
                        self.blocked.remove((i, j))
                        pdraw.rect(self._display, self.colours['white'], (i + 1, j + 1, 19, 19))
                        return
    
    def on_cleanup(self):
        """
        For handling all operations to be done before the game loop is broken.
        """
        pygame.quit()
        del self # deletes current instance of of the maze
        TKMainMenu()
    
    def on_execute(self):
        """
        For handling all operations to be done while executing the program.
        """
        self.on_init()
        
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            pygame.display.update()
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
        if start_node[0] >= maze_dim[0] or start_node[1] >= maze_dim[1] or start_node[0] < 0 or start_node[1] < 0:
            error[1] += 'Start node must be within maze dimensions! '
            error[0] = True
        if goal_node[0] >= maze_dim[0] or goal_node[1] >= maze_dim[1] or goal_node[0] < 0 or goal_node[1] < 0:
            error[1] += 'Goal node must be within maze dimensions! '
            error[0] = True
        
        if error[0]:
            showwarning("Invalid maze constraints!", error[1])
        else:
            self.main.destroy()
            PygameMaze(maze_dim, start_node, goal_node, self.show_exp.get()).on_execute()