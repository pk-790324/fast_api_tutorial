from fastapi import FastAPI


from data import pincode_db
from exception import PinCodeNotFoundError,pincode_not_found_handler,InvalidPinCodeError,invalid_pincode_handler
from model import PincodeRequest,LocationResponse,BulkResponse,BulkRequest




app=FastAPI(
    title="Pincode lookup API",
    description="Auto Fill City and status from Indian pincode during checkout",
    
)


# register your custom exception handler
app.add_exception_handler(
    PinCodeNotFoundError,
    pincode_not_found_handler
)

app.add_exception_handler(
    InvalidPinCodeError,
    invalid_pincode_handler
)


@app.get("/pincode/{code}",response_model=LocationResponse)
def lookup_pincode(code:str):
    if len(code)!=6 or not code.isdigit():
        raise InvalidPinCodeError(code,"must be exactly 6 digit")
    if code not in pincode_db:
        raise PinCodeNotFoundError(code)
    return pincode_db[code]
        
    
@app.get("/pincode/bulk",response_model=BulkResponse)
def bulk_lookup(request:BulkRequest):
    results=[]
    missing=[]
    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)
    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        result=results,
        missing=missing    
    )
            
            
#  uvicorn main:app --reload --app-dir fastapi_with_project/project_2 --port 8001
