import requests
import time
import sys

def test_server():
    base_url = "http://localhost:8000"
    
    print("🧪 Testando conexão com o servidor...")
    
    try:
        # Teste de health check
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando!")
            print(f"📊 Health: {response.json()}")
            return True
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return False
    except requests.ConnectionError:
        print("❌ Não foi possível conectar ao servidor")
        print("💡 Verifique se o servidor está rodando com: python main.py")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    if test_server():
        print("\n🎯 Teste de endpoints:")
        
        # Teste do proxy/score
        try:
            response = requests.get(
                f"http://localhost:8000/proxy/score",
                params={"cpf": "01658739060", "client_id": "pedro&luigi"},
                timeout=10
            )
            print(f"📡 Proxy/Score: Status {response.status_code}")
            print(f"📦 Resposta: {response.json()}")
        except Exception as e:
            print(f"❌ Erro no proxy/score: {e}")
    else:
        sys.exit(1)