from functools import wraps
import time

class Cache:
    def __init__(self, ttl=300):
        """Cache com Time-To-Live (padrão: 5 minutos)"""
        self.ttl = ttl
        self._cache = {}

    def get(self, key):
        """Recupera um valor do cache se ainda estiver válido"""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key, value):
        """Armazena um valor no cache com timestamp atual"""
        self._cache[key] = (value, time.time())

    def clear(self):
        """Limpa todo o cache"""
        self._cache.clear()

# Instância global do cache
cache = Cache()

def cached(ttl=300):
    """Decorator para cache automático de funções"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator