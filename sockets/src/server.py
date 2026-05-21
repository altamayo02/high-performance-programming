import socket
import threading

from chat_history import ChatHistory


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
		self.name: str = ''
		self.is_chat_client = False

	def _send(self, message: str) -> None:
		try:
			self.client_socket.send(message.encode())
		except (OSError):
			pass

	def run(self) -> None:
		try:
			self.name = self.client_socket.recv(4096).decode()
			if not self.name:
				return

			connect_msg = f'[SISTEMA] {self.name} se conectó desde {self.address}'
			self.server.chat_history.add(connect_msg)
			print(f'[SERVER] {connect_msg}')

			with self.server.clients_lock:
					self.server.connection_count += 1
					self.is_chat_client = self.server.connection_count <= 2
					if self.is_chat_client:
							self.server.chat_clients.append(self)

			if self.is_chat_client:
					self._send('[SYSTEM] Connected. Waiting for other client...')
					self.server.ready_barrier.wait()
					self._send('[SYSTEM] Both clients connected! You can start chatting.')
			else:
					self._send('[SYSTEM] Connected as observer (messages are rate-limited).')

			while True:
					try:
							data = self.client_socket.recv(4096)
							if not data:
									break

							decoded_msg = data.decode()

							self.server.msg_semaphore.acquire()
							try:
									formatted = f'[{self.name}]: {decoded_msg}'
									self.server.chat_history.add(formatted)
									print(f'[SERVER] {formatted}')

									if self.is_chat_client:
											self.server.broadcast(self, formatted)
							finally:
									self.server.msg_semaphore.release()

					except (ConnectionResetError, BrokenPipeError, OSError):
							break
		except Exception as e:
			print(f'[SERVER] Error with {self.name}: {e}')
		finally:
			self.client_socket.close()
			disc_msg = f'[SYSTEM] {self.name} disconnected'
			self.server.chat_history.add(disc_msg)
			print(f'[SERVER] {disc_msg}')
			with self.server.clients_lock:
					if self.is_chat_client and self in self.server.chat_clients:
							self.server.chat_clients.remove(self)


class Server:
	def __init__(self, host: str = '127.0.0.1', port: int = 6666) -> None:
		self.host = host
		self.port = port

		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Permite reutilizar la dirección y el puerto al reiniciar el servidor
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((self.host, self.port))
		self.server_socket.listen(1)

		self.chat_history = ChatHistory()
		self.chat_clients: list[ClientHandler] = []
		self.clients_lock = threading.Lock()
		self.connection_count = 0
		self.ready_barrier = threading.Barrier(2)
		self.msg_semaphore = threading.Semaphore(5)

		print(f'[SERVIDOR] Escuchando bajo {self.host}:{self.port}')

	def broadcast(self, sender: ClientHandler, message: str) -> None:
		with self.clients_lock:
			for client in self.chat_clients:
				if client is not sender:
					client._send(message)

	def start(self) -> None:
		try:
			while True:
				client_sock, addr = self.server_socket.accept()
				handler = ClientHandler(self, client_sock, addr)
				handler.start()
		except KeyboardInterrupt:
			print('\n[SERVIDOR] Apagando...')
		finally:
			self.server_socket.close()
			print('\n[SERVIDOR] Historial de chat final:')
			print(self.chat_history)
