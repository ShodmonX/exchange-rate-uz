from pydantic import BaseModel, Field, ConfigDict


class BankBase(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    name_en: str | None = Field(None, min_length=1)
    name_ru: str | None = Field(None, min_length=1)

    model_config = ConfigDict(from_attributes=True)

class BankOut(BankBase):
    id: int = Field(..., gt=0)

class BankCreate(BankBase):
    pass
