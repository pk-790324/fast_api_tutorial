from fastapi import FastAPI,HTTPException,status
from scalar_fastapi import get_scalar_api_reference

from typing import Any


from database_2 import Database,ShipmentCreate,ShipmentUpdate

app=FastAPI()

db=Database()

## Read a shipment by id 
@app.get("/shipment")
def get_shipment(id:int):
    # check for shipment with give id
    shipment=db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exists!",
        )
    return shipment

## Create a new shipment with content and weight
@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id=db.create(shipment)
    # return id for later use
    return {"id":new_id}

# update fields of a shipment
@app.patch("/shipment",response_model=None)
def update_shipment(id:int,shipment:ShipmentUpdate):
    #update data with given fieds
    shipment=db.update(id,shipment)
    return shipment

# delete shipment by id 
@app.delete("/shipment")
def delete_shipment(id:int)->dict[str,str]:
    # remove from database
    db.delete(id)
    return {"detail":f"shipment with id #{id} is deleted"}
    




@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")