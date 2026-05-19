import numpy as np
import threading
import time

def depositar(bloqueo: threading.Lock, balance: list):
	with bloqueo:
		print('Depositando dinero...')

		rng = np.random.default_rng()
		time.sleep(1 + 3 * rng.random())
		balance[0] = balance[0] + 10 + 90 * rng.random()
		
		print(f'Balance: {balance[0]:.2f} (+)')

def retirar(bloqueo: threading.Lock, balance: list):
	with bloqueo:
		print('Retirando dinero...')
		time.sleep(2)

		rng = np.random.default_rng()
		balance[0] = balance[0] - 10 - 90 * rng.random()

		print(f'Balance: {balance[0]:.2f} (-)')


def bloqueo(n_transacciones) -> None:
	balance: list[float] = [1000]
	print(f'Balance inicial: {balance[0]:.2f}')

	bloqueo = threading.Lock()  # Lock compartido entre depósito y retiro

	depósitos = []
	retiros = []
	for i in range(n_transacciones):
		depósitos.append(threading.Thread(
			target=depositar,
			args=(bloqueo, balance),
			name=f'Depósito {i}')
		)
		retiros.append(threading.Thread(
			target=retirar,
			args=(bloqueo, balance),
			name=f'Retiro {i}')
		)

		depósitos[i].start()
		retiros[i].start()

	for i in range(n_transacciones):
		depósitos[i].join()
		retiros[i].join()