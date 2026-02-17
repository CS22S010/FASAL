from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class ConstraintSignatureDomain(Base):
    __tablename__ = "constraint_signature_domain"

    constraint_signature_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("constraint_signature.id"),
        primary_key=True
    )

    position: Mapped[int] = mapped_column(primary_key=True)

    domain_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("domain.id"),
        nullable=False
    )
