import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class LeadModel(Base):
    __tablename__ = 'leads'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    country: Mapped[str] = mapped_column(String(2))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    affiliate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("affiliates.id"))


    offer: Mapped["OffersModel"] = relationship(back_populates="leads")
    affiliate: Mapped["AffiliatesModel"] = relationship(back_populates="leads")