import jwt

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.hash import bcrypt

from tortoise.contrib.fastapi import register_tortoise

from models import User, UserPydantic, UserInPydantic

app = FastAPI()

oauth2_sceheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = 'myeasypeasyjwtsecret'

async def get_current_user(token: str = Depends(oauth2_sceheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=401,
            detail='Invalid username or password'
        )
    return await UserPydantic.from_tortoise_orm(user)

async def authenticate_user(username: str, password: str):
    # Tortoise ORM is a asyncio library, so we need to use await
    user = await User.get(username=username)
    
    if not user:
        return False
    
    if not user.verify_password(password):
        return False
    
    return user

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        return {"Error": "Invalid username or password"}
    
    user_obj = await UserPydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    
    return {
        "access_token": token,
        "token_type": "Bearer",
    }

@app.post('/users')
async def create_user(user: UserInPydantic):
    user_obj = User(username=user.username, password=bcrypt.hash(user.password))
    
    # Tortoise ORM will automatically save the user object asyncronously
    await user_obj.save()
    
    # Coverting the user to UserPydantic
    return await UserPydantic.from_tortoise_orm(user_obj)


@app.get('/users/me')
async def get_user(current_user: UserPydantic = Depends(get_current_user)):
    return current_user


register_tortoise(
    app=app,
    db_url='sqlite://db.sqlite3',
    modules={
        'models': ['models']
    },
    generate_schemas=True,
    add_exception_handlers=True,
)