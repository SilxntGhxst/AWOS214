
#Endpoints de ususarios

from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.database.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.usuario import Usuario as usuarioDB

router = APIRouter(
   prefix="/v1/usuarios", 
   tags=['CRUD HTTP']
   )

@router.get("/")
async def leer_Usuarios(db: Session = Depends(get_db)):
   queryUsers= db.query(usuarioDB).all()
   return{
      "status":"200",
      "total": len(queryUsers),
      "usuarios":queryUsers
   }
   
@router.post("/", status_code=status.HTTP_201_CREATED)#agregar
async def crear_usuario(usuarioP: usuario_create, db: Session = Depends(get_db)):
    nuevo_usuario = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario agendado",
        "Usuario": usuarioP
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

