#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios

#Instancia del servidor
app = FastAPI(
   title='Mi Primer API',
   description='Santiago Meneses',
   version='1.0.0'
)

app.include_router(usuarios.router)
app.include_router(varios.router)
