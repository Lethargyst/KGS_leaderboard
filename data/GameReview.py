from PIL import Image, ImageDraw
from copy import deepcopy

SIZES = {19: [45, 72], 13: [70, 40], 9: [105, 25]}
STONES = {'black': 'X', 'white': 'O'}
COLORS = {'X': 'black', 'O': 'white'}


class Reviewer:
    def __init__(self):
        self.size = None
        self.moves = []
        self.iterations = []

    def init_match(self, size, moves):
        self.size = size
        self.moves = moves
        self.evaluate_iterations(size, moves)
        self.render_iteration(0)

    def evaluate_iterations(self, size, moves):
        # Возвращает расположение камней на каждой итерации игры
        self.iterations = [[[' ' for j in range(size)] for i in range(size)]]
        for move in moves:
            if move['loc'] != 'PASS':
                x, y = move['loc']['x'] - 1, move['loc']['y'] - 1
                color = move['color']
                board = self.get_updated_board(self.iterations[-1], x, y, color)
            else:
                board = deepcopy(self.iterations[-1])
            self.iterations.append(board)

    def get_updated_board(self, default_board, x, y, color):
        # Возвращает список новой итерации
        board_copy = deepcopy(default_board)
        board_copy[y][x] = STONES[color]
        for row in range(self.size):
            for col in range(self.size):
                self.kill_surrounded_stones(row, col, board_copy)

        return board_copy

    def kill_surrounded_stones(self, row, col, board):
        # Уничтожает камни, окруженные камнями противника
        checked = set()
        if self.is_surrounded(row, col, checked, board):
            for i, j in checked:
                board[i][j] = ' '

    def is_surrounded(self, row, col, checked, board):
        # Рекурсивная функция, проверяющая, окружен ли камень
        checked.add((row, col))
        if board[row][col] == ' ':
            return False

        res = []
        for i, j in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            i, j = row + i, col + j
            if not (self.outside_the_field(i, j)):
                if board[i][j] == ' ':
                    return False
                elif board[i][j] == board[row][col] and (i, j) not in checked:
                    res.append(self.is_surrounded(i, j, checked, board))

        if all(node for node in res):
            return True
        return False

    def outside_the_field(self, row, col):
        return not (0 <= row < self.size and 0 <= col < self.size)

    def render_iteration(self, iteration):
        # Рисует игровую доску на данной итерации
        board = self.iterations[iteration]
        img = Image.new('RGBA', (1000, 1000), '#dfbd6d')
        idraw = ImageDraw.Draw(img)
        node_size, padding = SIZES[self.size]
        stone_size = node_size * 0.75
        for row in range(self.size):
            for col in range(self.size):
                idraw.rectangle((padding + node_size * col,
                                 padding + node_size * row,
                                 padding + node_size * (col + 1),
                                 padding + node_size * (row + 1)), outline='#a78a48', width=2)

                if board[row][col] != ' ':
                    idraw.ellipse((padding + node_size * col - stone_size // 2,
                                   padding + node_size * row - stone_size // 2,
                                   padding + node_size * col + stone_size // 2,
                                   padding + node_size * row + stone_size // 2),
                                  fill=COLORS[board[row][col]])

        img.save('static/img/board.png')

