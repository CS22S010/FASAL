# app/models/relation_signature.py

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class RelationSignatureModel(Base):
    __tablename__ = "relation_signature"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    object_type1_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("object_type.id"),
        nullable=False
    )

    object_type2_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("object_type.id"),
        nullable=False
    )

    object_type1 = relationship("ObjectTypeModel", foreign_keys=[object_type1_id])
    object_type2 = relationship("ObjectTypeModel", foreign_keys=[object_type2_id])
