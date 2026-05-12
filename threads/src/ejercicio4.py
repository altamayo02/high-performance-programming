import threading
from queue import Queue

def consumir(n_productores: int, tasa_oferta: float, tasa_demanda: float) -> None:
	semáforo = threading.Semaphore(int(tasa_oferta ** -1))

	cola = Queue()
	productores: list[threading.Thread] = []
	consumidores: list[threading.Thread] = []
	for i in range(n_productores):
		