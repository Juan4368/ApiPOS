from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from domain.enums.contabilidadEnums import CategoriaTipo


class ContabilidadCategoriaEntity(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1)
    tipo_categoria: CategoriaTipo

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @classmethod
    def from_model(cls, obj: Any) -> "ContabilidadCategoriaEntity":
        return cls.model_validate(obj)
