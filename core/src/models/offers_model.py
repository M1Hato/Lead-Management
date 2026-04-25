import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.leads_model import LeadModel


class OffersModel(Base):
    __tablename__ = "offers"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))

    leads: Mapped[list[LeadModel]] = relationship(back_populates="offer")