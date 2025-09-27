import asyncio
import time
from collections import deque
from utils.rate_limiter import rate_limiter
from utils.cache import cache
import requests

class RequestQueue:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestQueue, cls).__new__(cls)
            cls._instance.queue = deque()
            cls._instance.processing = False
            cls._instance.last_processed = time.time()
        return cls._instance
    
    async def add_request(self, id_client, cpf, future):
        cache_key = f"score:{cpf}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            future.set_result(cached_result)
            return
        
        self.queue.append((id_client, cpf, future))
        if not self.processing:
            await self.process_queue()
    
    async def process_queue(self):
        self.processing = True
        while self.queue:
            now = time.time()
            time_since_last = now - self.last_processed
            if time_since_last < 1.0:
                await asyncio.sleep(1.0 - time_since_last)
            
            id_client, cpf, future = self.queue.popleft()
            
            try:
                result = await self.make_request(id_client, cpf)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            
            self.last_processed = time.time()
        
        self.processing = False
    
    async def make_request(self, id_client, cpf):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_request, id_client, cpf)
    
    def _sync_request(self, id_client, cpf):
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
            return {"error": f"Unexpected error, status code {response.status_code}"}

request_queue = RequestQueue()