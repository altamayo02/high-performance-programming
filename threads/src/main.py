import ejercicio1
import ejercicio2
import ejercicio3
import ejercicio4

if __name__ == '__main__':
	print('##### EJERCICIO 1 - BARRERA #####\n')
	ejercicio1.barrera(n_hilos=3)
	print('\n')

	print('##### EJERCICIO 2 - REPARACIÓN SERVIDORES #####\n')
	ejercicio2.semáforo(num_técnicos=10, aforo=3)
	print('\n')

	print('##### EJERCICIO 3 - BAILE DE TRANSACCIONES #####\n')
	ejercicio3.bloqueo()
	print('\n')

	print('##### EJERCICIO 4 - CONSUMISMO #####\n')
	ejercicio4.consumir(oferta=0.5, demanda=1)
	print('\n')