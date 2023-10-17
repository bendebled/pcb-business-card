# Note: this implementation is based on the following code
# https://gist.github.com/silvasur/565419
# It was modified in order to work on an ESP32 with an 128*64 oled and with GPIO

# Copyright (c) 2010 "Laria Carolin Chabowski"<me@laria.me>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from random import randrange as rand
import asyncio
import time

cell_size = 2
cols =      15
rows =      30

tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]]
]


def rotate_clockwise(shape):
    return [
        [ shape[y][x] for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1)
    ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1

class Tetris(object):
    def __init__(self, oled, buttons):
        self.oled = oled
        self.buttons = buttons
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.running = False
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = [ [0 for x in range(cols)] for y in range(rows)]
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        self.gameover = False

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    self.oled.fill_rect((off_x+x) * cell_size, (off_y+y) * cell_size, cell_size, cell_size, 1)

    def add_cleared_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*5:
            self.level += 1

    def move(self, delta_x):
        if not self.gameover:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self, manual):
        if not self.gameover:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(
                  self.board,
                  self.stone,
                  (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board):
                        if 0 not in row:
                            self.board = remove_row(
                              self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cleared_lines(cleared_rows)
                return True
        return False

    def rotate_stone(self):
        if not self.gameover:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def stop(self):
        self.running = False

    async def run(self):
        self.running = True

        tick = 0
        last_up = 0
        last_left = 0
        last_right = 0

        while self.running:
            self.oled.fill(0)
            if self.gameover:
                if time.time()%2:
                    self.oled.print_small_text("Game over", 50, 15, 1, 1)
            else:
                self.oled.print_small_text("Next:", 50, 15, 1, 1)
                self.draw_matrix(self.next_stone, (40,8))
            self.oled.print_small_text("Score: {}".format(self.score), 50, 25, 1, 1)
            self.oled.print_small_text("Level: {}".format(self.level), 50, 35, 1, 1)
            self.oled.print_small_text("Lines: {}".format(self.lines), 50, 45, 1, 1)
            
            self.oled.rect(1,1,cols*cell_size+2, rows*cell_size+2,1)
            self.draw_matrix(self.board, (1,1))
            self.draw_matrix(self.stone, (self.stone_x+1, self.stone_y+1))

            self.oled.show()

            if self.buttons.is_left_pressed() and tick - last_left > 1:
                last_left = tick
                self.move(-1)
            if self.buttons.is_right_pressed() and tick - last_right > 1:
                last_right = tick
                self.move(+1)
            if self.buttons.is_up_pressed() and tick - last_up > 2:
                last_up = tick
                self.rotate_stone()
            if self.buttons.is_down_pressed():
                self.drop(True)
            else:    
                if tick % max((4-self.level), 1) == 0:
                    self.drop(False)
            tick += 1
            await asyncio.sleep(0)
