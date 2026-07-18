from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class HCP(Base):
    __tablename__ = "hcp"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    speciality = Column(String(100))
    hospital = Column(String(150))
    location = Column(String(100))
    email = Column(String(120))
    phone = Column(String(20))

    interactions = relationship("Interaction", back_populates="hcp")


class Interaction(Base):
    __tablename__ = "interaction"

    id = Column(Integer, primary_key=True, index=True)

    hcp_id = Column(Integer, ForeignKey("hcp.id"))

    interaction_date = Column(Date)

    summary = Column(Text)

    products_discussed = Column(Text)

    follow_up_date = Column(Date)

    created_at = Column(DateTime, default=datetime.utcnow)

    hcp = relationship("HCP", back_populates="interactions")