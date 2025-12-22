"""Add bank UJSIUZ

Revision ID: a2911ee33333
Revises: 94a4b3eca5d1
Create Date: 2025-12-10 12:20:32.734927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2911ee33333'
down_revision: Union[str, Sequence[str], None] = '94a4b3eca5d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO banks (code, name, name_en, name_ru)
        VALUES
            ('UJSIUZ', 'O’zsanoatqurilishbank', 'Uzpromstroybank', 'Узпромстройбанк');
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM banks
        WHERE code IN ('UJSIUZ');
    """)
