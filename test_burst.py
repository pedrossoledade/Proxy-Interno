import asyncio
import aiohttp
import time

async def test_burst():
    base_url = "http://localhost:8000"
    cpf = "03930956144"
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(20):
            task = asyncio.create_task(
                session.get(f"{base_url}/proxy/score?cpf={cpf}")
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Tempo total: {duration:.2f}s")
        print(f"Requisições/s: {20/duration:.2f}")
        
        for i, response in enumerate(responses):
            data = await response.json()
            print(f"Req {i+1}: Status {response.status} - {data}")

if __name__ == "__main__":
    asyncio.run(test_burst())