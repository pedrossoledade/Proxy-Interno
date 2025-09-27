from fastapi import FastAPI, HTTPException
from api.score_api import get_score
import os

app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")

@app.get("/proxy/score")
async def proxy_score(cpf: str):
    if not CLIENT_ID:
        raise HTTPException(status_code=500, detail="Client ID não configurado")
    if not cpf or len(cpf) != 11:
        raise HTTPException(status_code=400, detail="CPF inválido")
    
    result = await get_score(CLIENT_ID, cpf)
    return result

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    from utils.request_queue import request_queue
    from utils.cache import cache
    
    return {
        "queue_size": len(request_queue.queue),
        "cache_size": len(cache._cache),
        "processing": request_queue.processing
    }