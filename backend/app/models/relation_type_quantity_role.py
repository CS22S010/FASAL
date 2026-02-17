from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class RelationTypeQuantityRole(Base):
    __tablename__ = "relation_type_quantity_role"

    relation_type_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("relation_type.id"),
        primary_key=True
    )

    quantity_role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("quantity_role.id"),
        primary_key=True
    )
