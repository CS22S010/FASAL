# app/models/relation_property.py

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class RelationPropertyModel(Base):
    __tablename__ = "relation_property"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
