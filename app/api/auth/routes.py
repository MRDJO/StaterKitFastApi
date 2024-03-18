from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pymysql import IntegrityError
from app.api.auth.models.user_model import UserModel
from app.api.auth.schema.user_schema import UserBase, UserOut, UserIn, UserAuthenticate, UserAuth, UserRefreshTokenIn, UserUpdatePassword
from app.core.database import db_dependency
from app.core.exceptions import not_found_exception
from datetime import datetime, timedelta
from sqlalchemy import exc
from app.api.auth.services.services_auth import create_access_token, get_password_hash, verify_password, refresh_access_token, get_current_user, depend_Auth, oauth2_scheme

routerauth =  APIRouter(
   tags=["User Authentication"],
   prefix = "/api/auth"
)

routeUser = APIRouter(
   tags=["User Crud And Authentication"],
   prefix="/api/users"
)

@routerauth.post("/login-request-form", summary="Authenticate User with Email or Telephone and password Option : REQUEST FORM", response_model=UserAuthenticate, status_code=status.HTTP_200_OK)
async def login_for_access_token(db: db_dependency,form_data: OAuth2PasswordRequestForm = Depends()):
  
   if any(char.isdigit() for char in form_data.username) and len(form_data.username) == 8:
      db_user = db.query(UserModel).filter(UserModel.telephone == form_data.username).first()
   elif "@" in form_data.username and form_data.username.count("@") == 1:
      db_user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
   else:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le format de username est invalide")

   if db_user is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"username ou mot de passe invalid")
   
  
   if verify_password(form_data.password, db_user.password):
      token = create_access_token(db_user)
      
      return UserAuthenticate(
         access_token=token,
         refresh_token=refresh_access_token(db_user),
         token_type="Bearer"
      )
   else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"{type} ou mot de passe invalid")

@routerauth.post("/login-with-json", summary="Authenticate User with Email or Telephone and password OPTION : JSON ", response_model=UserAuthenticate, status_code=status.HTTP_200_OK)
async def authentication_json(db: db_dependency, userAuth: UserAuth):
   if userAuth.telephone is None and userAuth.email is None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Vous devez entrer votre numéro de téléphone")
   type = userAuth.identifier_type

   if type == "telephone":
      db_user = db.query(UserModel).filter(UserModel.telephone == userAuth.telephone).first()
   elif type == "email":
      db_user = db.query(UserModel).filter(UserModel.email == userAuth.email).first()
   else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Type d'identifiant non pris en charge")
   
   if db_user is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"{type} ou mot de passe invalid")
   
   if verify_password(userAuth.password, db_user.password):
      token = create_access_token(db_user)
      return UserAuthenticate(
         access_token=token,
         refresh_token=refresh_access_token(db_user),
         token_type="Bearer"
      )
   else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"{type} ou mot de passe invalid")

@routerauth.post("", summary="Post User Data", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def post_user_data(db: db_dependency, user: UserIn):
   
   try:
      
      existing_user = db.query(UserModel).filter(UserModel.email == user.email or  UserModel.telephone == user.telephone).first()
      
      if existing_user:
         if existing_user.email == user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="L'adresse email existe déjà")
         elif existing_user.telephone == user.telephone:
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le numéro de téléphone existe déjà")

      if user.password is None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le mot de passe est requis")
      
      user_copy = user.model_copy()
      hash_password = get_password_hash(user.password)
      user_copy.password = hash_password
      db_user = UserModel(**user_copy.model_dump())
      db.add(db_user)
      db.commit()
      db.refresh(db_user)
      return db_user
   except Exception as e:
      print("Exception:", type(e).__name__)  # Imprime le type de l'exception déclenchée
      print("Message:", e)
      # Gérer d'autres exceptions ici si nécessaire
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Une erreur interne s'est produite.")

@routerauth.post("/refresh", summary="Refresh User Token", response_model=UserAuthenticate ,status_code=status.HTTP_201_CREATED)
async def refresh_user_token( db: db_dependency , userRefresh: UserRefreshTokenIn):

   user = get_current_user(userRefresh.refresh_token, db)
   if user is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"Refresh token invalid")
   token = create_access_token(user)
      
   return UserAuthenticate(
      access_token=token,
      refresh_token=refresh_access_token(user),
      token_type="Bearer"
   )

@routerauth.get("/me", summary="Get Current user data", response_model=UserOut)
async def get_user(token: depend_Auth , db: db_dependency):
   return get_current_user(token, db)

@routerauth.patch("", summary="Update User Data", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(token: depend_Auth , db: db_dependency, user: UserBase):
   db_user = get_current_user(token, db)

   for field, value in user.model_dump(exclude_unset=True).items():
      setattr(db_user, field, value)
   
   db.commit()
   db.refresh(db_user)

   return db_user

@routerauth.post("/update_password", summary="Update Password for User", )
async def update_password(token: depend_Auth, db: db_dependency, user: UserUpdatePassword):
   db_user = get_current_user(token, db)

   if verify_password(user.old_password, db_user.password):
      hash_password = get_password_hash(user.new_password)
      
      setattr(db_user, "password", hash_password)

      db.commit()
      db.refresh(db_user)
      return {
         "detail":"Mot de passe modifié avec succès"
      }
   
   else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"Ancien Mot de passe incorrect")





# @routerauth.post("/logout", summary="Déconnecter l'utilisateur",status_code=status.HTTP_200_OK)
# async def logout_user(token: depend_Auth , db: db_dependency):
#    oauth2_scheme.revoke_token(token)
#    return {
#       "detail":"Vous êtes déconnecté"
#    }

# @routeUser.get("", summary="Get Current user authenticate")
# async def get_current_user(token: dict = Depends(get_current_user)):
#    return token