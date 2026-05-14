import threading  # usado para Semaphore y Thread (alternancia entre hilos)
import time

def trabajador(
	nombre: str,
	permiso_actual: threading.Semaphore,  # semáforo que controla permiso de ejecución
	permiso_siguiente: threading.Semaphore,  # semáforo para ceder control al siguiente hilo
	contador: list
) -> None:
	"""Imprime un número y cede el control al siguiente trabajador."""
	while True:
		permiso_actual.acquire()
		if contador[0] <= 0:
			permiso_siguiente.release()
			break

		print(f'{nombre} imprime {contador[0]}')
		time.sleep(1)
		contador[0] -= 1
		permiso_siguiente.release()


def cuenta_regresiva() -> None:
	"""Alterna dos hilos en una cuenta regresiva de 10 a 1."""
	contador = [10]
	semaforo_a = threading.Semaphore(1)  # inicialmente A puede ejecutar
	semaforo_b = threading.Semaphore(0)  # B espera hasta que A libere

	hilo_a = threading.Thread(
		target=trabajador,
		args=('Trabajador A', semaforo_a, semaforo_b, contador)
	)  # crea hilo A
	hilo_b = threading.Thread(
		target=trabajador,
		args=('Trabajador B', semaforo_b, semaforo_a, contador)
	)  # crea hilo B

	hilo_a.start()
	hilo_b.start()

	hilo_a.join()
	hilo_b.join()
	print('Cuenta regresiva finalizada.')
