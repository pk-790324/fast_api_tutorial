from fastapi import FastAPI, HTTPException,status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
app=FastAPI()

@app.get("/shipment") #defining endpoints
def get_shipment():
    return{
        "content":"wooden table",
        "status":"in transit"
    }



#path parameters


@app.get("/shipment1/{id}")
def get_shipment1(id:int)->dict[str,Any]: #key:str, value:Any
    return{
        "id":id,
        "weight":2.32,
        "content":"wooden box",
        "status":"delivered"     
    }
    
# Route Ordering

@app.get("/shipment1/latest")
def get_latest_shipment():
    return {
        "id":"latest",
        "weight":77,
        "content":"glass ware",
        "status":"processing"
    }
# Note: to make run /shipment/latest make sure above /shipment1/{id} is comment
# because route ordering matters and /shipment/{id} requires input
# or run /shipment1/latest/above the /shipment1/{id}



#simple database
shipment_data = {
    23323: {
        "weight": 32,
        "content": "wooden box",
        "status": "delivered"
    },
    23324: {
        "weight": 15,
        "content": "electronics",
        "status": "in transit"
    },
    23325: {
        "weight": 8,
        "content": "clothing",
        "status": "processing"
    },
    23326: {
        "weight": 50,
        "content": "furniture",
        "status": "out for delivery"
    },
    23327: {
        "weight": 22,
        "content": "books",
        "status": "delivered"
    },
    23328: {
        "weight": 12,
        "content": "kitchen utensils",
        "status": "pending"
    }
}


@app.get("/shipment_data/{id}")
def get_shhipment_data(id:int)->dict[str,Any]:
    if id not in shipment_data:
        return {"details":"Given id not exist!"}
    return shipment_data[id]


#========================================================================================================
#===============================Module 4 : Query Parameters =============================================
#========================================================================================================

# 1. Query parameters 

@app.get("/shipment_data1")
def get_shipment_data1(id:int)->dict[str,Any]:
    if id not in shipment_data:
        return {"details":"given id not exist"}
    return shipment_data[id]


# Most used format

@app.get("/shipment_data2")
def get_shipment_data2(id:int|None=None)->dict[str,Any]: # test id:int or id:int|None or id:int|None=None in scalar documentation
    if not id: #executed when id field is blank
        id=max(shipment_data.keys())
        return shipment_data[id]
        
    if id not in shipment_data:
        return {"details":"Given ID not exist!"}
    return shipment_data[id]


#========================================================================================================
#================================ Module 4 : HTTP Exception =============================================
#========================================================================================================



@app.get("/shipment_data3")
def get_shipment_data3(id:int|None=None)->dict[str,Any]:
    if id not in shipment_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GIVEN ID DOESNOT EXISTS"
        )
    return shipment_data[id]
    
# Note: After executing /shipment_data3 in scalar documentation
# you should see 9ms, Size:36 B, Status:404 Not Found
# which is HTTP Exception


#========================================================================================================
#================================ Module 4 : Post Method =============================================
#========================================================================================================




















@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )
