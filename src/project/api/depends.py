from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.repository.hotel_repo import HotelRepository
from project.infrastructure.postgres.repository.room_repo import RoomRepository
from project.infrastructure.postgres.database import PostgresDatabase


client_repo = ClientRepository()
hotel_repo = HotelRepository()
room_repo = RoomRepository()
database = PostgresDatabase()