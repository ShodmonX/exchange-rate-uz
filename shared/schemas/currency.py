from pydantic import BaseModel, Field, ConfigDict


class CurrencyBase(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    name_en: str | None = Field(None, min_length=1)
    name_ru: str | None = Field(None, min_length=1)

    model_config = ConfigDict(from_attributes=True)

class CurrencyOut(CurrencyBase):
    id: int = Field(..., gt=0)

class CurrencyCreate(CurrencyBase):
    pass
