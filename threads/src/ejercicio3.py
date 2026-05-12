import numpy as np
import threading
import time

def depositar(bloqueo: threading.Lock, consignaciones: list):
	with bloqueo:
		print('Depositando dinero...')
		time.sleep(2)

		rng = np.random.default_rng(42)
		balance = consignaciones[-1]
		consignaciones.append(balance + 10 + 90 * rng.random())
		
		print(f'Balance: {consignaciones[-1]:.2f} (+)')

def retirar(bloqueo: threading.Lock, consignaciones: list):
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

	bloqueo = threading.Lock()

	depósito = threading.Thread(target=depositar, args=(bloqueo, consignaciones), name='Depósito')
	retiro = threading.Thread(target=retirar, args=(bloqueo, consignaciones), name='Retiro')

	depósito.start()
	retiro.start()

	depósito.join()
	retiro.join()