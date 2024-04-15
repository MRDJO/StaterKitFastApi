from app.core.base_model_config import BaseModelEntity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class HabilitationModel(BaseModelEntity):
   __tablename__ = 'habilitations'

   libelle=Column(String(255), nullable=False)
   description= Column(String(255))
   roles=relationship("RoleModel", secondary="habilitions_roles", back_populates="habilitations", cascade=("all, delete"))