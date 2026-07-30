import asyncio
import time
from rich import print

async def endpoint(route:str)->str:
    print(f">> handling {route}")
    await asyncio.sleep(4)
    print(f"<< response {route}")
    return route

async def  server():
    tests=(
        "GET /shipment?id=1",
        "PATCH /shipment?id=3",
        "DELETE /shipment?id=4"
    )
    start=time.perf_counter()
    
    requests=[
        asyncio.create_task(endpoint(route))
        for route in tests
    ]
    done,pending=await asyncio.wait(requests)
    
    for task in done:
        print("Result:",task.result())
    end=time.perf_counter()
    print(f"Time taken:{end-start:.2f}s")
    
asyncio.run(server())