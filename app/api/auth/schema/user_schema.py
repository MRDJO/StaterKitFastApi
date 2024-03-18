from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel
from app.api.auth.models.user_model import UserModel
from app.core.base_model_config import BaseEntitySchema


class UserBase(BaseModel):
   nom: str | None = None
   prenom: str | None = None
   telephone: int | None = None
   email: str | None = None



class UserOut(BaseEntitySchema):
   nom: str | None = None
   prenom: str | None = None
   telephone: int | None = None
   email: str | None = None



   @staticmethod
   def from_user_model(user_model: UserModel) -> 'UserOut':
      return UserOut(
         id= user_model.id,
         nom=user_model.nom,
         prenom=user_model.prenom,
         telephone=user_model.telephone,
         email=user_model.email,  
         createdAt=user_model.createdAt,
         updatedAt=user_model.updatedAt
      )



class UserIn(UserBase):
   password: str | None = None

class UserRefreshTokenIn(BaseModel):
   refresh_token: str 

class UserUpdatePassword(BaseModel):
   old_password: str
   new_password: str

class UserAuth(BaseModel):
   telephone: int | None = None
   email: str | None = None
   password: str

   @property
   def identifier_type(self) -> Optional[str]:
      if self.telephone is not None:
         return "telephone"
      elif self.email is not None:
         return "email"
      else:
         return None

class UserAuthenticate(BaseModel):
   access_token: str
   refresh_token: str
   token_type: str
