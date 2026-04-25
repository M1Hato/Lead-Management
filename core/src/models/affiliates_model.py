import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from src.database import Base
from src.models.leads_model import LeadModel


class AffiliatesModel(Base):
    __tablename__ = "affiliates"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()

    leads: Mapped[list[LeadModel]] = relationship(back_populates="affiliate")