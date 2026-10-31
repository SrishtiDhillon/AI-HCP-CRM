from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class HCPCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=100)
    speciality: str = Field(max_length=100)
    hospital: str = Field(max_length=150)
    location: str = Field(max_length=100)
    email: str = Field(max_length=120)
    phone: str = Field(max_length=20)


class HCPResponse(HCPCreate):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    id: int


class InteractionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    hcp_id: int = Field(gt=0)
    interaction_date: date
    summary: str = Field(min_length=1, max_length=10000)
    products_discussed: str = Field(default='', max_length=2000)
    follow_up_date: date | None = None

    @model_validator(mode='after')
    def follow_up_not_before_interaction(self):
        if self.follow_up_date and self.follow_up_date < self.interaction_date:
            raise ValueError('Follow-up date cannot precede interaction date')
        return self


class InteractionResponse(InteractionCreate):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    id: int
