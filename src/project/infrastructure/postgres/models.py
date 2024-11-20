from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime
from sqlalchemy import UniqueConstraint, ForeignKey, String, CheckConstraint, Text
from sqlalchemy.sql import func

from project.infrastructure.postgres.database import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    type_of_document: Mapped[str] = mapped_column(String(50), nullable=False)
    document: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_reg: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=True)

    unique_document_constraint = 'unique_document'
    unique_email_constraint = 'unique_email'
    __table_args__ = (
        UniqueConstraint('document', 'type_of_document', name=unique_document_constraint),
        UniqueConstraint('email', name=unique_email_constraint)
    )


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    stars: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        CheckConstraint("stars >= 0 AND stars <= 5"),
    )


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_num: Mapped[int] = mapped_column(nullable=False)
    hotel: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE", onupdate="CASCADE"),
                                       nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("hotel", "room_num", name="uq_hotel_room"),
    )


class RoomTypeBook(Base):
    __tablename__ = "room_types_book"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    places: Mapped[int] = mapped_column(nullable=False)
    square: Mapped[int] = mapped_column(nullable=False)
    extra_places: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class RoomType(Base):
    __tablename__ = "room_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    room: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"),
                                      nullable=False)
    category: Mapped[int] = mapped_column(ForeignKey("room_types_book.id",
                                                     ondelete="CASCADE", onupdate="CASCADE"),
                                          nullable=False)
    date_of_start: Mapped[date] = mapped_column(nullable=False)
    date_of_end: Mapped[date] = mapped_column(nullable=False)


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE", onupdate="CASCADE"),
                                       nullable=False)
    category: Mapped[int] = mapped_column(ForeignKey("room_types_book.id",
                                                     ondelete="CASCADE", onupdate="CASCADE"),
                                          nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    date_of_start: Mapped[date] = mapped_column(nullable=False)
    date_of_end: Mapped[date] = mapped_column(nullable=False)

    __table_args__ = (
        CheckConstraint("price > 0"),
        CheckConstraint("date_of_end >= date_of_start"),
    )


class Buyer(Base):
    __tablename__ = "buyers"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_company: Mapped[bool] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel: Mapped[int] = mapped_column(ForeignKey("hotels.id",
                                                  ondelete="CASCADE", onupdate="CASCADE"),
                                       nullable=False)
    room_type: Mapped[int] = mapped_column(ForeignKey("room_types_book.id",
                                                      ondelete="CASCADE", onupdate="CASCADE"),
                                           nullable=False)
    who_buy: Mapped[int] = mapped_column(ForeignKey("buyers.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False)
    main_client: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE", onupdate="CASCADE"),
                                             nullable=False)
    date_of_booking: Mapped[datetime] = mapped_column(nullable=False)
    date_of_start: Mapped[date] = mapped_column(nullable=False)
    date_of_end: Mapped[date] = mapped_column(nullable=False)
    extra: Mapped[str] = mapped_column(String(500), nullable=True)
    reason_cancel: Mapped[str] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        CheckConstraint("date_of_end > date_of_start"),
    )


class BookingClient(Base):
    __tablename__ = "bookings_clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False)
    client: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE", onupdate="CASCADE"),
                                        nullable=False)


class Residence(Base):
    __tablename__ = "residences"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE", onupdate="CASCADE"),
                                       nullable=False)
    room: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"),
                                      nullable=False)
    main_client: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE", onupdate="CASCADE"),
                                             nullable=False)
    who_buy: Mapped[int] = mapped_column(ForeignKey("buyers.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False)
    booking: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=True)
    date_of_start: Mapped[date] = mapped_column(nullable=False)
    date_of_end: Mapped[date] = mapped_column(nullable=False)
    sum_price: Mapped[int] = mapped_column(nullable=True)

    __table_args__ = (
        CheckConstraint("date_of_end > date_of_start"),
    )


class ResidenceClient(Base):
    __tablename__ = "residences_clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    residence: Mapped[int] = mapped_column(ForeignKey("residences.id", ondelete="CASCADE", onupdate="CASCADE"),
                                           nullable=False)
    client: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE", onupdate="CASCADE"),
                                        nullable=False)


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    hotel: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE", onupdate="CASCADE"),
                                       nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("hotel", "name"),
    )


class ServiceRendered(Base):
    __tablename__ = "services_rendered"

    id: Mapped[int] = mapped_column(primary_key=True)
    service: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False)
    client: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE", onupdate="CASCADE"),
                                        nullable=False)
    is_rendered: Mapped[bool] = mapped_column(nullable=False)
    date_of_render: Mapped[datetime] = mapped_column(nullable=False)


class PriceService(Base):
    __tablename__ = "prices_services"

    id: Mapped[int] = mapped_column(primary_key=True)
    service: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False)
    date_of_start: Mapped[date] = mapped_column(nullable=False)
    date_of_end: Mapped[date] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        CheckConstraint("date_of_end > date_of_start"),
        CheckConstraint("price > 0"),
    )
