from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from optimizer import run_optimizer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

class HU(BaseModel):
    id: int
    importancia: int
    criticidade: int
    impacto: int
    custo: int

class OptimizationRequest(BaseModel):
    requisitos: List[HU]
    num_sprints: int
    limite_custo: int

@app.post("/otimizar")
def otimizar(req: OptimizationRequest):
    h_us_dict = [hu.dict() for hu in req.requisitos]
    resultado = run_optimizer(
        h_us=h_us_dict,
        num_sprints=req.num_sprints,
        limite_custo=req.limite_custo
    )
    return resultado
