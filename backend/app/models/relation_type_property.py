# app/models/relation_type_property.py

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class RelationTypeProperty(Base):
    __tablename__ = "relation_type_property"

    relation_type_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("relation_type.id"),
        primary_key=True
    )

    property_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("relation_property.id"),
        primary_key=True
    )
