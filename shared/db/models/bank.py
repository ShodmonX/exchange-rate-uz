from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from shared.db import Base


class Bank(Base):
    __tablename__ = "banks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    name_ru: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)

    exchange_rates = relationship("ExchangeRate", back_populates="bank")

    def __repr__(self):
        return f"Bank(id={self.id!r}, name={self.name!r}, code={self.code!r})"

    def __str__(self):
        return self.name
