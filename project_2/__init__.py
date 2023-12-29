from typing import List
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter

from fastapi.security import OAuth2PasswordRequestForm

from .common import create_access_token
from fastapi import FastAPI
from project_2.database import database as connection
from project_2.database import User
from project_2.database import Movie
from project_2.database import UserReview
from project_2.schemas import ReviewRequestModel
from project_2.schemas import ReviewResponseModel
from project_2.schemas import ReviewRequestPutModel

from .routers import user_router
from .routers import review_router

app = FastAPI(title='Proyecto para reseñar peliculas',
              description='El objetivo es crear programa para reseñar pelis.',
              version="1.0")


api_v1 = APIRouter(prefix='/api/v1')


api_v1.include_router(user_router)
api_v1.include_router(review_router)


@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)

    if user:
        return {
            'access_token': create_access_token(user),
            'token_type': 'bearer'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Username o Password incorrectos',
            headers={'WWW-Authenticate': 'Bearer'}
        ) 


app.include_router(api_v1)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
#Para crear la conexión a las tablas.        
    connection.create_tables([User, Movie, UserReview])


@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()

        print('Closed...')


# async => Para indicar que es una función asincrona. 
@app.get('/')
async def index():
    return 'Hello World again'


@app.get('/about')
async def about():
    return 'Checho it is About you!!!'