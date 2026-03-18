#Seguridad HTTP Basic

from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets

security = HTTPBasic()

def verificar_Peticion(credenciales: HTTPBasicCredentials=Depends(security)):
   userAuth = secrets.compare_digest(credenciales.username, "San Meneses")
   passAuth = secrets.compare_digest(credenciales.password, "123456")
   
   if not(userAuth and passAuth):
      raise HTTPException(
         status_code= status.HTTP_401_UNAUTHORIZED,
         detail= "Credenciales no autorizadas"
      )

   return credenciales.username
