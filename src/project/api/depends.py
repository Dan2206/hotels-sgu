from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.repository.hotel_repo import HotelRepository
from project.infrastructure.postgres.repository.room_repo import RoomRepository
from project.infrastructure.postgres.repository.room_type_book_repo import RoomTypeBookRepository
from project.infrastructure.postgres.repository.room_type_repo import RoomTypeRepository
from project.infrastructure.postgres.repository.price_repo import PriceRepository
from project.infrastructure.postgres.repository.buyer_repo import BuyerRepository
from project.infrastructure.postgres.repository.booking_repo import BookingRepository
from project.infrastructure.postgres.repository.booking_client_repo import BookingClientRepository
from project.infrastructure.postgres.repository.residence_repo import ResidenceRepository
from project.infrastructure.postgres.repository.residence_client_repo import ResidenceClientRepository
from project.infrastructure.postgres.repository.service_repo import ServiceRepository
from project.infrastructure.postgres.repository.service_rendered_repo import ServiceRenderedRepository
from project.infrastructure.postgres.repository.price_service_repo import PriceServiceRepository
from project.infrastructure.postgres.database import PostgresDatabase

client_repo = ClientRepository()
hotel_repo = HotelRepository()
room_repo = RoomRepository()
room_type_book_repo = RoomTypeBookRepository()
room_type_repo = RoomTypeRepository()
price_repo = PriceRepository()
buyer_repo = BuyerRepository()
booking_repo = BookingRepository()
booking_client_repo = BookingClientRepository()
residence_repo = ResidenceRepository()
residence_client_repo = ResidenceClientRepository()
service_repo = ServiceRepository()
service_rendered_repo = ServiceRenderedRepository()
price_service_repo = PriceServiceRepository()
database = PostgresDatabase()
