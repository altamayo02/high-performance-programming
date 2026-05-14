import threading  # usado para Barrier y Thread (sincronización entre secciones)
import numpy as np


def sumar_sección(
	sección: np.ndarray,
	inicio: int,
	fin: int,
	resultados: list,
	indice: int,
	barrera: threading.Barrier  # Barrier hace que cada hilo espere hasta que todos terminen
) -> None:
	"""Calcula la suma parcial de una sección de la matriz y espera en la barrera."""
	parcial = int(sección.sum())
	resultados[indice] = parcial
	print(f'{threading.current_thread().name}: suma filas {inicio} a {fin - 1} = {parcial}')  # muestra el nombre del hilo que calcula
	barrera.wait()


def total_matriz(filas: int, columnas: int, n_secciones: int) -> None:
	"""Divide la matriz en secciones y usa una barrera para sumar los resultados parciales."""
	rng = np.random.default_rng(42)
	matriz = rng.integers(0, 100, size=(filas, columnas), dtype=int)

	print('Matriz generada con dimensiones: ', matriz.shape)

	barrera = threading.Barrier(n_secciones)  # crea barrera para `n_secciones` hilos
	resultados = [0] * n_secciones
	hilos: list[threading.Thread] = []  # lista de threads que calculan secciones
	filas_por_sección = filas // n_secciones

	for i in range(n_secciones):
		inicio = i * filas_por_sección
		if i < n_secciones - 1:
			fin = (i + 1) * filas_por_sección
		else:
			fin = filas
		hilo = threading.Thread(
			target=sumar_sección,
			args=(matriz[inicio:fin], inicio, fin, resultados, i, barrera),
			name=f'Sumador {i}'
		)
		# crea un hilo que suma su sección de la matriz
		hilos.append(hilo)
		hilo.start()

	for hilo in hilos:
		hilo.join()

	total = sum(resultados)
	print('\nResultados parciales:', resultados)
	print(f'Suma total de la matriz: {total}')
