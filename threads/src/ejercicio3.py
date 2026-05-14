import numpy as np
import threading  # usado para Lock y Thread (proteger sección crítica)
import time

def depositar(bloqueo: threading.Lock, consignaciones: list):  # Lock asegura exclusión mutua
	with bloqueo:
		print('Depositando dinero...')
		time.sleep(2)

		rng = np.random.default_rng(42)
		balance = consignaciones[-1]
		consignaciones.append(balance + 10 + 90 * rng.random())
		
		print(f'Balance: {consignaciones[-1]:.2f} (+)')

def retirar(bloqueo: threading.Lock, consignaciones: list):  # Lock protege acceso concurrente al balance
	with bloqueo:
		print('Retirando dinero...')
		time.sleep(2)

		rng = np.random.default_rng(42)
		balance = consignaciones[-1]
		consignaciones.append(balance - 10 - 90 * rng.random())

		print(f'Balance: {consignaciones[-1]:.2f} (-)')


def bloqueo() -> None:
	consignaciones: list[float] = [1000]
	print(f'Balance inicial: {consignaciones[-1]:.2f}')

	bloqueo = threading.Lock()  # Lock compartido entre depósito y retiro

	depósito = threading.Thread(target=depositar, args=(bloqueo, consignaciones), name='Depósito')  # crea hilo para depósito
	retiro = threading.Thread(target=retirar, args=(bloqueo, consignaciones), name='Retiro')  # crea hilo para retiro

	depósito.start()
	retiro.start()

	depósito.join()
	retiro.join()