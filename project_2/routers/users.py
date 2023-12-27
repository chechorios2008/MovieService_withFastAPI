from fastapi import APIRouter
from fastapi import HTTPException
from ..database import User
from ..schemas import UserRequestModel
from ..schemas import UserResponse


router = APIRouter(prefix='/users')


@router.post('', response_model=UserResponse)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).first():
        return HTTPException(409, 'El username ya esta en la BD')

    hash_password = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_password
    )

    return user