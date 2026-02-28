from sqlalchemy import Column, DateTime, Integer, String

from utils.timezone import now_utc_minus_5

from src.infrastructure.models.base import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=now_utc_minus_5, nullable=False)
    updated_at = Column(DateTime, default=now_utc_minus_5, onupdate=now_utc_minus_5, nullable=False)
