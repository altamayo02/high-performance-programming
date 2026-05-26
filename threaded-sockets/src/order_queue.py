import threading
from collections import deque


class OrderQueue:
    def __init__(self, max_capacity: int = 10) -> None:
        self._queue: deque = deque()
        self._capacity_sem = threading.Semaphore(max_capacity)
        self._items_sem = threading.Semaphore(0)
        self._lock = threading.Lock()

    def put(self, order: dict) -> int:
        self._capacity_sem.acquire()
        with self._lock:
            self._queue.append(order)
            size = len(self._queue)
        self._items_sem.release()
        return size

    def get(self) -> dict:
        self._items_sem.acquire()
        with self._lock:
            order = self._queue.popleft()
        self._capacity_sem.release()
        return order

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._queue)

    def __str__(self) -> str:
        with self._lock:
            items = list(self._queue)
            if not items:
                return '[Cola vacía]'
            return '\n'.join(
                f'  {i+1}. {o["quantity"]}x {o["product"]} (de {o["client"]})'
                for i, o in enumerate(items)
            )
