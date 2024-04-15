from app.core.base_model_config import BaseModelEntity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class RoleModel(BaseModelEntity):
   __tablename__="roles"

   libelle=Column(String(255), nullable=False, unique=True)
   habilitations=relationship("HabilitationModel", secondary="habilitions_roles", back_populates="roles", cascade=("all, delete"))


