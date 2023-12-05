import uuid
from sqlalchemy import Column, String
from app.api.core.database import Base


class Users(Base):
   __tablename__="utilisateurs"

   idUser=Column(String(255), primary_key=True, unique=True, default=str(uuid.uuid4()))