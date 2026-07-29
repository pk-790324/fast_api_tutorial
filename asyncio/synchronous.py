
from rich import print
import time


def endpoint(route):
    print(f">> handling {route}")
    # emulate database delay
    time.sleep(1)
    print(f"<< response {route}")
    
def server():
    # run test requests
    tests=(
        "GET / shipment?id=1",
        "PATCH / shipment?id=4",
        "DELETE / shipment?id=5"
    )
    start=time.perf_counter()
    for route in tests:
        endpoint(route)
    end=time.perf_counter()
    print(f'Time Taken: {end-start:.2f}s')
    
# Run server
server()