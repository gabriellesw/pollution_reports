"""new complaint table

Revision ID: ea41552f44e2
Revises: 
Create Date: 2021-04-06 11:40:07.399904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea41552f44e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complaint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('polluter_search', sa.String(), nullable=True),
    sa.Column('polluter_lat', sa.String(), nullable=True),
    sa.Column('polluter_lng', sa.String(), nullable=True),
    sa.Column('polluter_street_number', sa.String(), nullable=True),
    sa.Column('polluter_locality', sa.String(), nullable=True),
    sa.Column('polluter_route', sa.String(), nullable=True),
    sa.Column('polluter_administrative_area_level_1', sa.String(), nullable=True),
    sa.Column('polluter_administrative_area_level_2', sa.String(), nullable=True),
    sa.Column('polluter_postal_code', sa.String(), nullable=True),
    sa.Column('polluter_name', sa.String(), nullable=True),
    sa.Column('street_number', sa.String(), nullable=True),
    sa.Column('route', sa.String(), nullable=True),
    sa.Column('locality', sa.String(), nullable=True),
    sa.Column('administrative_area_level_1', sa.String(), nullable=True),
    sa.Column('administrative_area_level_2', sa.String(), nullable=True),
    sa.Column('postal_code', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('hour', sa.Integer(), nullable=True),
    sa.Column('minute', sa.Integer(), nullable=True),
    sa.Column('ampm', sa.String(), nullable=True),
    sa.Column('ongoing', sa.Boolean(), nullable=True),
    sa.Column('anonymous', sa.Boolean(), nullable=True),
    sa.Column('refinery', sa.Boolean(), nullable=True),
    sa.Column('pollution_type', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('recorded_date', sa.DateTime(), nullable=True),
    sa.Column('epa_confirmation_number', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('complaint')
    # ### end Alembic commands ###
