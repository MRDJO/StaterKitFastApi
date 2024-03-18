from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.api.auth.services.services_auth import get_current_user
from app.core.database import get_db_dependency
from sqlalchemy.orm import sessionmaker

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login-request-form")

def get_token_and_db_and_user(db:Annotated[sessionmaker, Depends(get_db_dependency)], token: Annotated[str, Depends(oauth2_scheme)]) -> tuple:
   user = get_current_user(token, db)
   return token, db, user