# app/models/value.py

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class ValueModel(Base):
    __tablename__ = "value"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    value: Mapped[str] = mapped_column(String, nullable=False)
