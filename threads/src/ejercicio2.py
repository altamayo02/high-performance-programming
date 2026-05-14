import threading  # usado para controlar concurrencia: Semaphore y Thread
import time
import numpy as np

def reparar(semáforo: threading.Semaphore) -> None:  # Semaphore limita acceso concurrente (aforo)
	with semáforo:
		print(f'{threading.current_thread().name}: Reparando el servidor...')
		rng = np.random.default_rng(42)
		tiempo_reparacion = 1 + 2 * rng.random()
		time.sleep(tiempo_reparacion)
		print(f'{threading.current_thread().name}: Reparación completa.')

def semáforo(num_técnicos: int, aforo: int) -> None:
	semáforo = threading.Semaphore(aforo)  # crea semáforo con capacidad `aforo`

	técnicos: list[threading.Thread] = []  # lista de threads que atenderán reparaciones
	for i in range(num_técnicos):
		técnicos.append(
			threading.Thread(target=reparar, args=(semáforo,), name=f'Técnico {i+1}')  # crea hilo técnico
		)

	for técnico in técnicos:
		técnico.start()
	
	for técnico in técnicos:
		técnico.join()