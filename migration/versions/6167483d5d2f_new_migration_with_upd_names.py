"""new migration with upd names

Revision ID: 6167483d5d2f
Revises: a190b8aed674
Create Date: 2024-11-28 01:26:04.457535

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = '6167483d5d2f'
down_revision = 'a190b8aed674'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buyers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_company', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('surname', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('patronymic', sa.String(length=100), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('type_of_document', sa.String(length=50), nullable=False),
    sa.Column('document', sa.String(length=50), nullable=False),
    sa.Column('date_of_reg', sa.DateTime(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('document', 'type_of_document', name='unique_document'),
    sa.UniqueConstraint('email', name='unique_email'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=False),
    sa.Column('stars', sa.Integer(), nullable=False),
    sa.CheckConstraint('stars >= 0 AND stars <= 5', name='check_stars'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', name='unique_name'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('room_types_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('places', sa.Integer(), nullable=False),
    sa.Column('square', sa.Integer(), nullable=False),
    sa.Column('extra_places', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel', sa.Integer(), nullable=False),
    sa.Column('room_type', sa.Integer(), nullable=False),
    sa.Column('who_buy', sa.Integer(), nullable=False),
    sa.Column('main_client', sa.Integer(), nullable=False),
    sa.Column('date_of_booking', sa.DateTime(timezone=True), nullable=False),
    sa.Column('date_of_start', sa.Date(), nullable=False),
    sa.Column('date_of_end', sa.Date(), nullable=False),
    sa.Column('extra', sa.String(length=500), nullable=True),
    sa.Column('reason_cancel', sa.String(length=500), nullable=True),
    sa.CheckConstraint('date_of_end > date_of_start', name='date_comp_constraint'),
    sa.ForeignKeyConstraint(['hotel'], ['hotels_schema.hotels.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['main_client'], ['hotels_schema.clients.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['room_type'], ['hotels_schema.room_types_book.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['who_buy'], ['hotels_schema.buyers.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel', sa.Integer(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('date_of_start', sa.Date(), nullable=False),
    sa.Column('date_of_end', sa.Date(), nullable=False),
    sa.CheckConstraint('date_of_end >= date_of_start', name='check_date_constraint'),
    sa.CheckConstraint('price > 0', name='check_price_constraint'),
    sa.ForeignKeyConstraint(['category'], ['hotels_schema.room_types_book.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['hotel'], ['hotels_schema.hotels.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_num', sa.Integer(), nullable=False),
    sa.Column('hotel', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['hotel'], ['hotels_schema.hotels.id'], name='fkey_rooms_hotels', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hotel', 'room_num', name='unique_room_num'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('hotel', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['hotel'], ['hotels_schema.hotels.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hotel', 'name', name='unique_hotel_name_constraint'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('bookings_clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('booking', sa.Integer(), nullable=False),
    sa.Column('client', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking'], ['hotels_schema.bookings.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['client'], ['hotels_schema.clients.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('prices_services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service', sa.Integer(), nullable=False),
    sa.Column('date_of_start', sa.Date(), nullable=False),
    sa.Column('date_of_end', sa.Date(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.CheckConstraint('date_of_end > date_of_start', name='check_date_service_constraint'),
    sa.CheckConstraint('price > 0', name='check_price_service_constraint'),
    sa.ForeignKeyConstraint(['service'], ['hotels_schema.services.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('residences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel', sa.Integer(), nullable=False),
    sa.Column('room', sa.Integer(), nullable=False),
    sa.Column('main_client', sa.Integer(), nullable=False),
    sa.Column('who_buy', sa.Integer(), nullable=False),
    sa.Column('booking', sa.Integer(), nullable=True),
    sa.Column('date_of_start', sa.Date(), nullable=False),
    sa.Column('date_of_end', sa.Date(), nullable=False),
    sa.Column('sum_price', sa.Integer(), nullable=True),
    sa.CheckConstraint('date_of_end > date_of_start', name='date_comp_residences_constraint'),
    sa.ForeignKeyConstraint(['booking'], ['hotels_schema.bookings.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['hotel'], ['hotels_schema.hotels.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['main_client'], ['hotels_schema.clients.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['room'], ['hotels_schema.rooms.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['who_buy'], ['hotels_schema.buyers.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('room_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room', sa.Integer(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.Column('date_of_start', sa.Date(), nullable=False),
    sa.Column('date_of_end', sa.Date(), nullable=False),
    sa.CheckConstraint('date_of_end > date_of_start', name='check_date_room_type_constraint'),
    sa.ForeignKeyConstraint(['category'], ['hotels_schema.room_types_book.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['room'], ['hotels_schema.rooms.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('services_rendered',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service', sa.Integer(), nullable=False),
    sa.Column('client', sa.Integer(), nullable=False),
    sa.Column('is_rendered', sa.Boolean(), nullable=False),
    sa.Column('date_of_render', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['client'], ['hotels_schema.clients.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['service'], ['hotels_schema.services.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('residences_clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('residence', sa.Integer(), nullable=False),
    sa.Column('client', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client'], ['hotels_schema.clients.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['residence'], ['hotels_schema.residences.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=settings.POSTGRES_SCHEMA
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('residences_clients', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('services_rendered', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('room_types', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('residences', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('prices_services', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('bookings_clients', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('services', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('rooms', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('prices', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('bookings', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('room_types_book', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('hotels', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('clients', schema=settings.POSTGRES_SCHEMA)
    op.drop_table('buyers', schema=settings.POSTGRES_SCHEMA)
    # ### end Alembic commands ###
