import threading  # usado para Lock, Semaphore y Thread (productor/consumidor)
import time
from collections import deque


def productor(
	cola: deque,
	bloqueo: threading.Lock,
	espacio_cola: threading.Semaphore,  # controla espacio disponible en la cola
	oferta: threading.Semaphore  # controla disponibilidad de productos
) -> None:
	"""Coloca productos en la cola cada 2 segundos, cuando hay espacio disponible."""
	# Cada productor produce 10 productos
	for i in range(10):
		# Los productores ponen productos en la cola cada 2 segundos
		time.sleep(2)
		espacio_cola.acquire()
		with bloqueo:
			cola.append(f'{threading.current_thread().name}.{i}')
			print(f'{threading.current_thread().name} produjo')
			print(list(cola))
		oferta.release()


def consumidor(
	cola: deque,
	bloqueo: threading.Lock,
	espacio_cola: threading.Semaphore,
	oferta: threading.Semaphore,
) -> None:
	"""Quita productos de la cola cada segundo, cuando hay productos disponibles."""
	# Cada consumidor consume 10 productos
	for _ in range(10):
		oferta.acquire()
		with bloqueo:
			producto = cola.popleft()
			print(f'{threading.current_thread().name} consumió {producto}')
		espacio_cola.release()
		# Los consumidores ponen productos en la cola cada segundo
		time.sleep(1)


def consumir(
	n_productores: int,
	n_consumidores: int,
	max_cola: int = 3
) -> None:
	cola: deque = deque()
	bloqueo = threading.Lock()  # Lock protege acceso a la cola compartida
	espacio_cola = threading.Semaphore(max_cola)  # semáforo para limitar tamaño de cola
	oferta = threading.Semaphore(0)  # semáforo que indica cuántos items hay para consumir

	productores: list[threading.Thread] = []
	consumidores: list[threading.Thread] = []

	for i in range(n_productores):
		productores.append(
			threading.Thread(
				target=productor,
				args=(
					cola,
					bloqueo,
					espacio_cola,
					oferta,
				),
				name=f'Productor {i + 1}'
			)  # crea hilo productor
		)

	for i in range(n_consumidores):
		consumidores.append(
			threading.Thread(
				target=consumidor,
				args=(
					cola,
					bloqueo,
					espacio_cola,
					oferta
				),
				name=f'Consumidor {i + 1}'
			)  # crea hilo consumidor
		)

	for hilo in productores + consumidores:
		hilo.start()
	for hilo in productores + consumidores:
		hilo.join()

	print('Producción y consumo finalizados.')