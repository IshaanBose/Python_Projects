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

COLOURS = {'black' : (0, 0, 0), 'white' : (255, 255, 255), 'green':(0, 255, 0), 'red': (255, 0, 0), 'light blue': (145, 231, 255), 
            'dark green': (0, 138, 14), 'dark grey': (235, 235, 235), 'dark red': (176, 0, 0), 'grey': (222, 222, 222), 
            'blue': (0, 174, 255)}
DWIDTH, DHEIGHT = 500, 500
root = Tk()
X = int(root.winfo_screenwidth() * 0.2)
Y = int(root.winfo_screenheight() * 0.2)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X, Y) # to place window at (x, y) position
DISPLAY = pygame.display.set_mode((DWIDTH, DHEIGHT), HWSURFACE | DOUBLEBUF)
pygame.display.set_caption('Tic Tac Toe')
pygame.init()

class StartMenu():
    def __init__(self):
        self._running = False
        self._display = None
    
    def on_init(self):
        self._display = pygame.Surface((DWIDTH, DHEIGHT))
        
        self._running = True
        self.difficulty = {'Easy': True, 'Med': False, 'Hard': False}
        self.mode = {'Single': True, 'Multi': False}
        
        self.draw_menu()
        DISPLAY.blit(self._display, (0, 0))
        pygame.display.update()
    
    def draw_menu(self):
        self._display.fill(COLOURS['white'])
        
        title_font = pygame.font.SysFont('sourcesansprosemibold', 70) # for title
        title = title_font.render('Tic Tac Toe', True, COLOURS['black'])
        title_rect = title.get_rect()
        title_rect.center = (DWIDTH // 2, DHEIGHT // 6)
        
        label_font = pygame.font.SysFont('sourcesanspro', 25)
        difficulty = label_font.render('Difficulty:', True, COLOURS['black'])
        mode = label_font.render('Mode:', True, COLOURS['black'])
        
        rb_font = pygame.font.SysFont('sourcesanspro', 23)
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
        button_font = pygame.font.SysFont('sourcesanspro', 23)
        start_txt = button_font.render('Start', True, COLOURS['black'])
        quit_txt = button_font.render('Quit', True, COLOURS['black'])
        mouse_pos = pygame.mouse.get_pos()
        
        if 198 >= mouse_pos[0] >= 102 and 418 >= mouse_pos[1] >= 382: # start button
            pygame.draw.rect(self._display, COLOURS['green'], (100, 380, 100, 40))
            pygame.draw.rect(self._display, COLOURS['dark grey'], (102, 382, 96, 36))
        else:
            pygame.draw.rect(self._display, COLOURS['dark green'], (100, 380, 100, 40))
            pygame.draw.rect(self._display, COLOURS['grey'], (102, 382, 96, 36))
        
        if 398 >= mouse_pos[0] >= 302 and 418 >= mouse_pos[1] >= 382: # quit button
            pygame.draw.rect(self._display, COLOURS['red'], (300, 380, 100, 40))
            pygame.draw.rect(self._display, COLOURS['dark grey'], (302, 382, 96, 36))
        else:
            pygame.draw.rect(self._display, COLOURS['dark red'], (300, 380, 100, 40))
            pygame.draw.rect(self._display, COLOURS['grey'], (302, 382, 96, 36))
        
        self._display.blit(start_txt, (125, 384))
        self._display.blit(quit_txt, (329, 384))
    
    def draw_radio_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        # Easy
        pygame.draw.circle(self._display, COLOURS['black'], (140, (DHEIGHT // 6) + 128), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (140, (DHEIGHT // 6) + 128), 7)
        if 144.5 >= mouse_pos[0] >= 135.5 and (DHEIGHT // 6) + 131.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 124.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (140, (DHEIGHT // 6) + 128), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (140, (DHEIGHT // 6) + 128), 5)
        # Medium
        pygame.draw.circle(self._display, COLOURS['black'], (225, (DHEIGHT // 6) + 128), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (225, (DHEIGHT // 6) + 128), 7)
        if 229.5 >= mouse_pos[0] >= 220.5 and (DHEIGHT // 6) + 131.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 124.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (225, (DHEIGHT // 6) + 128), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (225, (DHEIGHT // 6) + 128), 5)
        # Hard
        pygame.draw.circle(self._display, COLOURS['black'], (350, (DHEIGHT // 6) + 128), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (350, (DHEIGHT // 6) + 128), 7)
        if 354.5 >= mouse_pos[0] >= 345.5 and (DHEIGHT // 6) + 131.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 124.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (350, (DHEIGHT // 6) + 128), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (350, (DHEIGHT // 6) + 128), 5)
        # Single-Player
        pygame.draw.circle(self._display, COLOURS['black'], (120, (DHEIGHT // 6) + 218), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (120, (DHEIGHT // 6) + 218), 7)
        if 124.5 >= mouse_pos[0] >= 115.5 and (DHEIGHT // 6) + 222.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 213.5:
            pygame.draw.circle(self._display, COLOURS['light blue'], (120, (DHEIGHT // 6) + 218), 5)
        else:
            pygame.draw.circle(self._display, COLOURS['white'], (120, (DHEIGHT // 6) + 218), 5)
        # Multiplayer
        pygame.draw.circle(self._display, COLOURS['black'], (300, (DHEIGHT // 6) + 218), 9)
        pygame.draw.circle(self._display, COLOURS['white'], (300, (DHEIGHT // 6) + 218), 7)
        if 304.5 >= mouse_pos[0] >= 295.5 and (DHEIGHT // 6) + 222.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 213.5:
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
        if event.type == QUIT:
            self._running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if (DHEIGHT // 6) + 131.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 124.5:
                if 144.5 >= mouse_pos[0] >= 135.5 or 229.5 >= mouse_pos[0] >= 220.5 or 354.5 >= mouse_pos[0] >= 345.5:
                    for i in self.difficulty:
                        self.difficulty[i] = False
                    if 144.5 >= mouse_pos[0] >= 135.5:
                        self.difficulty['Easy'] = True
                    elif 229.5 >= mouse_pos[0] >= 220.5:
                        self.difficulty['Med'] = True
                    else:
                        self.difficulty['Hard'] = True
            elif (DHEIGHT // 6) + 222.5 >= mouse_pos[1] >= (DHEIGHT // 6) + 213.5:
                if 124.5 >= mouse_pos[0] >= 115.5 or 304.5 >= mouse_pos[0] >= 295.5:
                    for i in self.mode:
                        self.mode[i] = False
                    if 124.5 >= mouse_pos[0] >= 115.5:
                        self.mode['Single'] = True
                    else:
                        self.mode['Multi'] = True
            elif 198 >= mouse_pos[0] >= 102 and 418 >= mouse_pos[1] >= 382:
                pass
            elif 398 >= mouse_pos[0] >= 302 and 418 >= mouse_pos[1] >= 382:
                self._running = False
    
    def on_cleanup(self):
        pygame.quit()
    
    def on_execute(self):
        self.on_init()
        
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.draw_radio_buttons()
            self.draw_buttons()
            self.set_selected()
            DISPLAY.blit(self._display, (0, 0))
            pygame.display.update()
        self.on_cleanup()