import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def make_request(i, cpf, client_id, results):
    """Função para fazer uma requisição individual no teste de carga"""
    try:
        start_time = time.time()
        response = requests.get(
            f"http://localhost:8000/proxy/score",
            params={"cpf": cpf, "client_id": client_id},
            timeout=30
        )
        end_time = time.time()
        results[i] = {
            "status": response.status_code,
            "data": response.json(),
            "duration": end_time - start_time
        }
    except Exception as e:
        results[i] = {"error": str(e)}

def test_burst():
    """Teste de carga: 20 requisições simultâneas"""
    cpf = "01658739060"
    client_id = "pedro&luigi"
    
    num_requests = 20
    results = [None] * num_requests
    
    print(f"🧪 Iniciando teste de {num_requests} requisições simultâneas...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(num_requests):
            executor.submit(make_request, i, cpf, client_id, results)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"⏱️  Tempo total: {duration:.2f}s")
    print(f"📊 Requisições/s: {num_requests/duration:.2f}")
    
    successful = 0
    errors = 0
    for i, result in enumerate(results):
        if result and "error" not in result:
            successful += 1
            status_icon = "✅" if result['status'] == 200 else "⚠️"
            print(f"{status_icon} Req {i+1}: Status {result['status']} - Duração: {result['duration']:.2f}s")
        else:
            errors += 1
            print(f"❌ Req {i+1}: ERRO - {result.get('error', 'Unknown error')}")
    
    print(f"\n📈 RESUMO:")
    print(f"   ✅ Sucessos: {successful}/{num_requests}")
    print(f"   ❌ Erros: {errors}/{num_requests}")
    print(f"   ⏱️  Tempo médio por req: {duration/num_requests:.2f}s")

if __name__ == "__main__":
    test_burst()