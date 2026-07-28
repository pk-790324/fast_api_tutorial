from fastapi import FastAPI,HTTPException,status
from scalar_fastapi import get_scalar_api_reference

from typing import Any
import sqlite3

from pydantic import BaseModel

class ShipmentCreate(BaseModel):
    content: str
    weight: float

class ShipmentUpdate(BaseModel):
    status: str




class Database:
    def __init__(self):
        # make connection with database
        self.conn=sqlite3.connect("sqlite.db",check_same_thread=False)
        # get cursor to execute queries and fetch data
        self.cur=self.conn.cursor()
        # create a table if not exists
        self.create_table()
    def create_table(self):
        # 1. Create a table with columns
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment(
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
    
        """)
                
    def create(self,shipment:ShipmentCreate)->int:
        # find a new id
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result=self.cur.fetchone()
        new_id=result[0]+1
        # insert values in the tabel 
        self.cur.execute("""
            INSERT INTO shipment
            VALUES (:id,:content,:weight,:status)
        """,{
            "id":new_id,
            **shipment.model_dump(),
            "status":"placed"
        }
        )
        # commit the changes to the database
        self.conn.commit()
        return new_id


    def get(self,id:int)->dict[str,Any]|None:
        self.cur.execute("""
            SELECT * FROM shipment
            WHERE id=?
        """,(id,))
        row=self.cur.fetchone()
        return {
            "id":row[0],
            "content":row[1],
            "weight":row[2],
            "status":row[3],
        } if row else None
    
    def update(self,id:int,shipment:ShipmentUpdate)->dict[str,Any]:
        self.cur.execute("""
            UPDATE shipment SET status=:status
            WHERE id=:id
            
        """,{
            "id":id,
            **shipment.model_dump()
        }
        )
        self.conn.commit()
        return self.get(id)

    
    def delete(self,id:int):
        self.cur.execute("""
            DELETE FROM shipment
            WHERE id=?
        """,(id,)
        )
        self.conn.commit()
    
    def close(self):
        self.conn.close()
        
    
