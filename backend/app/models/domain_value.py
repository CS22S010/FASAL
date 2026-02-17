# app/models/domain_value.py

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class DomainValue(Base):
    __tablename__ = "domain_value"

    domain_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("domain.id"),
        primary_key=True
    )

    value_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("value.id"),
        primary_key=True
    )
