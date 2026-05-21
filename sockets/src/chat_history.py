import threading
from datetime import datetime


class ChatHistory:
    def __init__(self):
        self._messages: list[str] = []
        self._lock = threading.Lock()

    def add(self, message: str) -> None:
        timestamp = datetime.now().strftime('%H:%M:%S')
        with self._lock:
            self._messages.append(f'[{timestamp}] {message}')

    def get_all(self) -> list[str]:
        with self._lock:
            return list(self._messages)

    def __str__(self) -> str:
        with self._lock:
            if not self._messages:
                return '[No se ha enviado mensajes aún]'
            return '\n'.join(
                f'{i + 1}. {msg}' for i, msg in enumerate(self._messages)
            )
