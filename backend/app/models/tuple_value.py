from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class TupleValue(Base):
    __tablename__ = "tuple_value"

    tuple_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tuple.id"),
        primary_key=True
    )

    position: Mapped[int] = mapped_column(primary_key=True)

    value_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("value.id"),
        nullable=False
    )
