import socket
import threading


class ChatClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 5555) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.name = input('Enter your name: ')
        self.sock.send(self.name.encode())
        self.running = True

        self.receiver = threading.Thread(target=self._receive, daemon=True)
        self.receiver.start()

        self._send_loop()

    def _receive(self) -> None:
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                print(f'\n{data.decode()}')
                print('> ', end='', flush=True)
            except (ConnectionResetError, BrokenPipeError, OSError):
                break

        self.running = False

    def _send_loop(self) -> None:
        try:
            while self.running:
                msg = input('> ')
                if msg.lower() == '/quit':
                    break
                self.sock.send(msg.encode())
        finally:
            self.sock.close()
            self.running = False
            print('[CLIENT] Disconnected.')
