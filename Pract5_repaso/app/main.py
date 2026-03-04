from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import Literal, List
from datetime import datetime

Pract5 = FastAPI(
   title='Practica de repaso & POSTMAN',
   description='Santiago Meneses',
   version='1.0.0'
)

usuarios = [
    {"id_usuario": 1, "nombre_usuario": "Santiago Meneses", "correo_usuario": "santiago@correo.com", "libros_prestados": [101]},
    {"id_usuario": 2, "nombre_usuario": "Ana Garcia", "correo_usuario": "ana@correo.com", "libros_prestados": [102]},
    {"id_usuario": 3, "nombre_usuario": "Luis Perez", "correo_usuario": "luis@correo.com", "libros_prestados": [103]},
    {"id_usuario": 4, "nombre_usuario": "Maria Lopez", "correo_usuario": "maria@correo.com", "libros_prestados": [104]},
    {"id_usuario": 5, "nombre_usuario": "Carlos Ruiz", "correo_usuario": "carlos@correo.com", "libros_prestados": [105]}
]

libros = [
    {"id_libro": 101, "nombre_libro": "Ingenieria de Software", "autor": "Ian Sommerville", "año": 2015, "paginas": 400, "estado": "prestado"},
    {"id_libro": 102, "nombre_libro": "Clean Code", "autor": "Robert C. Martin", "año": 2008, "paginas": 464, "estado": "prestado"},
    {"id_libro": 103, "nombre_libro": "El Quijote", "autor": "Miguel de Cervantes", "año": 1605, "paginas": 863, "estado": "prestado"},
    {"id_libro": 104, "nombre_libro": "Cien Años de Soledad", "autor": "Gabriel Garcia Marquez", "año": 1967, "paginas": 417, "estado": "prestado"},
    {"id_libro": 105, "nombre_libro": "1984", "autor": "George Orwell", "año": 1949, "paginas": 328, "estado": "prestado"}
]

prestamos = [
    {"id_libro": 101, "id_usuario": 1},
    {"id_libro": 102, "id_usuario": 2},
    {"id_libro": 103, "id_usuario": 3},
    {"id_libro": 104, "id_usuario": 4},
    {"id_libro": 105, "id_usuario": 5}
]

año_actual = datetime.now().year

class UsuarioCreate(BaseModel):
   id_usuario: int = Field(..., gt=0)
   nombre_usuario: str = Field(..., min_length=2, max_length=50)
   correo_usuario: EmailStr
   libros_prestados: List[int] = []

class LibroCreate(BaseModel):
   id_libro: int = Field(..., gt=0)
   nombre_libro: str = Field(..., min_length=2, max_length=100)
   autor: str = Field(..., min_length=1, max_length=60)
   año: int = Field(..., gt=1450, le=año_actual)
   paginas: int = Field(..., gt=1)
   estado: Literal["disponible", "prestado"]

class PrestamoCreate(BaseModel):
   id_libro: int = Field(..., gt=0)
   id_usuario: int = Field(..., gt=0)

