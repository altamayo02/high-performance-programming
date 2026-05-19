import threading  # usado para controlar concurrencia: Semaphore y Thread
import time
import numpy as np

def reparar(semáforo: threading.Semaphore) -> None:
	with semáforo:
		print(f'{threading.current_thread().name}: Reparando el servidor...')
		rng = np.random.default_rng()
		tiempo_reparacion = 1 + 2 * rng.random()
		time.sleep(tiempo_reparacion)
		print(f'{threading.current_thread().name}: Reparación completa.')

def semáforo(n_técnicos: int, aforo: int) -> None:
	semáforo = threading.Semaphore(aforo)  # crea semáforo con capacidad `aforo`

	# lista de hilos que "atenderán reparaciones"
	técnicos: list[threading.Thread] = []
	for i in range(n_técnicos):
		técnicos.append(
			threading.Thread(target=reparar, args=(semáforo,), name=f'Técnico {i+1}')  # crea hilo técnico
		)

	for técnico in técnicos:
		técnico.start()
	
	for técnico in técnicos:
		técnico.join()