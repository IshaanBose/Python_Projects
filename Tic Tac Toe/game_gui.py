try:
    import pygame
    from pygame.locals import *
except ModuleNotFoundError:
    print('pygame module not installed. Run: %installdir%python.exe -m pip install -U pygame --user')
    quit()
try:
    from tkinter import Tk
except ModuleNotFoundError:
    print('tkinter module not installed. Refer: https://tkdocs.com/tutorial/install.html')
    quit()
import os
from game_logic import GameLogic
from pygame_button_element import Button

_ROOT = Tk()
COLOURS = {'black' : (0, 0, 0), 'white' : (255, 255, 255), 'green':(0, 255, 0), 'red': (255, 0, 0), 'light blue': (145, 231, 255), 
            'dark green': (0, 138, 14), 'dark grey': (235, 235, 235), 'dark red': (176, 0, 0), 'grey': (222, 222, 222), 
            'blue': (0, 174, 255)}
DWIDTH, DHEIGHT = 500, 500
X = int(_ROOT.winfo_screenwidth() * 0.2)
Y = int(_ROOT.winfo_screenheight() * 0.2)
DISPLAY = pygame.display.set_mode((DWIDTH, DHEIGHT), HWSURFACE | DOUBLEBUF)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X, Y) # to place window at (x, y) position
pygame.display.set_caption('Tic Tac Toe')
pygame.init()

class MainLoop():
    def __init__(self):
        self._running = False
        self.curr_frame = None
    
    def on_cleanup(self):
        pygame.quit()
    
    def on_execute(self):
        self._running = True
        self.curr_frame = StartMenu(self)
        
        while self._running:
            for event in pygame.event.get():
                self.curr_frame.on_event(event)
            if type(self.curr_frame) == StartMenu:
                self.curr_frame.draw_buttons()
                self.curr_frame.draw_radio_buttons()
                self.curr_frame.set_selected()
            DISPLAY.blit(self.curr_frame._display, (0, 0))
            pygame.display.update()
        self.on_cleanup()

