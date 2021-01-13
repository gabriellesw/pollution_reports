"""complaints table

Revision ID: 680bfdb32640
Revises: 
Create Date: 2021-01-12 21:30:53.326136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '680bfdb32640'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complaint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anonymous', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('confirm_email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=100), nullable=True),
    sa.Column('landline', sa.Boolean(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('street', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('zip', sa.String(length=5), nullable=True),
    sa.Column('pollution_type', sa.Enum('Odors/Fumes', 'Smoke', 'Dust', 'Asbestos'), nullable=False),
    sa.Column('description', sa.Text(length=5000), nullable=False),
    sa.Column('polluter_search', sa.String(length=100), nullable=True),
    sa.Column('polluter_street_number', sa.String(length=100), nullable=False),
    sa.Column('polluter_street_name', sa.String(length=100), nullable=False),
    sa.Column('polluter_city', sa.String(length=100), nullable=False),
    sa.Column('polluter_state', sa.String(length=2), nullable=False),
    sa.Column('polluter_zip', sa.String(length=5), nullable=False),
    sa.Column('observed_date', sa.DateTime(), nullable=False),
    sa.Column('ongoing', sa.Boolean(), nullable=False),
    sa.Column('consent_to_followup', sa.Boolean(), nullable=False),
    sa.Column('consent_to_campaign', sa.Boolean(), nullable=False),
    sa.Column('lat', sa.String(length=100), nullable=True),
    sa.Column('lng', sa.String(length=100), nullable=True),
    sa.Column('submitted_date', sa.DateTime(), nullable=True),
    sa.Column('submitted_to_calepa', sa.Boolean(), nullable=True),
    sa.Column('submitted_to_calepa_date', sa.DateTime(), nullable=True),
    sa.Column('calepa_confirmation_number', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('complaint')
    # ### end Alembic commands ###