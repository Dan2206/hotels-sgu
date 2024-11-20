from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.database import PostgresDatabase


client_repo = ClientRepository()
database = PostgresDatabase()