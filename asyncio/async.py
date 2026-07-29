import asyncio
import time

from rich import print



async def endpoint(route:str)->str:
    print(f">> handling {route}")
    
    # emulate database delay
    await asyncio.sleep(2)
    
    print(f"<< response{route}")
    
    return route

async def server():
    # run test requests
    tests=(
        "GET /shipment?id=1",
        "PATCH /shipment?id=4",
        "DELETE /shipment?id=6"
    )
    start=time.perf_counter()
    for routes in tests:
        await endpoint(routes)
    end=time.perf_counter()
    print(f'total time:{end-start:.2f}s')
    

# run server
asyncio.run(server())
