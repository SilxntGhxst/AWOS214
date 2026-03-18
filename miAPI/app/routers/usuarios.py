
#Endpoints de ususarios

from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.database.database import usuarios
from app.security.auth import verificar_Peticion

router = APIRouter(
   prefix="/v1/usuarios", 
   tags=['CRUD HTTP']
   )

@router.get("/")
async def leer_Usuarios():
   return{
      "status":"200",
      "total": len(usuarios),
      "usuarios":usuarios
   }
   
@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.put("/{id}")
async def actualizar_Usuario(id: int, usuario_actualizado: dict):
   for index, usr in enumerate(usuarios): 
      if usr["id"] == id:
         usuarios[index].update(usuario_actualizado)
         return {"mensaje": "Usuario actualizado", "usuario": usuarios[index]}
    
   return {"mensaje": "Usuario no encontrado", "id": id}
 
@router.delete("/{id}")
async def eliminar_Usuario(id: int, userAuth= Depends(verificar_Peticion)):
   for index, usr in enumerate(usuarios):
      if usr["id"] == id:
         usuario_eliminado = usuarios.pop(index)
         return {"mensaje": f"Usuario eliminado correctamente {userAuth}"}
   return {"mensaje": "Usuario no encontrado", "id": id}

