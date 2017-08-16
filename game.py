from board import Board


class Game(object):
    def __init__(self, value1='X', value2='O'):
        if value1 == value2:
            raise TypeError("Values cannot be the same")
        self._value1 = self._current_value = value1
        self._value2 = value2
        self.board = Board()

    @property
    def _next_value(self):
        return self._value1 if self._current_value == self._value2 else self._value2

    @staticmethod
    def _get_col_num():
        col_num = None
        valid = False
        while not valid:
            col_num = raw_input("Insert valid Row Num [1-7]: ").strip()
            if col_num.isdigit() and 1 <= int(col_num) <= 7:
                valid = True
        return int(col_num) - 1

    def _turn_logic(self):
        col = self._get_col_num()
        while not self.board.enter_value(col, self._current_value):
            print 'This column is full'
            col = self._get_col_num()

    def _print_board(self):
        print
        print self.board
        print

    def run(self):
        while not self.board.check_win():
            self._turn_logic()
            self._print_board()
            self._current_value = self._next_value

    @classmethod
    def play(cls, value1='X', value2='O'):
        game = cls(value1, value2)
        game.run()

Game.play()
