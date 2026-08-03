from fastapi import FastAPI, HTTPException, Query
from data import menu_item
from models import MenuResponse,MenuItem




app=FastAPI(
    title="chai point menu API",
    description="read only menu API for Kiosk display and mobile app"
)

@app.get("/")
def root():
    return {"message":"welcome to chai point menu api"}


@app.get("/menu",response_model=MenuResponse)
def get_menu(category:str|None=Query(None,description="filter by chai,snack or combo")):
    if category:
        filtered=[item for item in menu_item if item['category']==category.lower()]
        if not filtered:
            raise HTTPException(
                status_code=404,
                detail=f"No item found in category:{category}"
            )
        return MenuResponse(count=len(filtered),items=filtered)
    return MenuResponse(count=len(menu_item),items=menu_item)


@app.get("/menu/{item_id}",response_model=MenuItem)
def get_item(item_id:int):
    for item in menu_item:
        if item["id"]==item_id:
            return item
    raise HTTPException(
        status_code=404,
        detail="cannot found this id"
        
    )