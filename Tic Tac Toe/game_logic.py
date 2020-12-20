from random import randint

class GameLogic():
    def __init__(self, gui, mode, difficulty):
        self.gui = gui
        self.mode = mode
        self.difficulty = difficulty
        self.turn = 'X'
        self.turns = 0
    
    def next_turn(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'
    
    def check_win_state(self):
        pass
    
    def run(self):
        while True:
            index1, index2 = randint(0, 2), randint(0, 2)
            if self.gui.board[index1][index2] == '':
                self.gui.place_at(index1, index2)
                self.turns += 1
                return