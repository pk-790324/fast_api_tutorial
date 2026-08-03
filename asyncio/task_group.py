import asyncio
import time
from rich import print

async def endpont(route:str)->str:
    print(f"handling {route}")
    await asyncio.sleep(3)
    print(f"response {route}")
    
    
async def server():
    tests=(
        "GET /shipment?id=3",
        "PATCH /shipment?id=4",
        "DELETE /shipment?id=5"
    )
    start=time.perf_counter()
    async with asyncio.TaskGroup() as task_group:
        tasks=[
            task_group.create_task(endpont(route)) 
            for route in tests
        ]
        print(tasks[0])
    end=time.perf_counter()
    print(f"Time taken:{end-start:.2f}s")


# run server
asyncio.run(server())

    