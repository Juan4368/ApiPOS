from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.dtos.proveedorDto import (
    ProveedorRequest,
    ProveedorResponse,
    ProveedorUpdateRequest,
)
from src.domain.services.proveedor_service import ProveedorService
from src.infrastructure.repository.createProveedorRepository import ProveedorRepository

router = APIRouter(prefix="/proveedores", tags=["proveedores"])


def get_service(db: Session = Depends(get_db)) -> ProveedorService:
    repo = ProveedorRepository(db)
    return ProveedorService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[ProveedorService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[ProveedorResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_proveedor(
    payload: ProveedorRequest,
    service: ServiceDep,
) -> CreationResponse[ProveedorResponse]:
    try:
        created = service.create_proveedor(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[ProveedorResponse](id=created.id, data=created)


@router.get("/", response_model=list[ProveedorResponse])
def list_proveedores(
    service: ServiceDep,
    q: Optional[str] = None,
) -> list[ProveedorResponse]:
    if q and q.strip():
        return service.search_proveedores(q)
    return service.list_proveedores()


@router.get("/{proveedor_id}", response_model=ProveedorResponse)
def get_proveedor(proveedor_id: int, service: ServiceDep) -> ProveedorResponse:
    proveedor = service.get_proveedor(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return proveedor


@router.put("/{proveedor_id}", response_model=ProveedorResponse)
def update_proveedor(
    proveedor_id: int,
    payload: ProveedorRequest,
    service: ServiceDep,
) -> ProveedorResponse:
    proveedor = service.update_proveedor(proveedor_id, payload)
    if not proveedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return proveedor


@router.patch("/{proveedor_id}", response_model=ProveedorResponse)
def patch_proveedor(
    proveedor_id: int,
    payload: ProveedorUpdateRequest,
    service: ServiceDep,
) -> ProveedorResponse:
    proveedor = service.patch_proveedor(proveedor_id, payload)
    if not proveedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return proveedor
