from pydantic import BaseModel, Field, ConfigDict

import datetime

from .bank import BankOut
from .currency import CurrencyOut


class ExchangeRateOut(BaseModel):
    id: int = Field(..., gt=0)
    date: datetime.date
    buy_rate: float = Field(..., ge=0)
    sell_rate: float = Field(..., ge=0)
    bank: BankOut
    currency: CurrencyOut
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
    
class ExchangeRateIn(BaseModel):
    date: datetime.date
    buy_rate: float = Field(..., ge=0)
    sell_rate: float = Field(..., ge=0)
    bank_id: int = Field(..., ge=0)
    currency_id: int = Field(..., ge=0)