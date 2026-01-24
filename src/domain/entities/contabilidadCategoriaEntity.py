from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ContabilidadCategoriaEntity(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1)
    codigo: str = Field(..., min_length=1)

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @classmethod
    def from_model(cls, obj: Any) -> "ContabilidadCategoriaEntity":
        return cls.model_validate(obj)
