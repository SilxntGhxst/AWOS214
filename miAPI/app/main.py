#Importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field



#Instancia del servidor
app = FastAPI(
   title='Mi Primer API',
   description='Santiago Meneses',
   version='1.0.0'
)

#TB ficticia
usuarios=[
   {"id":1, "nombre":"Juan", "edad":21},
   {"id":2, "nombre":"Israel", "edad":21},
   {"id":3, "nombre":"Sofi", "edad":21}
]

class usuario_create(BaseModel):
   id: int = Field(..., gt=0, description="Identificador de usuario")
   nombre: str= Field(..., min_length=3, max_length=50, example="Juanita")
   edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")
   

@app.get("/", tags=['Inicio'])
async def bienvenida():
   return {"mensaje": "Bienvenido a mi API!"}

@app.get("/HolaMundo", tags=['Bienvenida Asincrona'])
async def hola():
   await asyncio.sleep(4) #simulación de una peticion
   return {
      "mensaje": "Hola mundo FastAPI!",
      "estatus": "200"
      }

@app.get("/v1/ParametroOB/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
   return {"Se encontro un usuario": id}

@app.get("/v1/ParametroOP/", tags=['Parametro Opcional'])
async def consultaTodos(id:Optional[int]=None):
   if id is not None:
      for usuario in usuarios:
         if usuario["id"] == id:
            return{"mensaje": "Usuario encontrado", "usuario":usuario}
      return{"mensaje": "Usuario NO encontrado", "usuario":id}
   else:
      return{"mensaje": "No se proporciono id"}


@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_Usuarios():
   return{
      "status":"200",
      "total": len(usuarios),
      "usuarios":usuarios
   }
   
@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_Usuario(usuario:usuario_create):
   for usr in usuarios:
      if usr["id"] == usuario.id:
         raise HTTPException(
            status_code=400,
            detail="El id ya existe"
         )
   usuarios.append(usuario)
   return{
      "mensaje":"Usuario Agregado",
      "Usuario":usuario
   }


@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_Usuario(id: int, usuario_actualizado: dict):
   for index, usr in enumerate(usuarios): 
      if usr["id"] == id:
         usuarios[index].update(usuario_actualizado)
         return {"mensaje": "Usuario actualizado", "usuario": usuarios[index]}
    
   return {"mensaje": "Usuario no encontrado", "id": id}
 
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_Usuario(id: int):
   for index, usr in enumerate(usuarios):
      if usr["id"] == id:
         usuario_eliminado = usuarios.pop(index)
         return {"mensaje": "Usuario eliminado", "usuario": usuario_eliminado}
   return {"mensaje": "Usuario no encontrado", "id": id}

