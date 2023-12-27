from typing import Any
from pydantic import BaseModel
from pydantic import validator
from pydantic.utils import GetterDict
from peewee import ModelSelect


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any= None):

        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res


class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be between 3 and 50 characters")

        return username.lower()


class response_model(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserResponseModel(response_model):
    id: int
    username: str

# ---------- Movie ---------


class MovieResponseModel(response_model):
    id: int
    title: str

# ---------- Review ---------


class ReviewValidator():

    @validator('score')
    def score_validator(cls, score):

        if score < 1 or score > 5:
            raise ValueError('El rango para score es de 1 a 5')

        return score


class ReviewRequestModel(BaseModel, ReviewValidator):
    user_id: int
    movie_id: int
    review: str
    score: int


class ReviewResponseModel(response_model):
    id: int
    movie: MovieResponseModel
    review: str
    score: int


class ReviewRequestPutModel(BaseModel, ReviewValidator):
    review: str
    score: int