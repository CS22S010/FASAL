from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class ObjectTypeQuantityRole(Base):
    __tablename__ = "object_type_quantity_role"

    object_type_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("object_type.id"),
        primary_key=True
    )

    quantity_role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("quantity_role.id"),
        primary_key=True
    )
