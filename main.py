from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from model import User, UserLogin, UserCreate
from database import MongoDB
import uvicorn
from fastapi.security import OAuth2PasswordBearer
from fastapi_login.exceptions import InvalidCredentialsException
from pymongo import MongoClient
from Shoebox import rs_system

# from pydantic import BaseModel
import pydantic
from bson import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

app = FastAPI()
security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
mongo = MongoDB('mongodb+srv://aistudio_3jo:a1234567@userdata.routxa4.mongodb.net/?retryWrites=true&w=majority', 'data')

@app.get('/userlist')
def load_user():
   user_list = mongo.load_user() 
   return {'result': user_list}

@app.post('/login')
async def login(user: UserLogin):
    user_id = user.id
    user_password = user.password
    db_user = mongo.load_user_id(user_id) 
    if db_user is None or not mongo.verify_password(user_password, db_user['password']):
        raise HTTPException(status_code=400, detail='Invalid username or password')
    return {'message: User successfully logged in'}
    # return {'access_token': user_id, 'token_type': 'bearer'}

@app.post('/signup', status_code=201)
async def signup(user: UserCreate):
    already_user = mongo.load_user_id(user.id)
    if already_user:
        raise HTTPException(status_code=400, detail='Username is already taken')
    hashed_password = mongo.hash_password(user.password)
    mongo.create_user(user.userName, user.age, user.gender, user.email, user.id, hashed_password, user.shoesSizes)
    return {'message': 'User successfully created'}

@app.get('/user/')
async def load_userId(user_id: int):
    user_data = mongo.load_user_userID(user_id)
    return user_data

@app.post('/review/')
async def review(id: int, brand: str, size: int):
    return mongo.update_size(id=id, brand=brand, size=size)

@app.post('/user/recom/')
async def size_recommend(id:int, brand: str):
    data = mongo.load_user()
    size = rs_system(data, id, brand)
    mongo.update_size(id=id, brand=brand, size=size)
    return rs_system(data, id, brand)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)