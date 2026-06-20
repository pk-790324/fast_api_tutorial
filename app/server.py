from typing import Callable,Any



routes: dict[str,Callable[[Any],Any]]={}

def route(path:str):
    def register_route(func):
        routes[path]=func
        return func
    return register_route

@route("/shipment")
def get_shipment():
    return "Shipment<1001, in transit>"
# this functions converts like this :get_shipment = route("/shipment")(get_shipment)

request:str=""

while request!="quit":
    request=input(">  ")
    if request in routes:
        response=routes[request]()
        print(response,end="\n\n")
    else:
        print("not found ")
