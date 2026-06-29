from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from pydantic import  BaseModel, Field
from random import randint
from enum import Enum

app = FastAPI()


@app.get("/shipment")  # defining endpoints
def get_shipment():
    return {"content": "wooden table", "status": "in transit"}



# ========================================================================================================
# =============================== Module 3 : Path Parameters==============================================
# ========================================================================================================

# path parameters

@app.get("/shipment1/{id}")
def get_shipment1(id: int) -> dict[str, Any]:  # key:str, value:Any
    return {"id": id, "weight": 2.32, "content": "wooden box", "status": "delivered"}





# ========================================================================================================
# =============================== Module 3 : Route Ordering ==============================================
# ========================================================================================================

# Route Ordering
@app.get("/shipment1/latest")
def get_latest_shipment():
    return {
        "id": "latest",
        "weight": 77,
        "content": "glass ware",
        "status": "processing",
    }


# Note: to make run /shipment/latest make sure above /shipment1/{id} is comment
# because route ordering matters and /shipment/{id} requires input
# or run /shipment1/latest/above the /shipment1/{id}



# ========================================================================================================
# =============================== Module 3 : Simple Database =============================================
# ========================================================================================================

# simple database
shipment_data = {
    23323: {"weight": 32, "content": "wooden box", "status": "delivered"},
    23324: {"weight": 15, "content": "electronics", "status": "in_transit"},
    23325: {"weight": 8, "content": "clothing", "status": "in_transit"},
    23326: {"weight": 50, "content": "furniture", "status": "placed"},
    23327: {"weight": 22, "content": "books", "status": "delivered"},
    23328: {"weight": 12, "content": "kitchen utensils", "status": "delivered"},
}


@app.get("/shipment_data/{id}")
def get_shhipment_data(id: int) -> dict[str, Any]:
    if id not in shipment_data:
        return {"details": "Given id not exist!"}
    return shipment_data[id]


# ========================================================================================================
# ===============================Module 4 : Query Parameters =============================================
# ========================================================================================================

# 1. Query parameters

@app.get("/shipment_data1")
def get_shipment_data1(id: int) -> dict[str, Any]:
    if id not in shipment_data:
        return {"details": "given id not exist"}
    return shipment_data[id]


# Most used format


@app.get("/shipment_data2")
def get_shipment_data2(
    id: int | None = None,
) -> dict[
    str, Any
]:  # test id:int or id:int|None or id:int|None=None in scalar documentation
    if not id:  # executed when id field is blank
        id = max(shipment_data.keys())
        return shipment_data[id]

    if id not in shipment_data:
        return {"details": "Given ID not exist!"}
    return shipment_data[id]


# ========================================================================================================
# ================================ Module 4 : HTTP Exception =============================================
# ========================================================================================================


@app.get("/shipment_data3")
def get_shipment_data3(id: int | None = None) -> dict[str, Any]:
    if id not in shipment_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="GIVEN ID DOESNOT EXISTS"
        )
    return shipment_data[id]


# Note: After executing /shipment_data3 in scalar documentation
# you should see 9ms, Size:36 B, Status:404 Not Found
# which is HTTP Exception


# ========================================================================================================
# ================================ Module 4 : Post Method ================================================
# ========================================================================================================


# here we use /shipment_data3 get method
@app.post("/shipment_data3")
def post_shipment_data3(content: str, weight: float) -> dict[str, int]:
    if weight > 25.0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight must be less than 25 kg",
        )
    new_id = max(shipment_data.keys()) + 1
    shipment_data[new_id] = {"content": content, "weight": weight, "status": "placed"}
    return {"id": new_id}


# ========================================================================================================
# ================================ Module 4 : Request Body ===============================================
# ========================================================================================================


@app.post("/shipment_data4")
def request_body_shipment_data4(data: dict[str, Any]) -> dict[str, Any]:
    content = data["content"]
    weight = data["weight"]
    # validata weight
    if weight >= 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25kgs",
        )
    new_id = max(shipment_data.keys()) + 1
    shipment_data[new_id] = {"content": content, "weight": weight, "status": "placed"}
    return {"id": new_id}


# ========================================================================================================
# ============================= Module 4 : Path and Query Parameters =====================================
# ========================================================================================================


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> Any:
    return shipment_data[id][field]


# ========================================================================================================
# ==================================== Module 5 : PUT Method =============================================
# ========================================================================================================

# put method is used to update the all value of the existing data
# to check  data is changed or not check on get_shipment_data2 or 3


@app.put("/shipment_data4")
def update_shipment_data(
    id: int, content: str, weight: float, status: str
) -> dict[str, Any]:
    shipment_data[id] = {"content": content, "weight": weight, "status": status}
    return {"id": id, "content": content, "weight": weight, "status": status}


# ========================================================================================================
# ==================================== Module 5 : PATCH Method ===========================================
# ========================================================================================================


# patch method is used to update only the required field in the existing data
# to check data is changed or not check on get_shipment_data2 or 3


@app.patch("/shipment_data4")
def patch_shipment_data(
    id: int, body:dict[str,Any]
) -> dict[str, Any]:
    shipment=shipment_data[id]
    shipment.update(body)
    return shipment



