import sys
import time
import threading

from server import Server
from client import Client


def main() -> None:
    if len(sys.argv) < 2:
        print('Uso:')
        print('  python main.py server     - Iniciar servidor de pedidos')
        print('  python main.py client     - Iniciar un cliente')
        print('  python main.py demo       - Ejecutar demo automatizada')
        return

    mode = sys.argv[1].lower()

    if mode == 'server':
        server = Server()
        server.start()
    elif mode == 'client':
        Client()
    elif mode == 'demo':
        _run_demo()
    else:
        print(f'Modo desconocido: {mode}')


def _run_demo() -> None:
    print('=== Demo automatizada: Centro de Pedidos ===\n')

    server = Server()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    time.sleep(1)

    clients_data = [
        ('Camilo', ['laptop,1', 'mouse,2', 'keyboard,1', 'monitor,1']),
        ('Valeria', ['headset,1', 'mouse,1', 'laptop,1']),
        ('Santiago', ['keyboard,2', 'monitor,1', 'mouse,3', 'headset,2']),
    ]

    def auto_client(name: str, orders: list[str]) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 7777))
        sock.send(name.encode())

        rx_stop = False

        def receive() -> None:
            nonlocal rx_stop
            while not rx_stop:
                try:
                    data = sock.recv(4096)
                    if not data:
                        break
                    msg = data.decode()
                    if not msg.startswith('[SISTEMA] Bienvenido'):
                        print(f'[{name}] {msg}')
                except OSError:
                    break

        recv_thread = threading.Thread(target=receive, daemon=True)
        recv_thread.start()

        time.sleep(1.5)
        for order in orders:
            if rx_stop:
                break
            try:
                sock.send(order.encode())
                print(f'[{name}] Envió: {order}')
                time.sleep(random.uniform(0.5, 1.0))
            except OSError:
                break

        time.sleep(4)
        rx_stop = True
        sock.close()
        print(f'[{name}] Desconectado.')

    import socket
    import random

    threads = []
    for name, orders in clients_data:
        t = threading.Thread(
            target=auto_client,
            args=(name, orders),
            daemon=True
        )
        threads.append(t)
        t.start()
        time.sleep(0.3)

    for t in threads:
        t.join(timeout=10)

    time.sleep(6)

    print('\n=== Demo finalizada ===')
    print('\nPresiona Ctrl+C para detener el servidor.')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n[DEMO] Terminando...')
        server.running = False
        server.server_socket.close()


if __name__ == '__main__':
    main()
