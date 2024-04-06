from fastapi import FastAPI
import math
from fastapi.responses import HTMLResponse
# from enum import Enum
# from mangum import Mangum
from pydantic import BaseModel
app = FastAPI()
# handler=Mangum(app)
import data
import model

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ayurvedic(BaseModel):
    Symptoms: str


@app.get("/")
async def main():
    return HTMLResponse("<h1>welcome to Ayurmedic</h1>")

@app.post("/")
async def root(item: Ayurvedic):
    input=data.symptoms[item.Symptoms]
    k=model.model.predict([[input]])[0]
    for i in range(len(k)):
        k[i]=math.floor(k[i])
    ans={
        "MedicineName":data.ayurvedic[k[0]],
        "MainIngredients": data.ingredients[k[1]],
        "CommonlyUsedforDiseases": data.commonName[k[2]],
        "AlternateAllopathicDrugName": data.allopathicO[k[3]],
        "HomeRemedies": data.home_Remedies[k[4]],
        "Dosage": data.dosage[k[5]],
        "DietChart": data.diet_chart[k[6]],
        "YogaNames": data.yoga[k[7]],
    }
    return ans
