import sys

from server import Server
from client import ChatClient
from spam_client import SpamClient


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage:')
        print('  python main.py server     - Start chat server')
        print('  python main.py client     - Start a regular chat client')
        print('  python main.py spam       - Start the spam client')
        print('  python main.py demo       - Run automated demo')
        return

    mode = sys.argv[1].lower()

    if mode == 'server':
        server = Server()
        server.start()
    elif mode == 'client':
        ChatClient()
    elif mode == 'spam':
        SpamClient()
    elif mode == 'demo':
        _run_demo()
    else:
        print(f'Unknown mode: {mode}')


def _run_demo() -> None:
    import time
    import threading

    print('=== Starting automated demo ===')

    server = Server()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    time.sleep(0.5)

    def auto_client(name: str, messages: list[str]) -> None:
        import socket as sk
        sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        sock.connect(('127.0.0.1', 5555))
        sock.send(name.encode())
        time.sleep(1)

        receiver_stop = False

        def receive() -> None:
            nonlocal receiver_stop
            while not receiver_stop:
                try:
                    data = sock.recv(4096)
                    if not data:
                        break
                    msg_str = data.decode()
                    if '[SYSTEM]' in msg_str or msg_str.startswith('['):
                        print(f'[{name}] {msg_str}')
                except OSError:
                    break

        recv_thread = threading.Thread(target=receive, daemon=True)
        recv_thread.start()

        time.sleep(2)
        for msg in messages:
            if receiver_stop:
                break
            try:
                sock.send(msg.encode())
                print(f'[{name}] Sent: {msg}')
                time.sleep(1.5)
            except OSError:
                break

        time.sleep(1)
        receiver_stop = True
        sock.close()
        print(f'[{name}] Disconnected.')

    print('\n[DEMO] Starting chat clients...')
    client1_thread = threading.Thread(
        target=auto_client,
        args=('Alice', [f'Hello Bob! #{i}' for i in range(5)]),
        daemon=True
    )
    client2_thread = threading.Thread(
        target=auto_client,
        args=('Bob', [f'Hey Alice! #{i}' for i in range(5)]),
        daemon=True
    )

    client1_thread.start()
    time.sleep(0.3)
    client2_thread.start()

    time.sleep(4)

    print('\n[DEMO] Starting spam client...')
    spam_client = SpamClient(num_messages=30)
    spam_client_thread = threading.Thread(target=spam_client._spam, daemon=True)
    spam_client_thread.start()

    time.sleep(8)

    print('\n[DEMO] Done. Check server output for chat history.')
    print('\nPress Ctrl+C to stop the server.')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n[DEMO] Finished.')
        server.server_socket.close()


if __name__ == '__main__':
    main()
