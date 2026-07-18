from pydantic import BaseModel
from datetime import date


# ---------- HCP ----------

class HCPCreate(BaseModel):
    name: str
    speciality: str
    hospital: str
    location: str
    email: str
    phone: str


class HCPResponse(HCPCreate):
    id: int

    class Config:
        from_attributes = True


# ---------- Interaction ----------

class InteractionCreate(BaseModel):
    hcp_id: int
    interaction_date: date
    summary: str
    products_discussed: str
    follow_up_date: date


class InteractionResponse(InteractionCreate):
    id: int

    class Config:
        from_attributes = True



# ---------- Interaction ----------

class InteractionCreate(BaseModel):
    hcp_id: int
    interaction_date: date
    summary: str
    products_discussed: str
    follow_up_date: date


class InteractionResponse(InteractionCreate):
    id: int

    class Config:
        from_attributes = True