import threading


PRODUCTS = {
    'laptop': {'price': 1200, 'stock': 10},
    'mouse': {'price': 25, 'stock': 50},
    'keyboard': {'price': 80, 'stock': 30},
    'monitor': {'price': 350, 'stock': 15},
    'headset': {'price': 60, 'stock': 25},
}


class Inventory:
    def __init__(self) -> None:
        self._products = {
            name: dict(info) for name, info in PRODUCTS.items()
        }
        self._lock = threading.Lock()

    def get_products(self) -> dict:
        with self._lock:
            return {name: dict(info) for name, info in self._products.items()}

    def check_availability(self, product: str, quantity: int = 1) -> bool:
        with self._lock:
            if product not in self._products:
                return False
            return self._products[product]['stock'] >= quantity

    def deduct(self, product: str, quantity: int = 1) -> bool:
        with self._lock:
            if product not in self._products:
                return False
            if self._products[product]['stock'] < quantity:
                return False
            self._products[product]['stock'] -= quantity
            return True

    def __str__(self) -> str:
        with self._lock:
            lines = ['Inventario actual:']
            for name, info in self._products.items():
                lines.append(f'  {name}: ${info["price"]} - {info["stock"]} unidades')
            return '\n'.join(lines)
