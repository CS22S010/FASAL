from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class TupleModel(Base):
    __tablename__ = "tuple"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str | None] = mapped_column(String)
    arity: Mapped[int] = mapped_column(nullable=False)
