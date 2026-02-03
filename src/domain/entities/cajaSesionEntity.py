from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CajaSesionEntity(BaseModel):
    id: Optional[int] = None
    caja_id: int
    usuario_id: Optional[int] = None
    fecha_apertura: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @classmethod
    def from_model(cls, obj: Any) -> "CajaSesionEntity":
        return cls.model_validate(obj)
