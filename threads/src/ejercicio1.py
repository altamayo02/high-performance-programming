import threading
import pandas as pd
import numpy as np

def generar_marco_datos(filas, columnas) -> pd.DataFrame:
	rng = np.random.default_rng(42)
	datos = rng.integers(0, 101, size=(filas, columnas))
	df = pd.DataFrame(datos)
	return df

def calcular_media(
	df: pd.DataFrame,
	id_col: int,
	medias: list,
	barrera: threading.Barrier
) -> None:
	# Selecciona su columna correspondiente y calcula la media
	media = df.iloc[:, id_col].mean()
	medias[id_col] = media
	print(f'Hilo {id_col}, columna {id_col} - Media: {media:.2f}')

	# Espera a que todos los hilos hayan calculado una media
	barrera.wait()

def barrera(n_hilos: int) -> None:
	df = generar_marco_datos(100, max(10, n_hilos))
	print('Cabeza del conjunto de datos:')
	print(df.head(), '\n')

	barrera = threading.Barrier(n_hilos)

	medias = [0.0] * n_hilos
	hilos: list[threading.Thread] = []
	for id_col in range(n_hilos):
		hilo = threading.Thread(
			target=calcular_media,
			args=(df, id_col, medias, barrera)
		)
		hilos.append(hilo)
		hilo.start()

	for hilo in hilos:
		hilo.join()
	
	suma_medias = sum(medias)
	print(f'Suma de las tres medias: {suma_medias:.2f}')