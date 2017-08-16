import socket
import cPickle
import random
import time
from board import Board


class SocketServer(object):
    def __init__(self, hostname=socket.gethostname(), my_port=80):
        self.hostname = hostname
        self.my_port = my_port
        self._create_socket()

    def _create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.hostname, self.my_port))
        self.server_socket.listen(2)

    def get_client_connection(self):
        conn, address = self.server_socket.accept()
        print 'connected to ' + address[0]
        return conn, address

    @staticmethod
    def get_data_from_client(conn):
        data = conn.recv(1024)
        return data

    @staticmethod
    def send_data_to_client(conn, message, demand_answer=False):
        data = cPickle.dumps((demand_answer, message), -1)
        time.sleep(0.1)  # without waiting the client cant always keep up
        conn.sendall(data)

    def send_question_get_response(self, conn, message):
        self.send_data_to_client(conn, message, demand_answer=True)
        answer = self.get_data_from_client(conn).strip()
        return answer


class Player(object):
    def __init__(self, num, name, conn, address, sign):
        self.num = num
        self.name = name
        self.conn = conn
        self.ip = address[0]
        self.port = address[1]
        self.sign = sign


class ServerGame(SocketServer):
    _NUMBER_OF_PLAYERS = 2

    def __init__(self, hostname=socket.gethostname(), my_port=80):
        super(ServerGame, self).__init__(hostname, my_port)
        self.board = Board()
        self.players = []
        self._current_player_num = random.randint(0, self._NUMBER_OF_PLAYERS - 1)
        self._load_players()

    def _load_players(self):
        signs = []
        for i in xrange(self._NUMBER_OF_PLAYERS):
            print 'waiting for connections'
            conn, address = self.get_client_connection()
            name = self.send_question_get_response(conn, 'what is your name?')
            sign = self.send_question_get_response(conn, 'choose your sign')
            while sign in signs:
                sign = self.send_question_get_response(conn, 'Sign in use. Please choose another sign')
            player = Player(i + 1, name, conn, address, sign)
            self.players.append(player)
            self.send_data_to_client(conn, 'waiting for all connections')

    @property
    def _next_player_num(self):
        return (self._current_player_num + 1) % self._NUMBER_OF_PLAYERS

    @property
    def _next_player(self):
        return self.players[self._next_player_num]

    @property
    def _current_player(self):
        return self.players[self._current_player_num]

    def _get_col_num(self):
        col_num = None
        valid = False
        while not valid:
            col_num = self.send_question_get_response(self._current_player.conn, 'Please insert valid Row Num [1-7]:')
            if col_num.isdigit() and 1 <= int(col_num) <= 7:
                valid = True
        return int(col_num) - 1

    def tell_all_players(self, message):
        for player in self.players:
            self.send_data_to_client(player.conn, message)

    def _turn_logic(self):
        self.tell_all_players('Its %s\'s turn!\n' % self._current_player.name)
        col = self._get_col_num()
        while not self.board.enter_value(col, self._current_player.sign):
            self.send_data_to_client(self._current_player.conn, 'This column is full')
            col = self._get_col_num()

    def _print_board(self):
        self.tell_all_players('\n' + str(self.board) + '\n')

    def _announce_winner(self, winner):
        self.tell_all_players('The winner is: %s!!!' % winner.name)

    def _close_connections(self):
        for player in self.players:
            self.send_data_to_client(player.conn, 'FIN')
            player.conn.close()
        self.server_socket.close()

    def play(self):
        last_player = None
        self._print_board()
        while not self.board.check_win():
            self._turn_logic()
            self._print_board()
            last_player = self._current_player_num
            self._current_player_num = self._next_player_num
        winner = self.players[last_player]
        self._announce_winner(winner)
        self._close_connections()


if __name__ == '__main__':
    ServerGame().play()
