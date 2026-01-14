from typing import Generic, TypeVar
from uuid import UUID

from pydantic.generics import GenericModel

T = TypeVar("T")


class CreationResponse(GenericModel, Generic[T]):
    """DTO generico para manejar las respuestas de creacion."""

    id: UUID | int
    message: str = "Creacion exitosa"
    data: T

    model_config = {"from_attributes": True}
