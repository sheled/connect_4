import socket
import cPickle


class SocketClient(object):
    def __init__(self, remote_hostname, remote_port):
        self.remote_hostname = remote_hostname
        self.remote_port = remote_port
        self._create_socket()

    def _create_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        remote_ip = socket.gethostbyname(self.remote_hostname)
        self.client_socket.connect((remote_ip, self.remote_port))

    def send_message(self, message='', get_input_from_user=False):
        """
        A message must be given unless "get_input_from_user is True
        """
        if get_input_from_user:
                message = raw_input('reply: ')
        self.client_socket.sendall(message)

    def receive_message(self):
        reply = self.client_socket.recv(2048)
        return cPickle.loads(reply)

    def _close_connection(self):
        self.client_socket.close()


class ClientGame(SocketClient):
    def __init__(self, remote_hostname, remote_port):
        super(ClientGame, self).__init__(remote_hostname, remote_port)

    def _turns_logic(self):
        (to_answer, message) = self.receive_message()
        while message != 'FIN':
            print message
            if to_answer:
                self.send_message(get_input_from_user=True)
            (to_answer, message) = self.receive_message()

    def play(self):
        self.connect_to_server()
        self._turns_logic()
        self._close_connection()

if __name__ == '__main__':
        ClientGame(socket.gethostname(), 80).play()
