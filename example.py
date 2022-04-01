from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_sceheme = OAuth2PasswordBearer(tokenUrl="token")

# This endpoint will take credentials and return a JWT token if the credentials are valid
@app.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username + 'token' }


# This endpoint asks for user credentials
# Then it will get a JWT token and return the user's token if it is valid
@app.get('/')
def index(token: str = Depends(oauth2_sceheme)):
    return {"token": token}