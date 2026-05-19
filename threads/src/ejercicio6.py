import threading
import time


def lector(
	registro: dict,
	bloqueo: threading.Lock,  # Lock para proteger contador de lectores
	escritura: threading.Lock,  # Lock exclusivo para escritores
	lectores_activos: list
) -> None:
	"""Lee el registro de usuarios respetando exclusión de escritores."""
	with bloqueo:
		lectores_activos[0] += 1
		if lectores_activos[0] == 1:
			escritura.acquire()

	print(f'Introduciendo {threading.current_thread().name}')
	usuario = registro['usuario1']
	print(f'{threading.current_thread().name} leyendo: {usuario}')
	time.sleep(1)

	with bloqueo:
		lectores_activos[0] -= 1
		if lectores_activos[0] == 0:
			escritura.release()

	print(f'{threading.current_thread().name} terminó de leer.')


def escritor(
	registro: dict,
	escritura: threading.Lock  # Lock exclusivo para proteger actualización
) -> None:
	"""Actualiza el registro de usuarios de forma exclusiva."""
	with escritura:  # adquiere exclusión para actualizar el registro
		print(f'{threading.current_thread().name} actualizando registro...')
		time.sleep(2)
		registro['usuario1']['visitas'] += 1
		registro['usuario1']['email'] = (
			f"{threading.current_thread().name.split(' ')[1]}@ejemplo.com"
		)  # usa nombre del hilo para modificar email (demostración)
		print(
			f'{threading.current_thread().name} actualizó registro: ' + 
			str(registro["usuario1"])  # muestra registro actualizado
		)


def lectores_y_escritores() -> None:
	"""Crea lectores y escritores para demostrar sincronización con Locks."""
	registro = {
		'usuario1': {
			'nombre': 'Ana Pérez',
			'email': 'ana.perez@ejemplo.com',
			'visitas': 0
		}
	}

	escritura = threading.Lock()  # Lock exclusivo para escritores
	bloqueo = threading.Lock()  # Lock para el contador de lectores
	lectores_activos = [0]

	hilos: list[threading.Thread] = []  # contenedor de hilos
	
	# Agregamos el Escritor 0
	hilos.append(
		threading.Thread(
			target=escritor,
			args=(registro, escritura),
			name='Escritor 0'
		)
	)

	# Agregamos los Lectores 0 y 1
	for i in range(2):
		hilos.append(
			threading.Thread(
				target=lector,
				args=(registro, bloqueo, escritura, lectores_activos),
				name=f'Lector {i}'
			)
		)
	
	# Agregamos el Escritor 1
	hilos.append(
		threading.Thread(
			target=escritor,
			args=(registro, escritura),
			name='Escritor 1'
		)
	)

	# Agregamos el Lector 2
	hilos.append(
		threading.Thread(
			target=lector,
			args=(registro, bloqueo, escritura, lectores_activos),
			name='Lector 2'
		)
	)

	for hilo in hilos:
		hilo.start()

	for hilo in hilos:
		hilo.join()

	print('\nRegistro final:', registro['usuario1'])


if __name__ == '__main__':
	lectores_y_escritores()
