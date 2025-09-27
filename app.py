from fastapi import FastAPI, HTTPException
from api.score_api import get_score
import os

app = FastAPI(title="Proxy Score API", description="Proxy interno para API de Score")

@app.get("/proxy/score")
def proxy_score(cpf: str, client_id: str):
    """
    Endpoint principal do proxy
    - cpf: CPF a ser consultado (11 dígitos)
    - client_id: Client ID para autenticação
    """
    if not client_id:
        raise HTTPException(status_code=400, detail="Client ID não informado")
    if not cpf or len(cpf) != 11:
        raise HTTPException(status_code=400, detail="CPF inválido")
    
    result = get_score(client_id, cpf)
    return result

@app.get("/health")
def health():
    """Endpoint de health check"""
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    """Endpoint de métricas para monitoramento"""
    from utils.request_queue import request_queue
    from utils.cache import cache
    
    return {
        "queue_size": len(request_queue.queue),
        "cache_size": len(cache._cache),
        "processing": request_queue.processing,
        "system_status": "operational"
    }

@app.get("/")
def root():
    """Página inicial"""
    return {
        "message": "Proxy API Score",
        "endpoints": {
            "/proxy/score": "Consulta de score por CPF",
            "/health": "Status do serviço",
            "/metrics": "Métricas do sistema"
        }
    }