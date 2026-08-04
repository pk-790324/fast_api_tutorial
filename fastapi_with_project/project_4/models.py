from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import datetime,date


class Student(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:str=Field(index=True)
    age:int=Field(ge=20)
    dob:date
    address:str
    phone_no:str=Field(max_length=10)
    email:str=Field(index=True,unique=True)
    created_at:datetime=Field(default_factory=datetime.now)
    
    
class StudentCreate(SQLModel):
    name:str=Field(index=True)
    age:int=Field(ge=20)
    dob:date
    address:str
    phone_no:str=Field(max_length=10)
    email:str=Field(index=True,unique=True)
        


class StudentRead(SQLModel):
    id:int
    name:str
    age:int
    dob:date
    address:str
    phone_no:str
    email:str
    created_at:datetime


class StudentUpdate(SQLModel):
    name:str
    age:Optional[int]=Field(ge=20)
    dob:date
    address:str
    phone_no:str
    email:str
    
    