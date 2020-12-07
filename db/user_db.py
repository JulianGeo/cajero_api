import fastapi
from typing import Dict
from pydantic import BaseModel

class UserInDB(BaseModel): #public class UserInDB extends BaseModel (equivalente java)
    username: str # con esto se declaran variables. es equivalente a String username
    password: str
    balance: int

    #Diccionario
database_users = Dict[str, UserInDB]
database_users = {
        #Los * son para cuando no se sabe cuántos parámetros van a llegar a la función
            #A continuación UserInDB es el constructor. 
"camilo24": UserInDB(**{"username":"camilo24",
                        "password":"root",
                        "balance":12000}),
"andres18": UserInDB(**{"username":"andres18",
                         "password":"hola",
                         "balance":34000}),
}


def get_user(username: str):
    if username in database_users.keys():
        return database_users[username]
    else:
        return None
def update_user(user_in_db: UserInDB):
    database_users[user_in_db.username] = user_in_db
    return user_in_db