from datetime import datetime, timedelta

from fastapi import FastAPI,HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from typing import Any


from app.main import ShipmentStatus

from database.models import Shipment
from database_2 import Database,ShipmentCreate, ShipmentRead,ShipmentUpdate

from database.session import SessionDep, create_db_tables, get_session
@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield
    
    






app=FastAPI(lifespan=lifespan_handler)

db=Database()

## Read a shipment by id 
@app.get("/shipment")
def get_shipment(id:int,session:SessionDep):
    # check for shipment with give id
    shipment=session.get(Shipment,id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exists!",
        )
    return shipment

## Create a new shipment with content and weight
@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate,session:SessionDep) -> dict[str, int]:
    new_shipment=Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now()+timedelta(days=3)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id":new_shipment.id}

# update fields of a shipment
@app.patch("/shipment",response_model=ShipmentRead)
def update_shipment(id:int,shipment_update:ShipmentUpdate,session: SessionDep):
    #update data with given fieds
    update=shipment_update.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="NO data provided to update"
        )
    shipment=session.get(Shipment,id)
    shipment.sqlmodel_update(update)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment

# delete shipment by id 
@app.delete("/shipment")
def delete_shipment(id:int,session: SessionDep)->dict[str,str]:
    # remove from database
    session.delete(
        session.get(Shipment,id)
    )
    session.commit()
    return {"detail":f"shipment with id #{id} is deleted"}
    




@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")