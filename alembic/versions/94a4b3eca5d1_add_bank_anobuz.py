"""Add bank ANOBUZ

Revision ID: 94a4b3eca5d1
Revises: 4198a88147f7
Create Date: 2025-12-09 10:50:30.187938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94a4b3eca5d1'
down_revision: Union[str, Sequence[str], None] = '4198a88147f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO banks (code, name, name_en, name_ru)
        VALUES
            ('ANOBUZ', 'Anorbank', 'Anorbank', 'Анорбанк');
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM banks
        WHERE code IN ('ANOBUZ');
    """)
