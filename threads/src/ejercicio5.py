import threading  # usado para Barrier y Thread (sincronización entre secciones)
import numpy as np


def sumar_sección(
	sección: np.ndarray,
	inicio: int,
	fin: int,
	sumas_parciales: list,
	indice: int,
	barrera: threading.Barrier
) -> None:
	"""
		Calcula la suma parcial de una sección de la matriz y espera en la barrera.
	"""
	parcial = int(sección.sum())
	sumas_parciales[indice] = parcial
	print(
		f'{threading.current_thread().name}: ' +
		f'suma filas {inicio} a {fin - 1} = {parcial}'
	)
	barrera.wait()


def total_matriz(filas: int, columnas: int, n_secciones: int) -> None:
	"""Divide la matriz en secciones y usa una barrera para sumar los resultados parciales."""
	rng = np.random.default_rng(42)
	matriz = rng.integers(0, 100, size=(filas, columnas), dtype=int)

	print('Matriz generada con dimensiones: ', matriz.shape)

	barrera = threading.Barrier(n_secciones)  # crea barrera para `n_secciones` hilos
	sumas_parciales = [0] * n_secciones
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
			args=(matriz[inicio:fin], inicio, fin, sumas_parciales, i, barrera),
			name=f'Sumador {i}'
		)
		# crea un hilo que suma su sección de la matriz
		hilos.append(hilo)
		hilo.start()

	for hilo in hilos:
		hilo.join()

	total = sum(sumas_parciales)
	print('\nResultados parciales:', sumas_parciales)
	print(f'Suma total de la matriz: {total}')
