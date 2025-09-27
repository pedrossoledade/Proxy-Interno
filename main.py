import uvicorn
import os
import socket

def is_port_in_use(port):
    """Verifica se a porta está em uso"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == "__main__":
    # Configuração para desenvolvimento
    if not os.getenv("CLIENT_ID"):
        os.environ["CLIENT_ID"] = "000"  # Valor padrão para testes
    
    port = 8000
    
    # Verificar se a porta está disponível
    if is_port_in_use(port):
        print(f"⚠️  Porta {port} está ocupada. Tentando porta 8001...")
        port = 8001
    
    print("🚀 Iniciando Proxy API Server...")
    print(f"📍 URL: http://localhost:{port}")
    print("📋 Endpoints:")
    print(f"   • http://localhost:{port}/proxy/score?cpf=XXX&client_id=XXX")
    print(f"   • http://localhost:{port}/health")
    print(f"   • http://localhost:{port}/metrics")
    print("⏹️  Pressione CTRL+C para parar")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=port,
            reload=True,
            access_log=True
        )
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        print("💡 Tente mudar a porta no código")