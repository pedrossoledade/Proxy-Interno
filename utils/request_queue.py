import time
import threading
from collections import deque
from utils.rate_limiter import rate_limiter
from utils.cache import cache
import requests

class RequestQueue:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton: garante apenas uma instância da fila"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(RequestQueue, cls).__new__(cls)
                cls._instance.queue = deque()
                cls._instance.processing = False
                cls._instance.last_processed = time.time()
                cls._instance.thread = None
        return cls._instance
    
    def add_request(self, id_client, cpf):
        """Adiciona uma requisição à fila e retorna o resultado"""
        cache_key = f"score:{cpf}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        with self._lock:
            future = {
                "id_client": id_client, 
                "cpf": cpf, 
                "event": threading.Event(),
                "result": None
            }
            self.queue.append(future)
            
            if not self.processing:
                self.start_processing()
        
        future["event"].wait()
        return future["result"]
    
    def start_processing(self):
        """Inicia o thread que processa a fila"""
        self.processing = True
        self.thread = threading.Thread(target=self.process_queue, daemon=True)
        self.thread.start()
    
    def process_queue(self):
        """Processa a fila em um thread separado (1 req/segundo)"""
        while True:
            with self._lock:
                if not self.queue:
                    self.processing = False
                    break
                
                future = self.queue[0]
            
            now = time.time()
            time_since_last = now - self.last_processed
            if time_since_last < 1.0:
                time.sleep(1.0 - time_since_last)
            
            try:
                result = self.make_request(future["id_client"], future["cpf"])
                future["result"] = result
            except Exception as e:
                future["result"] = {"error": str(e)}
            
            future["event"].set()
            
            with self._lock:
                self.queue.popleft()
                self.last_processed = time.time()
    
    def make_request(self, id_client, cpf):
        """Faz a requisição real para a API externa"""
        rate_limiter.wait_for_slot()
        
        url = f"https://score.hsborges.dev/api/score?cpf={cpf}"
        headers = {
            "accept": "application/json",
            "client-id": id_client
        }
        
        response = requests.get(url, headers=headers)
        rate_limiter.update_after_response(response)
        
        if response.status_code == 200:
            result = response.json()
            cache_key = f"score:{cpf}"
            cache.set(cache_key, result)
            return result
        elif response.status_code == 400:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Client ID não informado ou inválido"}
        elif response.status_code == 429:
            return response.json()
        else:
            return {"error": f"Erro inesperado, status code {response.status_code}"}

request_queue = RequestQueue()