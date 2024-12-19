# from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import compteController, ticketController, userController, enclosController, adminController, animalController, commentController, biomeController

app = FastAPI()

origins = [
    "http://localhost:3000",  
    "http://localhost:8000",  
   
]

app.add_middleware(
    CORSMiddleware,
     allow_origins=["*"],  # Permettre ces origines
    allow_credentials=True,
    allow_methods=["*"],  # Permettre toutes les méthodes HTTP
    allow_headers=["*"],  # Permettre tous les en-têtes
)

app.include_router(userController.router, prefix="/user", tags=["user"])
app.include_router(compteController.router, prefix="/compte", tags=["compte"])
app.include_router(ticketController.router, prefix="/service", tags=["service"])
app.include_router(enclosController.router, prefix="/enclos", tags=["enclos"])
app.include_router(adminController.router, prefix="/admin", tags=["admin"])
app.include_router(animalController.router, prefix="/animal", tags=["animal"])
app.include_router(commentController.router, prefix="/comment", tags=["comment"])
app.include_router(biomeController.router, prefix="/biome", tags=["biome"])
@app.get("/")
def read_root():
    return {"Hello": "World"}
