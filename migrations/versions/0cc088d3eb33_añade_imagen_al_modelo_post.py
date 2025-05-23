"""añade imagen al modelo post

Revision ID: 0cc088d3eb33
Revises: 185c6dd2699b
Create Date: 2025-04-22 17:41:12.810679

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0cc088d3eb33"
down_revision = "185c6dd2699b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("post", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("image_name", sa.String(), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("post", schema=None) as batch_op:
        batch_op.drop_column("image_name")

    # ### end Alembic commands ###
