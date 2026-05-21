import socket
import threading

from client import ChatClient


class SpamClient(ChatClient):
    def __init__(self, host: str = '127.0.0.1', port: int = 5555,
                 num_messages: int = 300) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.name = 'SPAM_BOT'
        self.sock.send(self.name.encode())
        self.running = True
        self.num_messages = num_messages

        self.receiver = threading.Thread(target=self._receive, daemon=True)
        self.receiver.start()

        self._spam()

    def _receive(self) -> None:
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
            except (ConnectionResetError, BrokenPipeError, OSError):
                break
        self.running = False

    def _spam(self) -> None:
        try:
            sent = 0
            for i in range(self.num_messages):
                if not self.running:
                    break
                try:
                    msg = f'SPAM #{i} - ' + 'X' * 200
                    self.sock.send(msg.encode())
                    sent += 1
                except (ConnectionResetError, BrokenPipeError, OSError):
                    break
            print(f'[SPAM_BOT] Sent {sent}/{self.num_messages} spam messages.')
        finally:
            self.sock.close()
            self.running = False
