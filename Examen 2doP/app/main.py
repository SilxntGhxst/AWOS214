from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from typing import Literal, List, Optional
from datetime import datetime
import secrets

app = FastAPI(
   title='Sistema de tickets de soporte técnico',
   description='Santiago Meneses',
   version='1.0.0'
)

tickets = [
   {"id":1, "usuario":"Juan", "descripcion":"La computadora no enciende", "prioridad":"alta", "estado":"pendiente"},
   {"id":2, "usuario":"Israel", "descripcion":"La impresora no responde al comando de impresión.", "prioridad":"media", "estado":"resuelto"},
   {"id":3, "usuario":"Sofi", "descripcion":"El internet está muy lento.", "prioridad":"baja", "estado":"pendiente"}
]

class Ticket(BaseModel):
    id: int
    usuario: str = Field(..., min_length=5, example="Santiago Meneses")
    description: str = Field(..., min_length=20, max_length=200, example="La impresora no responde al comando de impresión.")
    prioridad: Literal['baja', 'media', 'alta'] = Field(..., example="media") 
    estado: Literal['pendiente', 'resuelto'] = Field(..., example="pendiente")
    
security = HTTPBasic()

def verificar_Peticion(credenciales: HTTPBasicCredentials=Depends(security)):
   userAuth = secrets.compare_digest(credenciales.username, "Soporte")
   passAuth = secrets.compare_digest(credenciales.password, "4321")
   
   if not(userAuth and passAuth):
      raise HTTPException(
         status_code= status.HTTP_401_UNAUTHORIZED,
         detail= "Credenciales no autorizadas"
      )

   return credenciales.username

@app.post("/tickets", status_code=status.HTTP_201_CREATED, response_model=Ticket)
async def crear_ticket(ticket: Ticket):
      for tckt in tickets:
         if tckt["id"] == ticket.id:
            raise HTTPException(
               status_code=400,
               detail="El id ya existe"
            )
      tickets.append(ticket.model_dump())
      return{
      "mensaje":"Ticket Agregado",
   }

@app.get("/tickets", response_model=List[Ticket])
async def obtener_tickets():
   return{
      "status":"200",
      "total": len(tickets),
      "tickets":tickets
      }

@app.get("/tickets/{ticket_id}", response_model=Ticket, status_code=status.HTTP_200_OK, )
async def obtener_ticket(ticket_id: int, userAuth: str = Depends(verificar_Peticion)):
   for tckt in tickets:
      if tckt["id"] == ticket_id:
         return tckt
   raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Ticket no encontrado"
   )
