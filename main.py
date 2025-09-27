import uvicorn
import os

if __name__ == "__main__":
    if not os.getenv("CLIENT_ID"):
        print("ERRO: CLIENT_ID não configurado")
        print("Exporte com: export CLIENT_ID=seu_client_id")
        exit(1)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )