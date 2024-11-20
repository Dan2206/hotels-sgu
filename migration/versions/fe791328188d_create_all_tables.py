"""create all tables

Revision ID: fe791328188d
Revises: 5c4905d2016a
Create Date: 2024-11-20 18:43:06.516613

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = 'fe791328188d'
down_revision = '5c4905d2016a'
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
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=False),
    sa.Column('stars', sa.Integer(), nullable=False),
    sa.CheckConstraint('stars >= 0 AND stars <= 5'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
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
    sa.Column('date_of_booking', sa.DateTime(), nullable=False),
    sa.Column('date_of_start', sa.Date(), nullable=False),
    sa.Column('date_of_end', sa.Date(), nullable=False),
    sa.Column('extra', sa.String(length=500), nullable=True),
    sa.Column('reason_cancel', sa.String(length=500), nullable=True),
    sa.CheckConstraint('date_of_end > date_of_start'),
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
    sa.CheckConstraint('date_of_end >= date_of_start'),
    sa.CheckConstraint('price > 0'),
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
    sa.ForeignKeyConstraint(['hotel'], ['hotels_schema.hotels.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hotel', 'room_num', name='uq_hotel_room'),
    schema=settings.POSTGRES_SCHEMA
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('hotel', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['hotel'], ['hotels_schema.hotels.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hotel', 'name'),
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
    sa.CheckConstraint('date_of_end > date_of_start'),
    sa.CheckConstraint('price > 0'),
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
    sa.CheckConstraint('date_of_end > date_of_start'),
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
    op.alter_column('clients', 'surname',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'name',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'patronymic',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'type_of_document',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=50),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'document',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=50),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'email',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'phone',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=True,
               schema=settings.POSTGRES_SCHEMA)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('clients', 'phone',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'email',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'document',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'type_of_document',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'patronymic',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
    op.alter_column('clients', 'surname',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False,
               schema=settings.POSTGRES_SCHEMA)
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
    op.drop_table('buyers', schema=settings.POSTGRES_SCHEMA)
    # ### end Alembic commands ###
