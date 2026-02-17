from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class CRelationModel(Base):
    __tablename__ = "crelation"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str | None] = mapped_column(String)

    type_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("constraint_type.id"),
        nullable=False
    )

    constraint_tuple_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tuple.id"),
        nullable=False
    )

    constraint_type = relationship("ConstraintTypeModel")
    constraint_tuple = relationship("TupleModel")
