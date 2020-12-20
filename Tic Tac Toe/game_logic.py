from random import randint

class Player():
    def __init__(self, name, action, cpu=False):
        self.name = name
        self.action = action
        self.cpu = cpu

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
        self.turns += 1
    
    def check_win_state(self):
        rcount, ccount, ldcount, rdcount = 0, 0, 0, 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.gui.board[i][j] == self.turn:
                    rcount += 1
                if self.gui.board[j][i] == self.turn:
                    ccount += 1
                if (i + j) == 2 and self.gui.board[i][j] == self.turn:
                    rdcount += 1
                    if i == j:
                        ldcount += 1
                    continue
                if (i + j) % 2 == 0 and self.gui.board[i][j] == self.turn:
                    ldcount += 1
            if rcount == 3 or ccount == 3 or ldcount == 3 or rdcount == 3:
                return True
            rcount, ccount = 0, 0
        return False
    
    def run(self):
        while self.turns != 8:
            index1, index2 = randint(0, 2), randint(0, 2)
            if self.gui.board[index1][index2] == '':
                self.gui.place_at(index1, index2)
                return