# app/models/relation_type.py

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class RelationTypeModel(Base):
    __tablename__ = "relation_type"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    parent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("relation_type.id"),
        nullable=True
    )

    signature_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("relation_signature.id"),
        nullable=False
    )

    parent = relationship(
        "RelationTypeModel",
        remote_side=[id],
        backref="children"
    )

    signature = relationship("RelationSignatureModel")
