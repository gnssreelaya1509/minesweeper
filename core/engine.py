import random

class MinesweeperEngine:
    def __init__(self, rows=10, cols=10, num_mines=12):
        self.rows, self.cols, self.num_mines = rows, cols, num_mines
        self.reset()

    def reset(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.visible = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = self.win = self.mines_placed = False

    def place_mines(self, safe_r, safe_c):
        placed = 0
        while placed < self.num_mines:
            r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if self.board[r][c] != -1 and not (r == safe_r and c == safe_c):
                self.board[r][c] = -1
                placed += 1
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1: continue
                count = 0
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        nr, nc = r+dr, c+dc
                        if 0<=nr<self.rows and 0<=nc<self.cols and self.board[nr][nc] == -1: count += 1
                self.board[r][c] = count
        self.mines_placed = True

    def reveal(self, r, c):
        if self.game_over or self.win or self.flags[r][c] or self.visible[r][c]: return
        if not self.mines_placed: self.place_mines(r, c)
        self.visible[r][c] = True
        if self.board[r][c] == -1: self.game_over = True
        elif self.board[r][c] == 0:
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr, nc = r+dr, c+dc
                    if 0<=nr<self.rows and 0<=nc<self.cols: self.reveal(nr, nc)
        self.check_win()

    def toggle_flag(self, r, c):
        if not self.visible[r][c]: self.flags[r][c] = not self.flags[r][c]

    def check_win(self):
        if sum(row.count(False) for row in self.visible) == self.num_mines: self.win = True