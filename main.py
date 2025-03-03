# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.IAVectorial import router as ia_vectororial


app = FastAPI()

# Configuración de CORS
origins = [
    "https://copilotasertis.fenalcovalle.com", 
    "https://hey-web.heynowbots.com",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(ia_vectororial)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003)