# ========================================================================================================
# ==================================== Module 5 : DELETE Method ==========================================
# ========================================================================================================

# used to delete the data from the existing data

@app.delete("/shipment_data4")
def delete_shipment_data(id:int)->dict[str,Any]:
    shipment_data.pop(id)
    return {"detail":f"shipment with id: {id} is deleted"}


# ========================================================================================================
# ==================================== Module 6 : Pydantic Model =========================================
# ========================================================================================================

# here we are using pydantic model for type validations

class Shipment(BaseModel):
    content:str
    weight:float
    status:str

@app.post("/shipment")
def pydantic_submit_method(body:Shipment)->dict[str,Any]:
    if body.weight>25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kgs",
        )
    new_id=max(shipment_data.keys())+1
    shipment_data[new_id]={
        "content":body.content,
        "weight":body.weight,
        "status":body.status}
    return {"id":new_id,"data":shipment_data[new_id]}
    

# ========================================================================================================
# ==================================== Module 6 : Model Fields ===========================================
# ========================================================================================================

def random_number():
    return randint(200,300)


class Shipment1_field(BaseModel):
    content:str=Field(max_length=20,description="content of the shipment")
    weight:float=Field(le=90,ge=3,description="weight of the shipment")
    status:str=Field(description="status of the description")
    product_id:int=Field(default_factory=random_number,description="product id of the shipment")
    

# lt-> less than 
# le -> less than equal to 
# gt-> greater than
# ge-> greater than equal to 

@app.post("/shipment_field")
def field_submit_method(body1:Shipment1_field)->dict[str,Any]:
    new_id=max(shipment_data.keys())+1
    shipment_data[new_id]={
        "content":body1.content,
        "weight":body1.weight,
        "status":body1.status,
    }
    return {"id":new_id,"data":shipment_data[new_id]}



# ========================================================================================================
# ==================================== Module 6 : Python: Enum ===========================================
# ========================================================================================================

class ShipmentStatus(str,Enum):
    placed="placed"
    in_transit="in_transit"
    out_for_delivery="out_for_delivery"
    delivered="delivered"
# if shipment status if different from the above then it raise error
    
@app.patch("/shipment_data")
def patch_shipment_data_with_enum(
    id: int, body:dict[str,ShipmentStatus]
) -> dict[str, Any]:
    shipment=shipment_data[id]
    shipment.update(body)
    return {"shipment_data":shipment_data[id]}


    """
    give id of sample item in query parameters and only add status
    {
        "status":"delivered"
    }
    """


# ========================================================================================================
# ==================================== Module 6 : Response Model =========================================
# ========================================================================================================

#problem: during return time any data is returned so to fix that
# we use response model

class Shipment_response(BaseModel): # return type
    content:str
    weight:float #=Field(le=10,ge=3) if we enable this and weight is not compatible during return time it raise internal server error
    status:str
    
@app.get("/shipment_response")
def get_shipment_resonse(id:int)->Shipment_response:
    if id not in shipment_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does't exists"
        )
    shipment=shipment_data[id]
    #shipment.pop("content") # i.e if we miss content it raise: Internal Server error
    return Shipment_response(**shipment)

# note: when you expand 200 Successful Response in Response you 
# saw Shipment_response object like:
    """
    content string · Content required
    status string · Status required
    weight number · Weight required
    
    """




# ========================================================================================================
# ==================================== Module 6 : Different Model ========================================
# ========================================================================================================


shipment_modified_data = {
    2000: {"weight": 32, "content": "wooden box", "status": "delivered"},
    2001: {"weight": 15, "content": "electronics", "status": "in_transit"},
    2002: {"weight": 8, "content": "clothing", "status": "in_transit"},
    2003: {"weight": 50, "content": "furniture", "status": "placed"},
    2004: {"weight": 22, "content": "books", "status": "delivered"},
    2005: {"weight": 12, "content": "kitchen utensils", "status": "delivered"},
}


class BasePayment(str,Enum):
    cash_on_delivery="cash_on_delivery"
    on_line_payment="on_line_payment"

class BaseShipment(BaseModel):
    content:str
    weight:float
    status:ShipmentStatus
    
class ShipmentRead(BaseShipment):
    pass
class ShipmentCreate(BaseShipment):
    pass
class ShipmentUpdate(BaseShipment):
    payment:BasePayment


# for get method

@app.get("/shipment_response_different_model",response_model=ShipmentRead)
def get_shipment_different_model(id:int):
    if id not in shipment_modified_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does't exists in shipment_modified_data"
        )
    shipment=shipment_modified_data[id]
    #shipment.pop("content") # i.e if we miss content it raise: Internal Server error
    return shipment



# for patch method

@app.patch("/shipment_path_different_model",response_model=ShipmentUpdate)
def patch_shipment_data_with_different_model(
    id: int, body:ShipmentUpdate
):
    shipment=shipment_modified_data[id]
    print(body)
    shipment.update(body)
    return {"shipment_data":shipment_modified_data[id]}





# ==================================================================================================
# ==================================================================================================
# ==================================================================================================


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")


# ======================================================================================================
# ======================================================================================================
# ======================================================================================================
