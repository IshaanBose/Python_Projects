from pygame.draw import rect
from pygame import mouse
from pygame.font import SysFont
from pygame.font import init
from pygame.locals import MOUSEBUTTONDOWN

init()

class Button():
    def __init__(self, display, msg: str, coord: tuple, dim: tuple, inactive_colour=(255, 255, 255), active_colour=(255, 255, 255), border_inactive=(0, 0, 0), border_active=(0, 0, 0), font=SysFont('sourcesanspro', 23), font_colour=(0, 0, 0), action=None):
        self.display = display
        self.msg = msg
        self.coord = coord
        self.dim = dim
        self.ic = inactive_colour
        self.ac = active_colour
        self.bd_ic = border_inactive
        self.bd_ac = border_active
        self.font = font
        self.font_colour = font_colour
        self.action = action
    
    def draw_button(self):
        mouse_pos = mouse.get_pos()
        msg_txt = self.font.render(self.msg, True, self.font_colour)
        msg_rect = msg_txt.get_rect()
        msg_rect.center = (self.coord[0] + (self.dim[0] // 2), (self.coord[1] + (self.dim[1] // 2)) - 2)
        
        if self.coord[0] + self.dim[0] - 2 >= mouse_pos[0] >= self.coord[0] + 2 and self.coord[1] + self.dim[1] - 2 >= mouse_pos[1] >= self.coord[1] + 2:
            self.draw_active()
        else:
            self.draw_inactive()
        
        self.display.blit(msg_txt, msg_rect)
        
        return self
    
    def draw_active(self):
        rect(self.display, self.bd_ac, (self.coord[0], self.coord[1], self.dim[0], self.dim[1]))
        rect(self.display, self.ac, (self.coord[0] + 2, self.coord[1] + 2, self.dim[0] - 4, self.dim[1] - 4))
    
    def draw_inactive(self):
        rect(self.display, self.bd_ic, (self.coord[0], self.coord[1], self.dim[0], self.dim[1]))
        rect(self.display, self.ic, (self.coord[0] + 2, self.coord[1] + 2, self.dim[0] - 4, self.dim[1] - 4))
    
    def on_event(self, event):
        if self.action:
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = mouse.get_pos()
                if self.coord[0] + self.dim[0] - 2 >= mouse_pos[0] >= self.coord[0] + 2 and self.coord[1] + self.dim[1] - 2 >= mouse_pos[1] >= self.coord[1] + 2:
                    self.action()
                    return True
        return False