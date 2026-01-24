from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.contabilidadCategoriaDto import (
    ContabilidadCategoriaRequest,
    ContabilidadCategoriaResponse,
    ContabilidadCategoriaUpdateRequest,
)
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.services.contabilidad_categoria_service import ContabilidadCategoriaService
from src.infrastructure.repository.createContabilidadCategoriaRepository import (
    ContabilidadCategoriaRepository,
)

router = APIRouter(prefix="/contabilidad/categorias", tags=["contabilidad-categorias"])


def get_service(db: Session = Depends(get_db)) -> ContabilidadCategoriaService:
    repo = ContabilidadCategoriaRepository(db)
    return ContabilidadCategoriaService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[ContabilidadCategoriaService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[ContabilidadCategoriaResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_categoria(
    payload: ContabilidadCategoriaRequest,
    service: ServiceDep,
) -> CreationResponse[ContabilidadCategoriaResponse]:
    try:
        created = service.create_categoria(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[ContabilidadCategoriaResponse](id=created.id, data=created)


@router.get("/", response_model=list[ContabilidadCategoriaResponse])
def list_categorias(service: ServiceDep) -> list[ContabilidadCategoriaResponse]:
    return service.list_categorias()


@router.get("/por-nombre", response_model=ContabilidadCategoriaResponse)
def get_by_nombre(nombre: str, service: ServiceDep) -> ContabilidadCategoriaResponse:
    if not nombre.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parametro nombre no puede estar vacio",
        )
    categoria = service.get_by_nombre(nombre.strip())
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    return categoria


@router.get("/{categoria_id}", response_model=ContabilidadCategoriaResponse)
def get_categoria(categoria_id: int, service: ServiceDep) -> ContabilidadCategoriaResponse:
    categoria = service.get_categoria(categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    return categoria


@router.put("/{categoria_id}", response_model=ContabilidadCategoriaResponse)
def update_categoria(
    categoria_id: int,
    payload: ContabilidadCategoriaRequest,
    service: ServiceDep,
) -> ContabilidadCategoriaResponse:
    categoria = service.update_categoria(categoria_id, payload)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    return categoria


@router.patch("/{categoria_id}", response_model=ContabilidadCategoriaResponse)
def patch_categoria(
    categoria_id: int,
    payload: ContabilidadCategoriaUpdateRequest,
    service: ServiceDep,
) -> ContabilidadCategoriaResponse:
    categoria = service.patch_categoria(categoria_id, payload)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    return categoria

