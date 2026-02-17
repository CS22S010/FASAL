# app/models/quantity_role.py

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class QuantityRoleModel(Base):
    __tablename__ = "quantity_role"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    domain_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("domain.id"),
        nullable=False
    )

    domain = relationship("DomainModel")
