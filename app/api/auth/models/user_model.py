from enum import Enum
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.base_model_config import BaseModelEntity

class UserModel(BaseModelEntity):

   __tablename__ = "users"
   
   nom=Column(String(30))
   prenom=Column(String(50))
   email=Column(String(30), unique=True , nullable=True)
   password=Column(String(255))
   telephone=Column(Integer, unique=True, nullable=True)
   role=relationship("RoleModel", )
  