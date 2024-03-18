from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.api.auth.models.user_model import UserModel
from jose import JWTError, jwt
from fastapi import Header

from app.core.exceptions import not_found_exception

SECRET_KEY="KeySecretForsjwC53h4jiH7ruMTlYd8K0t4bVCDFS2v"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 2880

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login-request-form")

depend_Auth = Annotated[str, Depends(oauth2_scheme)]

def verify_password(plain_password, hashed_password):
   return pwd_content.verify(plain_password, hashed_password)

def get_password_hash(password):
   return pwd_content.hash(password)


def create_access_token(db_user: UserModel, plain_password: str | None = None):

   if db_user.email is None:
      encode = {'sub': str(db_user.telephone), "id": db_user.id, "role":db_user.role}
   else:
      # CETTE PARTIE DU CODE EST A MODIFIER LORSQUE SERA RAJOUTER LA CLASSE ROLE
      encode = {'sub': db_user.email, "id": db_user.id, "role":"USER"}
   # print(encode)
   expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   encode.update({'exp': expires})
   return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def refresh_access_token(db_user: UserModel):
   if db_user.email is None:
      encode = {'sub': db_user.telephone, "id": db_user.id, "role":db_user.role}
   else:
      # CETTE PARTIE DU CODE EST A MODIFIER LORSQUE SERA RAJOUTER LA CLASSE ROLE
      encode = {'sub': db_user.email, "id": db_user.id, "role":"USER"}
   expires = datetime.utcnow() + timedelta(days=7)
   encode.update({'exp': expires})
   return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db_user(id: int, db) -> UserModel:
   db_user = db.query(UserModel).filter(UserModel.id == id).first()
   if db_user is None:
      raise not_found_exception(detail=f"Aucune charge ne correspond à l'id '{id}'")
   return db_user 



async def header_token(authorization: str = Header(...)):
    if not authorization or not authorization.startswith("Bearer "):
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Invalid authorization header",
         headers={"WWW-Authenticate": "Bearer"},
      )
    token = authorization.replace("Bearer ", "")
    return token

def get_current_user(token: str, db):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_or_tel = payload.get("sub")
        user_id = payload.get("id")
        if email_or_tel is None or user_id is None:
           raise credentials_exception
        db_user = get_db_user(user_id, db)
        if db_user is None:
           raise credentials_exception
        return db_user
 
    except JWTError:
        raise credentials_exception
