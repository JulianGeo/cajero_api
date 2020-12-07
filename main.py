""" Esto es código que se hizo para verificar si los db y modelos sirven
def main():

    print("db:\n")
    print(user_db.database_users)
    print("camilo24:\n")
    print(user_db.get_user("camilo24"))

if __name__ == "__main__":
    main()

@app.get("/")
async def read_root():
    return {"message": "Hello FastAPI"}


@app.get("/users")
async def users():
    return {"message": "Hello users"}
"""

#Código profes

from db.user_db import UserInDB, update_user, get_user
from db.transaction_db import TransactionInDB, save_transaction

from models.user_models import UserIn, UserOut
from models.transaction_models import TransactionIn, TransactionOut

import datetime
from fastapi import FastAPI, HTTPException

#Con esta línea se crea una apiRest, http exception se usa para lanzar los errores
api = FastAPI()

#Modificaciones S11
@api.get("/") 
async def home(): 
    return {"message": "Bienvenido a su cajero de confianza"}

#Función API para autenticar usuario, funcionalidad de la RESTAPI
@api.post("/user/auth/")
async def auth_user(user_in: UserIn):

    user_in_db = get_user(user_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if user_in_db.password != user_in.password:
        return  {"Autenticado": False}

    return  {"Autenticado": True}

#Siempre que es get lo que está en la url {} , debe estar como parámetro en la función {username}=(username)
@api.get("/user/balance/{username}")
async def get_balance(username: str):

    user_in_db = get_user(username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    user_out = UserOut(**user_in_db.dict())

    return  user_out


@api.put("/user/transaction/")
async def make_transaction(transaction_in: TransactionIn):

    user_in_db = get_user(transaction_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if user_in_db.balance < transaction_in.value:
        raise HTTPException(status_code=400, detail="No se tienen los fondos suficientes")

    user_in_db.balance = user_in_db.balance - transaction_in.value
    update_user(user_in_db)

    # ** es para mapear
    transaction_in_db = TransactionInDB(**transaction_in.dict(), actual_balance = user_in_db.balance)
    transaction_in_db = save_transaction(transaction_in_db)

    transaction_out = TransactionOut(**transaction_in_db.dict())

    return  transaction_out
 
