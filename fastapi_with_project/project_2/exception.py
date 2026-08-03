from fastapi.responses import JSONResponse
from fastapi import Request




class PinCodeNotFoundError(Exception):
    def __init__(self,pincode:str):
        self.pincode=pincode


class InvalidPinCodeError(Exception):
    def __init__(self,pincode:str,reason:str="Invalid format"):
        self.pincode=pincode
        self.reason=reason
        
# custom handler

async def pincode_not_found_handler(request:Request,exc:PinCodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error":"pincode not found",
            "message":f"no location for pincode:{exc.pincode}",
            "pincode":exc.pincode
        }
    )
    
    
async def invalid_pincode_handler(request:Request,exc:InvalidPinCodeError):
    return JSONResponse(
        status_code=400,
        content={
            "error":"invalid pin code",
            "message":f"pincode '{exc.pincode}' is invalid: {exc.reason}",
            "pincode":exc.pincode
            
        }
    )
    