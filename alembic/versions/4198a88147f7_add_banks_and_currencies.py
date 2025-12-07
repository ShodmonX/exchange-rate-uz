"""Add banks and Currencies

Revision ID: 4198a88147f7
Revises: 2538f0fb9beb
Create Date: 2025-12-07 12:35:54.356554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4198a88147f7'
down_revision: Union[str, Sequence[str], None] = '2538f0fb9beb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO banks (code, name, name_en, name_ru)
        VALUES
            ('CBU', 'Oʻzbekiston markaziy banki', 'Central Bank of Uzbekistan', 'Центральный банк Узбекистана');
    """)

    op.execute("""
        INSERT INTO currencies (code, name, name_en, name_ru)
        VALUES
            ('USD', 'AQSh dollari', 'US Dollar', 'Доллар США'),
            ('EUR', 'Yevro', 'Euro', 'Евро'),
            ('RUB', 'Rossiya rubli', 'Russian Ruble', 'Российский рубль'),
            ('GBP', 'Angliya funt sterlingi', 'British Pound Sterling', 'Британский фунт стерлингов'),
            ('CNY', 'Xitoy yuani', 'Chinese Yuan', 'Китайский юань'),
            ('CHF', 'Shveysariya franki', 'Swiss Franc', 'Швейцарский франк'),
            ('JPY', 'Yaponiya iyenasi', 'Japanese Yen', 'Японская иена'),
            ('KZT', 'Qozog‘iston tengesi', 'Kazakhstani Tenge', 'Казахстанский тенге');
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM banks
        WHERE code IN ('cbu')
    """)

    op.execute("""
        DELETE FROM currencies
        WHERE code IN ('USD', 'EUR', 'RUB', 'GBP', 'CNY', 'CHF', 'JPY', 'KZT');
    """)