class StartMenu():
    def __init__(self, main_loop: MainLoop):
        self.main_loop = main_loop
        self.main_loop.curr_frame = self
        self._display = None
        self.start_btn = None
        self.quit_btn = None
        
        self.on_init()
    
    def on_init(self):
        self._display = pygame.Surface((DWIDTH, DHEIGHT))
        
        self._running = True
        self.difficulty = {'Easy': True, 'Med': False, 'Hard': False}
        self.mode = {'Single': True, 'Multi': False}
        self.start_btn = Button(self._display, 'Start', (100, 380), (100, 40), COLOURS['grey'], COLOURS['dark grey'], COLOURS['dark green'], COLOURS['green'], action=self.start)
        self.quit_btn = Button(self._display, 'Quit', (300, 380), (100, 40), COLOURS['grey'], COLOURS['dark grey'], COLOURS['dark red'], COLOURS['red'], action=self.quit_fnt)
        
        self.draw_static_elements()
        DISPLAY.blit(self._display, (0, 0))
        pygame.display.update()
    
    def draw_static_elements(self):
        self._display.fill(COLOURS['white'])
        
        title_font = pygame.font.SysFont('sourcesansprosemibold', 70) # for title
        title = title_font.render('Tic Tac Toe', True, COLOURS['black'])
        title_rect = title.get_rect()
        title_rect.center = (DWIDTH // 2, DHEIGHT // 6)
        
        label_font = pygame.font.SysFont('sourcesanspro', 25) # for the labels
        difficulty = label_font.render('Difficulty:', True, COLOURS['black'])
        mode = label_font.render('Mode:', True, COLOURS['black'])
        
        rb_font = pygame.font.SysFont('sourcesanspro', 23) # for radiobutton labels
        easy_diff = rb_font.render('Easy', True, COLOURS['black'])
        med_diff = rb_font.render('Medium', True, COLOURS['black'])
        hard_diff = rb_font.render('Hard', True, COLOURS['black'])
        single_pl = rb_font.render('Single-Player', True, COLOURS['black'])
        multi_pl = rb_font.render('Multiplayer', True, COLOURS['black'])
        
        self._display.blit(title, title_rect)
        self._display.blit(difficulty, (20, (DHEIGHT // 6) + 110))
        self._display.blit(mode, (20, (DHEIGHT // 6) + 200))
        self._display.blit(easy_diff, (152, (DHEIGHT // 6) + 112))
        self._display.blit(med_diff, (238, (DHEIGHT // 6) + 112))
        self._display.blit(hard_diff, (365, (DHEIGHT // 6) + 112))
        self._display.blit(single_pl, (135, (DHEIGHT // 6) + 202))
        self._display.blit(multi_pl, (315, (DHEIGHT // 6) + 202))
    
    def draw_buttons(self):
        self.start_btn.draw_button()
        self.quit_btn.draw_button()
    
    def draw_radio_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        # Easy
        pygame.draw.circle(self._display, COLOURS['black'], (140, (DHEIGHT // 6) + 128), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (140, (DHEIGHT // 6) + 128), 7)
        if 146.5 >= mouse_pos[0] >= 133.5 and (DHEIGHT // 6) + 133.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 122.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (140, (DHEIGHT // 6) + 128), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (140, (DHEIGHT // 6) + 128), 5)
        # Medium
        pygame.draw.circle(self._display, COLOURS['black'], (225, (DHEIGHT // 6) + 128), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (225, (DHEIGHT // 6) + 128), 7)
        if 231.5 >= mouse_pos[0] >= 218.5 and (DHEIGHT // 6) + 133.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 122.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (225, (DHEIGHT // 6) + 128), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (225, (DHEIGHT // 6) + 128), 5)
        # Hard
        pygame.draw.circle(self._display, COLOURS['black'], (350, (DHEIGHT // 6) + 128), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (350, (DHEIGHT // 6) + 128), 7)
        if 356.5 >= mouse_pos[0] >= 343.5 and (DHEIGHT // 6) + 133.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 122.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (350, (DHEIGHT // 6) + 128), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (350, (DHEIGHT // 6) + 128), 5)
        # Single-Player
        pygame.draw.circle(self._display, COLOURS['black'], (120, (DHEIGHT // 6) + 218), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (120, (DHEIGHT // 6) + 218), 7)
        if 126.5 >= mouse_pos[0] >= 113.5 and (DHEIGHT // 6) + 224.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 211.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (120, (DHEIGHT // 6) + 218), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (120, (DHEIGHT // 6) + 218), 5)
        # Multiplayer
        pygame.draw.circle(self._display, COLOURS['black'], (300, (DHEIGHT // 6) + 218), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (300, (DHEIGHT // 6) + 218), 7)
        if 306.5 >= mouse_pos[0] >= 293.5 and (DHEIGHT // 6) + 224.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 211.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (300, (DHEIGHT // 6) + 218), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (300, (DHEIGHT // 6) + 218), 5)
    
    def set_selected(self):
        if self.difficulty['Easy']:
            pygame.draw.circle(self._display, COLOURS['blue'], (140, (DHEIGHT // 6) + 128), 5)
        elif self.difficulty['Med']:
            pygame.draw.circle(self._display, COLOURS['blue'], (225, (DHEIGHT // 6) + 128), 5)
        elif self.difficulty['Hard']:
            pygame.draw.circle(self._display, COLOURS['blue'], (350, (DHEIGHT // 6) + 128), 5)
        
        if self.mode['Single']:
            pygame.draw.circle(self._display, COLOURS['blue'], (120, (DHEIGHT // 6) + 218), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['blue'], (300, (DHEIGHT // 6) + 218), 5)
    
    def on_event(self, event):
        if self.start_btn.on_event(event):
            return
        elif self.quit_btn.on_event(event):
            return
        elif event.type == QUIT:
            self.main_loop._running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if (DHEIGHT // 6) + 133.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 122.5:
                if 146.5 >= mouse_pos[0] >= 133.5 or 231.5 >= mouse_pos[0] >= 218.5 or 356.5 >= mouse_pos[0] >= 343.5:
                    for i in self.difficulty:
                        self.difficulty[i] = False
                    if 146.5 >= mouse_pos[0] >= 133.5:
                        self.difficulty['Easy'] = True
                    elif 231.5 >= mouse_pos[0] >= 218.5:
                        self.difficulty['Med'] = True
                    else:
                        self.difficulty['Hard'] = True
            elif (DHEIGHT // 6) + 224.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 211.5:
                if 126.5 >= mouse_pos[0] >= 113.5 or 306.5 >= mouse_pos[0] >= 293.5:
                    for i in self.mode:
                        self.mode[i] = False
                    if 126.5 >= mouse_pos[0] >= 113.5:
                        self.mode['Single'] = True
                    else:
                        self.mode['Multi'] = True
    
    def start(self):
        difficulty, mode = None, None
        for i in self.difficulty.keys():
            if self.difficulty[i]:
                difficulty = i
        for i in self.mode.keys():
            if self.mode[i]:
                mode = i
        
        GameBoard(self.main_loop, difficulty, mode)
    
    def quit_fnt(self):
        self.main_loop._running = False

class MultiOptionPopup():
    def __init__(self, main_loop: MainLoop):
        self._display = None
        self.main_loop = main_loop
    
    def on_init(self):
        self._display = pygame.Surface((DWIDTH, DHEIGHT))
        
        self.draw_static_elements()
        
        DISPLAY.blit(self._display, (0, 0))
        pygame.display.update()
    
    def draw_static_elements(self):
        self._display.fill(COLOURS['white'])

class GameBoard():
    def __init__(self, main_loop: MainLoop, difficulty, mode):
        self._display = None
        self.main_loop = main_loop
        self.main_loop.curr_frame = self
        self.difficulty = difficulty
        self.mode = mode
        # if self.mode == 'Single':
            
        self.game_logic = GameLogic(self, mode, difficulty)
        self.board = [['', '', ''],
                    ['', '', ''],
                    ['', '', '']]
        
        self.on_init()
    
    def on_init(self):
        self._display = pygame.Surface((DWIDTH, DHEIGHT))
        
        self.draw_static_elements()
        DISPLAY.blit(self._display, (0, 0))
        pygame.display.update()
    
    def on_event(self, event):
        if event.type == QUIT:
            self.main_loop._running = False
        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                StartMenu(self.main_loop)
        elif event.type == MOUSEBUTTONDOWN:
            if self.game_logic.turns <= 8 and not self.game_logic.check_win_state():
                mouse_pos = pygame.mouse.get_pos()
                x, y, index1, index2 = 0, 0, 0, 0
                
                while index1 != 3:
                    if x + 164 >= mouse_pos[0] >= x and y + 164 >= mouse_pos[1] >= y:
                        if self.board[index1][index2] == '':
                            self.place_at(index1, index2, x, y, True)
                            
                            if self.mode == 'Single':
                                self.game_logic.run()
                            break
                    if x + 168 == 504:
                        x = 0
                        y += 168
                        index2 = 0
                        index1 += 1
                    else:
                        x += 168
                        index2 += 1
    
    def place_at(self, index1, index2, x=0, y=0, setxy=False):
        action_font = pygame.font.SysFont('sourcesanspro', 100)
        i, j = 0, 0
        
        while i != 3:
            if (i == index1 and j == index2) or setxy:
                action = action_font.render(self.game_logic.turn, True, COLOURS['black'])
                action_rect = action.get_rect()
                action_rect.center = (x + 164 // 2, y + 164 // 2)
                self._display.blit(action, action_rect)
                self.board[index1][index2] = self.game_logic.turn
                
                if self.game_logic.turns >= 4:
                    if self.game_logic.check_win_state():
                        print(self.game_logic.turn, 'wins!')
                        return
                    if self.game_logic.turns == 8:
                        print('Tie!')
                        return
                
                self.game_logic.next_turn()
                return
            if x + 168 == 504:
                x = 0
                y += 168
                j = 0
                i += 1
            else:
                x += 168
                j += 1
    
    def draw_static_elements(self):
        self._display.fill(COLOURS['white'])
        
        pygame.draw.line(self._display, COLOURS['black'], (164, 0), (164, DHEIGHT), width=4)
        pygame.draw.line(self._display, COLOURS['black'], (332, 0), (332, DHEIGHT), width=4)
        pygame.draw.line(self._display, COLOURS['black'], (0, 164), (DWIDTH, 164), width=4)
        pygame.draw.line(self._display, COLOURS['black'], (0, 332), (DWIDTH, 332), width=4)