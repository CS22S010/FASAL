# app/models/object_type.py

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class ObjectTypeModel(Base):
    __tablename__ = "object_type"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("object_type.id"),
        nullable=True
    )

    parent: Mapped["ObjectTypeModel"] = relationship(
        "ObjectTypeModel",
        remote_side=[id],
        backref="children"
    )
