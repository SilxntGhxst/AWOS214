#Endpoints varios
import asyncio
from typing import Optional

from fastapi import status, HTTPException, Depends, APIRouter
from app.database.database import usuarios

router = APIRouter(
   tags= ['Varios']
)

@router.get("/")
async def bienvenida():
   return {"mensaje": "Bienvenido a mi API!"}

@router.get("/HolaMundo")
async def hola():
   await asyncio.sleep(4) #simulación de una peticion
   return {
      "mensaje": "Hola mundo FastAPI!",
      "estatus": "200"
      }

@router.get("/v1/ParametroOB/{id}")
async def consultaUno(id:int):
   return {"Se encontro un usuario": id}

@router.get("/v1/ParametroOP/")
async def consultaTodos(id:Optional[int]=None):
   if id is not None:
      for usuario in usuarios:
         if usuario["id"] == id:
            return{"mensaje": "Usuario encontrado", "usuario":usuario}
      return{"mensaje": "Usuario NO encontrado", "usuario":id}
   else:
      return{"mensaje": "No se proporciono id"}

