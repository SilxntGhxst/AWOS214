#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios

#Instancia del servidor
app = FastAPI(
   title='API con JWT',
   description='Santiago Meneses',
   version='1.0.0'
)

app.include_router(varios.router)
app.include_router(usuarios.router)
