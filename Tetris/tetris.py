class Piece:
    pieces = {'_': [[-1, -1, -1, -1]],
              'O': [[4, 14, 15, 5]],
              'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
              'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
              'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
              'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
              'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
              'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}

    def __new__(cls, *args, **kwargs):
        assert (args[0] in cls.pieces), "Invalid piece type/letter"
        return object.__new__(cls)

    def __init__(self, piece_type, dimension: tuple = (10, 20)):
        self.piece_type = piece_type
        self.shapes = self.pieces[self.piece_type]
        self.position_matrix = self.shapes[0]
        self.x, self.y, self.r = 0, 0, 0
        self.m, self.n = dimension
        self.lock = False

    def __repr__(self):
        return f'Piece(piece_type={self.piece_type}, position={self.position_matrix})'

    def update_position(self):
        # if not self.lock:
        self.position_matrix = self.shapes[self.r % len(self.shapes)]

        bottom_side = max(e // self.m for e in self.position_matrix)
        self.y = min(self.y, self.n - bottom_side - 1)

        left_side = min(e % self.m for e in self.position_matrix)
        right_side = max(e % self.m for e in self.position_matrix)
        self.x = - min(abs(self.x), left_side) if self.x < 0 else min(self.x, self.m - right_side - 1)

        self.position_matrix = list(map(self.transform_func, self.position_matrix))

        if self.y == self.n - bottom_side - 1:
            self.lock = True

    def transform_func(self, e):
        return e + (self.y * self.m) + ((e + self.x) % self.m) - (e % self.m)


class Grid:

    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.size = width * height
        self.main_grid = ['-'] * self.size
        self.temp_grid = []

    def __repr__(self):
        return f'Grid(width={self.width}, height={self.height}'

    def clear(self):
        self.main_grid = ['-'] * self.size

    def line_break(self):
        while all(x == '0' for x in self.main_grid[-self.width:]):
            self.main_grid = ['-'] * self.width + self.main_grid[:-self.width]


class Game:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.grid: Grid = Grid(m, n)
        self.piece: Piece = Piece('_', dimension=(m, n))

    def line_break(self):
        self.piece = Piece("_", (self.m, self.n))
        self.grid.line_break()
        self.render()

    def piece_collision(self):
        # print([self.grid.main_grid[i] for i in self.piece.position_matrix])
        return '0' in [self.grid.main_grid[i] for i in self.piece.position_matrix]

    def render(self):

        self.grid.temp_grid = ['0' if i in self.piece.position_matrix else self.grid.main_grid[i]
                               for i in range(0, self.grid.size)]

        if self.piece.lock:
            self.grid.main_grid = self.grid.temp_grid[:]

        for i in range(0, self.grid.size, self.grid.width):
            print(" ".join(self.grid.temp_grid[i:i + self.grid.width]))
        print()

    def new_piece(self, piece_type: str):
        self.piece = Piece(piece_type, (self.m, self.n))
        self.render()

    def undo_move(self, direction):
        if direction in ['rotate', 'r']:
            self.piece.r -= 1
        elif direction in ['down', 's']:
            pass
        elif direction in ['left', 'a']:
            self.piece.x += 1
        elif direction in ['right', 'd']:
            self.piece.x -= 1

    def move_piece(self, direction):
        if self.piece.lock:
            if any(x < 10 for x in self.piece.position_matrix):
                return False
        else:
            if direction in ['rotate', 'r']:
                self.piece.r += 1
            elif direction in ['down', 's']:
                pass
            elif direction in ['left', 'a']:
                self.piece.x -= 1
            elif direction in ['right', 'd']:
                self.piece.x += 1
            else:
                print("Invalid Input, Try again: ")
                return True
            self.piece.update_position()
            if self.piece_collision():
                self.undo_move(direction)
            self.piece.y += 1
            self.piece.update_position()
            if self.piece_collision():
                self.piece.y -= 1
                self.piece.update_position()
                self.piece.lock = True
                if any(x < 10 for x in self.piece.position_matrix):
                    return False
        self.render()
        return True


def main():
    d = input().split()
    m, n = int(d[0]), int(d[1])

    game = Game(m, n)
    game.render()

    while True:
        action = input()
        if action in ['exit', 'q']:
            break
        elif action in ['piece', 'p']:
            piece_type = input()
            game.new_piece(piece_type)
            if game.piece_collision():
                print('Game Over!')
                break
        elif action in ['break', 'b']:
            game.line_break()
        else:
            if not game.move_piece(action):
                game.render()
                print('Game Over!')
                break


def test():
    pass


if __name__ == '__main__':
    main()
    # test()
