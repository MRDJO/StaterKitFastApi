from datetime import datetime
from typing import Any, Type, TypeVar, cast
import uuid
from pydantic import BaseModel
from sqlalchemy import Column, String, Float, DateTime
from app.core.database import Base

class BaseModelEntity(Base):
   __abstract__ = True

   id=Column(String(255), primary_key=True, unique=True, default=str(uuid.uuid4()))
   createdAt=Column(DateTime, default=datetime.utcnow)
   updatedAt=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   deletedAt=Column(DateTime, nullable=True)
   
class BaseEntitySchema(BaseModel):
   id: int | str
   createdAt: datetime
   updatedAt: datetime

T = TypeVar("T")

def from_str(x: Any) -> str:
   assert isinstance(x, str)
   return x



def to_class(c: Type[T], x: Any) -> dict:
   assert isinstance(x, c)
   return cast(Any, x).to_dict()



def from_float(x: Any) -> float:
   assert isinstance(x, (float, int)) and not isinstance(x, bool)
   return float(x)

def to_float(x: Any) -> float:
   assert isinstance(x, float)
   return x
