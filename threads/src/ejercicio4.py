import threading
import time
from collections import deque


def productor(
	cola: deque,
	bloqueo: threading.Lock,
	demanda: threading.Semaphore,  # controla espacio disponible en la cola
	oferta: threading.Semaphore,  # controla disponibilidad de productos
	n_consumidores: int
) -> None:
	"""
		Coloca productos en la cola cada 2 segundos, cuando hay espacio disponible.
	"""
	# Cada productor produce n_consumidores productos
	for i in range(n_consumidores):
		# Los productores ponen productos en la cola cada 2 segundos
		time.sleep(2)
		demanda.acquire()
		with bloqueo:
			cola.append(f'{threading.current_thread().name}.{i}')
			print(f'{threading.current_thread().name} produjo')
			print(list(cola))
		oferta.release()


def consumidor(
	cola: deque,
	bloqueo: threading.Lock,
	demanda: threading.Semaphore,
	oferta: threading.Semaphore,
	n_productores: int
) -> None:
	"""
		Quita productos de la cola cada segundo, cuando hay productos disponibles.
	"""
	# Cada consumidor consume n_productores productos
	for _ in range(n_productores):
		oferta.acquire()
		with bloqueo:
			producto = cola.popleft()
			print(f'{threading.current_thread().name} consumió {producto}')
		demanda.release()
		# Los consumidores quitan productos de la cola cada segundo
		time.sleep(1)


def consumir(
	n_consumidores: int,
	n_productores: int,
	max_cola: int = 3
) -> None:
	cola: deque = deque()
	demanda = threading.Semaphore(max_cola)  # limitar tamaño de cola
	oferta = threading.Semaphore(0)  # indica cuántos items hay para consumir
	bloqueo = threading.Semaphore(1)  # protege acceso a la cola compartida

	productores: list[threading.Thread] = []
	consumidores: list[threading.Thread] = []

	for i in range(n_productores):
		productores.append(
			threading.Thread(
				target=productor,
				args=(
					cola,
					bloqueo,
					demanda,
					oferta,
					n_consumidores
				),
				name=f'Productor {i + 1}'
			)
		)

	for i in range(n_consumidores):
		consumidores.append(
			threading.Thread(
				target=consumidor,
				args=(
					cola,
					bloqueo,
					demanda,
					oferta,
					n_productores
				),
				name=f'Consumidor {i + 1}'
			)
		)

	for hilo in productores + consumidores:
		hilo.start()
	for hilo in productores + consumidores:
		hilo.join()

	print('Producción y consumo finalizados.')