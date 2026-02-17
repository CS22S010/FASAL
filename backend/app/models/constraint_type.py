from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class ConstraintTypeModel(Base):
    __tablename__ = "constraint_type"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    signature_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("constraint_signature.id"),
        nullable=False
    )

    signature = relationship("ConstraintSignatureModel")
