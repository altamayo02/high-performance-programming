import socket
import random
import threading
import time

PRODUCTS = ['laptop', 'mouse', 'keyboard', 'monitor', 'headset']


class Client:
    def __init__(self, host: str = '127.0.0.1', port: int = 7777) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.name = input('Nombre del cliente: ') or f'Cliente-{random.randint(100, 999)}'
        self.sock.send(self.name.encode())
        self.running = True

        self.receiver = threading.Thread(target=self._receive, daemon=True)
        self.receiver.start()

        self._send_orders()

    def _receive(self) -> None:
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                print(f'\n{data.decode()}')
                print('> ', end='', flush=True)
            except OSError:
                break
        self.running = False

    def _send_orders(self) -> None:
        time.sleep(0.5)
        n_orders = random.randint(1, 5)
        print(f'\n[{self.name}] Enviando {n_orders} pedido(s)...\n')

        for i in range(n_orders):
            if not self.running:
                break
            product = random.choice(PRODUCTS)
            quantity = random.randint(1, 3)
            msg = f'{product},{quantity}'
            try:
                self.sock.send(msg.encode())
                print(f'[{self.name}] Pedido {i + 1}: {quantity}x {product}')
                time.sleep(random.uniform(0.5, 1.5))
            except OSError:
                break

        print(f'\n[{self.name}] Todos los pedidos enviados. Esperando respuestas...\n')
        time.sleep(3)

        self.sock.close()
        self.running = False
        print(f'[{self.name}] Desconectado.')
