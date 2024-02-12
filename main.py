

from typing import List, Union

from fastapi import FastAPI, Query
from app import  ProductDTO

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/allergens/{barcode}")
def check_allergens(barcode: str, intolerances: List[str] = Query(None)):
    product = ProductDTO(barcode)
    if product.has_intolerance(intolerances):
        return {"contains_allergens": True}
    else:
        return {"contains_allergens": False}

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
