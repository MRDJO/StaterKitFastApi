import datetime
from app.core.base_model_config import BaseModelEntity
from sqlalchemy import Column, Integer, ForeignKey, DateTime

from app.core.database import Base

class HabilitionRole(Base):
   __tablename__ = 'habilitions_roles'


   role_id=Column(Integer,ForeignKey("roles.id"),  primary_key=True, )
   habiliation_id=Column(Integer,ForeignKey("habilitations.id"),  primary_key=True,)
   createdAt=Column(DateTime, default=datetime.utcnow)
   updatedAt=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   deletedAt=Column(DateTime, nullable=True)