__author__ = 'Shelly'


class Cell(object):
    def __init__(self, row_index, col_index, value):
        self.x = row_index
        self.y = col_index
        self.value = value


class Board(object):
    _EMPTY_CELL_VALUE = None
    _WINNING_SEQ = 4

    def __init__(self, width=7, height=6):
        self.width = width
        self.height = height
        self.board = self._create_board()

    def _create_board(self):
        return [[Cell(i, j, self._EMPTY_CELL_VALUE) for i in xrange(self.width)] for j in xrange(self.height)]

    def enter_value(self, col_index, value):
        for row_index in range(self.height)[::-1]:
            if not self.board[row_index][col_index].value:
                self.board[row_index][col_index].value = value
                return True
        return False

    def _get_rows(self):
        return [row[i:i + self._WINNING_SEQ] for row in self.board for i in xrange(len(row) - (self._WINNING_SEQ - 1))]

    def _get_columns(self):
        return [[self.board[row_index + i][col_index] for i in xrange(self._WINNING_SEQ)]
                for row_index in xrange(self.height - (self._WINNING_SEQ - 1))
                for col_index in xrange(self.width)]

    def _get_diagonals(self):
        return [[self.board[row_index + i][col_index + i] for i in xrange(self._WINNING_SEQ)]
                for row_index in xrange(self.height - (self._WINNING_SEQ - 1))
                for col_index in xrange(self.width - (self._WINNING_SEQ - 1))] + \
               [[self.board[row_index + i][col_index - i] for i in xrange(self._WINNING_SEQ)]
                for row_index in xrange(self.height - (self._WINNING_SEQ - 1))
                for col_index in range(self._WINNING_SEQ - 1, self.width)]

    def _get_all_sequences(self):
        return self._get_rows() + self._get_columns() + self._get_diagonals()

    @staticmethod
    def _is_win_sequence(seq):
        seq_set = set(map(lambda cell: cell.value, seq))
        return len(seq_set) == 1 and seq_set.pop() is not None

    def check_win(self):
        return any(map(self._is_win_sequence, self._get_all_sequences()))

    def __repr__(self):
        return "\n".join(['|'.join(map(lambda cell: cell.value or '_', row)) for row in self.board])