@Pract5.post("/v1/usuarios/", tags=['Usuarios'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate):
   for usu in usuarios:
      if usu["id_usuario"] == usuario.id_usuario or usu["correo_usuario"] == usuario.correo_usuario:
         raise HTTPException(status_code=400, detail="El ID o correo ya está registrado")
   
   usuarios.append(usuario.model_dump())
   return {"mensaje": "Usuario creado exitosamente", "Usuario": usuario}

@Pract5.get("/v1/usuarios/", tags=['Usuarios'], status_code=status.HTTP_200_OK)
async def listar_usuarios():
   if len(usuarios) > 0:
      return {"Usuarios registrados": usuarios}
   return {"mensaje": "No hay usuarios registrados"}

@Pract5.get("/v1/prestamo/", tags=['Préstamos'], status_code=status.HTTP_200_OK)
async def listar_usuarios():
   if len(prestamos) > 0:
      return {"Prestamos registrados": prestamos}
   return {"mensaje": "No hay prestamos registrados"}

@Pract5.get("/v1/libros/", tags=['Libros'], status_code=status.HTTP_200_OK)
async def listar_libros():
   if len(libros) > 0:
      return {"Libros registrados": libros}
   return {"mensaje": "No hay libros registrados"}

@Pract5.post("/v1/libros/", tags=['Libros'], status_code=status.HTTP_201_CREATED)
async def crear_libro(libro: LibroCreate):
   for lib in libros:
      if lib["id_libro"] == libro.id_libro:
         raise HTTPException(status_code=400, detail="El id ya existe")
   
   libros.append(libro.model_dump())
   return {"mensaje": "Libro Agregado", "Libro": libro}

@Pract5.get("/v1/libros/disponibles", tags=['Libros'], status_code=status.HTTP_200_OK)
async def mostrar_libros_disponibles():
   libros_disponibles = []
   for lib in libros:
      if lib["estado"] == "disponible":
         libros_disponibles.append(lib)
         
   if len(libros_disponibles) > 0:
      return {"libros disponibles": libros_disponibles}
   return {"mensaje": "No hay libros disponibles"}

@Pract5.get("/v1/libros/buscar/{nombre_libro}", tags=['Libros'], status_code=status.HTTP_200_OK)
async def buscar_libro(nombre_libro: str):
   for lib in libros:
      if lib["nombre_libro"].lower() == nombre_libro.lower():
         return {"Libro encontrado": lib}
         
   raise HTTPException(status_code=400, detail="Nombre de libro no válido o no encontrado")

@Pract5.post("/v1/prestamos/", tags=['Préstamos'], status_code=status.HTTP_201_CREATED)
async def registrar_prestamo(prestamo: PrestamoCreate):
   usuario_encontrado = None
   for usu in usuarios:
      if usu["id_usuario"] == prestamo.id_usuario:
         usuario_encontrado = usu
         break
         
   if not usuario_encontrado:
      raise HTTPException(status_code=400, detail="Solicitud incorrecta: El usuario no existe")

   for lib in libros:
      if lib["id_libro"] == prestamo.id_libro:
         if lib["estado"] == "prestado":
            raise HTTPException(status_code=409, detail="Conflicto: El libro ya está prestado")
            
         lib["estado"] = "prestado"
         usuario_encontrado["libros_prestados"].append(prestamo.id_libro)
         prestamos.append(prestamo.model_dump())
         return {"mensaje": "Préstamo registrado exitosamente", "prestamo": prestamo}
         
   raise HTTPException(status_code=400, detail="Solicitud incorrecta: Faltan datos o el libro no existe")

@Pract5.put("/v1/prestamos/devolver/{id_libro}", tags=['Préstamos'], status_code=status.HTTP_200_OK)
async def devolver_libro(id_libro: int):
   for prestamo in prestamos:
      if prestamo["id_libro"] == id_libro:
         
         for lib in libros:
            if lib["id_libro"] == id_libro:
               lib["estado"] = "disponible"
               
         for usu in usuarios:
            if usu["id_usuario"] == prestamo["id_usuario"]:
               if id_libro in usu["libros_prestados"]:
                  usu["libros_prestados"].remove(id_libro)
                  
         prestamos.remove(prestamo)
         return {"mensaje": "Libro devuelto con éxito"}
               
   raise HTTPException(status_code=409, detail="Conflicto: El registro de préstamo ya no existe")

@Pract5.delete("/v1/prestamos/{id_libro}", tags=['Préstamos'], status_code=status.HTTP_200_OK)
async def eliminar_prestamo(id_libro: int):
   for prestamo in prestamos:
      if prestamo["id_libro"] == id_libro:
         
         for usu in usuarios:
            if usu["id_usuario"] == prestamo["id_usuario"]:
               if id_libro in usu["libros_prestados"]:
                  usu["libros_prestados"].remove(id_libro)
                  
         prestamos.remove(prestamo)
         return {"mensaje": "Registro de préstamo eliminado correctamente"}
         
   raise HTTPException(status_code=409, detail="Conflicto: El registro de préstamo ya no existe")