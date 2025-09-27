import asyncio
from utils.request_queue import request_queue

async def get_score(id_client, cpf):
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    
    await request_queue.add_request(id_client, cpf, future)
    
    return await future