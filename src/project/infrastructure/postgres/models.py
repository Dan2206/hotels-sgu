from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime
from sqlalchemy import UniqueConstraint

from project.infrastructure.postgres.database import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    surname: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column(nullable=False)
    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    type_of_document: Mapped[str] = mapped_column(nullable=False)
    document: Mapped[str] = mapped_column(nullable=False)
    date_of_reg: Mapped[datetime] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    __table_args__ = (
        UniqueConstraint('document', 'type_of_document'),
    )