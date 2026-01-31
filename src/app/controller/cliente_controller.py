from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import get_db
from src.domain.dtos.clienteDto import ClienteRequest, ClienteResponse, ClienteUpdateRequest
from src.domain.dtos.genericResponseDto import CreationResponse
from src.domain.services.ClienteService import ClienteService
from src.infrastructure.repository.ClienteRepository import ClienteRepository

router = APIRouter(prefix="/clientes", tags=["clientes"])


def get_service(db: Session = Depends(get_db)) -> ClienteService:
    repo = ClienteRepository(db)
    return ClienteService(repo)


DbDep = Annotated[Session, Depends(get_db)]
ServiceDep = Annotated[ClienteService, Depends(get_service)]


@router.post(
    "/",
    response_model=CreationResponse[ClienteResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_cliente(
    payload: ClienteRequest,
    service: ServiceDep,
) -> CreationResponse[ClienteResponse]:
    try:
        created = service.create_cliente(payload)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return CreationResponse[ClienteResponse](id=created.id, data=created)


@router.get("/", response_model=list[ClienteResponse])
def list_clientes(
    service: ServiceDep,
    q: Optional[str] = None,
) -> list[ClienteResponse]:
    if q and q.strip():
        return service.search_clientes(q)
    return service.list_clientes()


@router.get("/buscar", response_model=list[ClienteResponse])
def search_clientes(
    q: str,
    service: ServiceDep,
) -> list[ClienteResponse]:
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parametro q no puede estar vacio",
        )
    return service.search_clientes(q)


@router.get("/buscar-normalizado", response_model=ClienteResponse)
def get_cliente_por_nombre_normalizado(
    nombre: str,
    service: ServiceDep,
) -> ClienteResponse:
    nombre_norm = nombre.strip().lower()
    if not nombre_norm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre no puede estar vacio",
        )

    cliente = service.get_by_nombre_normalizado(nombre_norm)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )
    return cliente


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: UUID, service: ServiceDep) -> ClienteResponse:
    cliente = service.get_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: UUID,
    payload: ClienteRequest,
    service: ServiceDep,
) -> ClienteResponse:
    cliente = service.update_cliente(cliente_id, payload)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse)
def patch_cliente(
    cliente_id: UUID,
    payload: ClienteUpdateRequest,
    service: ServiceDep,
) -> ClienteResponse:
    cliente = service.patch_cliente(cliente_id, payload)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente
