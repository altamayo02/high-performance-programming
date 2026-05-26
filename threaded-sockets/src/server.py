import socket
import threading
import time
import random

from order_queue import OrderQueue
from inventory import Inventory

MIN_ORDERS = 5
N_PROCESSORS = 3


class ClientHandler(threading.Thread):
    def __init__(
        self,
        server: 'Server',
        client_socket: socket.socket,
        address: tuple
    ) -> None:
        super().__init__()
        self.server = server
        self.client_socket = client_socket
        self.address = address
        self.name = ''

    def run(self) -> None:
        try:
            self.name = self.client_socket.recv(4096).decode()
            if not self.name:
                return

            msg = f'[SISTEMA] {self.name} se conectó desde {self.address}'
            print(f'[SERVIDOR] {msg}')

            self._send(f'[SISTEMA] Bienvenido {self.name} al centro de pedidos.')
            self._send(self.server.inventory.__str__())

            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    break

                raw = data.decode()
                parts = raw.split(',')
                if len(parts) != 2:
                    self._send('[ERROR] Formato inválido. Use: producto,cantidad')
                    continue

                product = parts[0].strip().lower()
                try:
                    quantity = int(parts[1].strip())
                except ValueError:
                    self._send('[ERROR] La cantidad debe ser un número entero')
                    continue

                if quantity <= 0:
                    self._send('[ERROR] La cantidad debe ser positiva')
                    continue

                if not self.server.inventory.check_availability(product, quantity):
                    self._send(f'[ERROR] Stock insuficiente de {product}')
                    continue

                order = {
                    'client': self.name,
                    'product': product,
                    'quantity': quantity,
                }
                qsize = self.server.order_queue.put(order)
                self._send(f'[SISTEMA] Pedido recibido: {quantity}x {product}. Pedidos en cola: {qsize}')

                msg = f'{self.name} pidió {quantity}x {product} (cola: {qsize})'
                print(f'[SERVIDOR] {msg}')

        except (ConnectionResetError, BrokenPipeError, OSError) as e:
            print(f'[SERVIDOR] Error con {self.name}: {e}')
        finally:
            self.client_socket.close()
            print(f'[SISTEMA] {self.name} se desconectó')

    def _send(self, message: str) -> None:
        try:
            self.client_socket.send(message.encode())
        except OSError:
            pass


class Processor(threading.Thread):
    def __init__(
        self,
        order_queue: OrderQueue,
        inventory: Inventory,
        barrier: threading.Barrier,
        min_orders: int
    ) -> None:
        super().__init__(daemon=True)
        self.order_queue = order_queue
        self.inventory = inventory
        self.barrier = barrier
        self.min_orders = min_orders
        self.running = True

    def stop(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            while self.order_queue.size < self.min_orders:
                if not self.running:
                    return
                time.sleep(0.5)

            if not self.running:
                break

            self.barrier.wait()

            if not self.running:
                break

            if self.order_queue.size == 0:
                continue

            order = self.order_queue.get()

            t = random.uniform(1, 5)
            print(
                f'[PROCESADOR] {threading.current_thread().name} '
                f'procesando {order["quantity"]}x {order["product"]} '
                f'para {order["client"]} ({t:.1f}s)'
            )
            time.sleep(t)

            success = self.inventory.deduct(order['product'], order['quantity'])
            if success:
                print(
                    f'[PROCESADOR] {threading.current_thread().name} '
                    f'despachó {order["quantity"]}x {order["product"]} '
                    f'para {order["client"]}'
                )
            else:
                print(
                    f'[PROCESADOR] {threading.current_thread().name} '
                    f'sin stock suficiente de {order["product"]} '
                    f'para {order["client"]}'
                )


class Server:
    def __init__(self, host: str = '127.0.0.1', port: int = 7777) -> None:
        self.host = host
        self.port = port
        self.inventory = Inventory()
        self.order_queue = OrderQueue(max_capacity=10)
        self.barrier = threading.Barrier(N_PROCESSORS)
        self.running = True

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.processors = [
            Processor(
                self.order_queue,
                self.inventory,
                self.barrier,
                MIN_ORDERS
            ) for _ in range(N_PROCESSORS)
        ]
        for p in self.processors:
            p.start()

        print(f'[SERVIDOR] Centro de pedidos iniciado en {self.host}:{self.port}')
        print(f'[SERVIDOR] Procesadores activos: {N_PROCESSORS}')
        print(f'[SERVIDOR] Mínimo de pedidos por lote: {MIN_ORDERS}')
        print(self.inventory)
        print()

    def start(self) -> None:
        try:
            while self.running:
                client_sock, addr = self.server_socket.accept()
                handler = ClientHandler(self, client_sock, addr)
                handler.start()
        except KeyboardInterrupt:
            print('\n[SERVIDOR] Apagando...')
        finally:
            self.running = False
            for p in self.processors:
                p.stop()
            self.server_socket.close()
            print('\n[SERVIDOR] Inventario final:')
            print(self.inventory)
