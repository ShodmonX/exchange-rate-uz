from sqlalchemy import Integer, ForeignKey, Date, DateTime, Float, func, UniqueConstraint, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column

import datetime

from shared.db import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    bank_id: Mapped[int] = mapped_column(Integer, ForeignKey("banks.id"), nullable=False)
    bank = relationship("Bank", back_populates="exchange_rates")

    currency_id: Mapped[int] = mapped_column(Integer, ForeignKey("currencies.id"), nullable=False)
    currency = relationship("Currency", back_populates="exchange_rates")

    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    buy_rate: Mapped[float] = mapped_column(Float, nullable=False)
    sell_rate: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("bank_id", "currency_id", "date"),
        Index("idx_bank_id", "bank_id"),
        Index("idx_currency_id", "currency_id"),
        Index("idx_date", "date"),
    )

    def __repr__(self):
        return f"ExchangeRate(id={self.id!r}, bank={self.bank!r}, currency={self.currency!r}, date={self.date!r}, buy_rate={self.buy_rate!r}, sell_rate={self.sell_rate!r})"

    def __str__(self):
        return f"ExchangeRate(id={self.id!r}, bank={self.bank!r}, currency={self.currency!r}, date={self.date!r}, buy_rate={self.buy_rate!r}, sell_rate={self.sell_rate!r})"

