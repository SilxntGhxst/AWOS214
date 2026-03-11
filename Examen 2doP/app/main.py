from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from typing import Literal, List
import secrets

app = FastAPI(
   title='Sistema de tickets de soporte técnico',
   description='Santiago Meneses',
   version='1.0.0'
)

tickets = [
   {"ticket_id":1, "usuario":"Juan Gutierrez", "descripcion":"La computadora no enciende", "prioridad":"alta", "estado":"pendiente"},
   {"ticket_id":2, "usuario":"Israel Gomez", "descripcion":"La impresora no responde al comando de impresión.", "prioridad":"media", "estado":"resuelto"},
   {"ticket_id":3, "usuario":"Sofia Alvarez", "descripcion":"El internet está muy lento.", "prioridad":"baja", "estado":"pendiente"}
]

class Ticket(BaseModel):
    ticket_id: int
    usuario: str = Field(..., min_length=5, example="Santiago Meneses")
    descripcion: str = Field(..., min_length=20, max_length=200, example="La impresora no responde al comando de impresión.")
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

@app.post("/v1/Tickets/", status_code=status.HTTP_201_CREATED)
async def crear_ticket(ticket: Ticket):
      for tckt in tickets:
         if tckt["id"] == ticket.ticket_id:
            raise HTTPException(
               status_code=400,
               detail="El id ya existe"
            )
      tickets.append(ticket.model_dump())
      return{
      "mensaje":"Ticket Agregado",
   }

@app.get("/v1/Tickets/", status_code=status.HTTP_200_OK)
async def obtener_tickets():
   return{
      "status":"200",
      "total": len(tickets),
      "tickets":tickets
      }

@app.get("/v1/Tickets/{ticket_id}", status_code=status.HTTP_200_OK, )
async def obtener_ticket(ticket_id: int, userAuth: str = Depends(verificar_Peticion)):
   for tckt in tickets:
      if tckt["id"] == ticket_id:
         return tckt
   raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Ticket no encontrado"
   )

@app.put("/v1/Tickets/estado/{ticket_id}", status_code=status.HTTP_200_OK)
async def cambiar_estado_ticket(ticket_id: int, ticket: Ticket, userAuth: str = Depends(verificar_Peticion)):
   for i, tckt in enumerate(tickets):
      if tckt["id"] == ticket_id:
         tickets[i] = ticket.model_dump()
         return ticket
   raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Ticket no encontrado"
   )


@app.delete("/v1/Tickets/{ticket_id}", status_code=status.HTTP_200_OK)
async def eliminar_ticket(ticket_id: int):
   for i, tckt in enumerate(tickets):
      if tckt["id"] == ticket_id:
         if tckt["estado"] == "resuelto":
            raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Solo se pueden eliminar tickets pendientes"
            )
         
         del tickets[i]
         return{
            "mensaje":"Ticket Eliminado"
         }
   raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Ticket no encontrado"
   )
