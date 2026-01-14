import logging
import os
from dataclasses import dataclass, field
from typing import Optional, Set

import requests
from fastapi import HTTPException, status

from src.domain.dtos.clienteDto import ClienteRequest
from src.domain.services.ClienteService import ClienteService
from src.infrastructure.repository.whatsappClientRepository import WhatsAppClient


@dataclass
class WebhookConversationState:
    pending_cliente_creacion: Set[str] = field(default_factory=set)


def setup_webhook_logger() -> logging.Logger:
    log_path = os.getenv("WEBHOOK_LOG_PATH", "logs/webhook_payloads.txt")
    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger("webhook")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(file_handler)
    return logger


def build_whatsapp_client() -> Optional[WhatsAppClient]:
    api_url = os.getenv("WHATSAPP_API_URL")
    token = os.getenv("WHATSAPP_TOKEN")
    if api_url and token:
        return WhatsAppClient(api_url=api_url, token=token)
    return None


class WebhookService:
    def __init__(
        self,
        *,
        verify_token: str,
        state: WebhookConversationState,
        logger: logging.Logger,
        whatsapp_client: Optional[WhatsAppClient],
    ):
        self.verify_token = verify_token
        self.state = state
        self.logger = logger
        self.whatsapp_client = whatsapp_client

    def verify_subscription(
        self,
        hub_mode: str | None,
        hub_verify_token: str | None,
        hub_challenge: int | None,
    ):
        self.logger.info(
            "GET /webhook hub.mode=%s token_provided=%s hub.challenge=%s",
            hub_mode,
            bool(hub_verify_token),
            hub_challenge,
        )
        if hub_mode == "subscribe" and hub_verify_token == self.verify_token:
            return hub_challenge
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    def handle_webhook(
        self,
        body: dict,
        *,
        cliente_service: ClienteService,
    ):
        if self.whatsapp_client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="WhatsApp client no configurado",
            )

        self.logger.info("POST /payload: %s", body)

        value, messages = self._extract_messages(body)
        if not messages:
            self.logger.info("No se encontraron mensajes en el payload")
            return {"status": "ignored"}

        message = messages[0]
        self.logger.info("Mensaje detectado: %s", message)

        text = message.get("text", {}).get("body", "").strip()
        sender = message.get("from")
        contact_name = self._get_contact_name(value)

        if not text or not sender:
            self.logger.info("Payload sin texto o sin remitente")
            return {"status": "ignored"}

        normalized_text = text.strip()

        if normalized_text.upper().startswith("A"):
            return self._start_cliente_flow(sender)

        if sender in self.state.pending_cliente_creacion:
            return self._handle_cliente_creacion(sender, normalized_text, cliente_service)

        self.logger.info("Mensaje sin flujo de cliente activo, ignorado")
        return {"status": "ignored"}

    def _extract_messages(self, body: dict) -> tuple[Optional[dict], list]:
        value = None
        messages: list = []

        try:
            entry = body.get("entry", [])[0]
            change = entry.get("changes", [])[0]
            value = change.get("value", {})
            messages = value.get("messages", [])
        except Exception:
            pass

        if not messages:
            value = body.get("value", {})
            messages = value.get("messages", [])

        return value, messages

    def _get_contact_name(self, value: Optional[dict]) -> Optional[str]:
        try:
            contacts = value.get("contacts", []) if value else []
            if contacts:
                return contacts[0].get("profile", {}).get("name")
        except Exception:
            return None
        return None

    def _start_cliente_flow(self, sender: str) -> dict:
        self.state.pending_cliente_creacion.add(sender)
        instrucciones = (
            "**Nuevo cliente**\n"
            "Envia hasta 3 lineas:\n"
            "1) Nombre (obligatorio)\n"
            "2) Telefono (opcional)\n"
            "3) Email (opcional)"
        )
        self._send_message(sender, instrucciones)
        return {"status": "ok"}

    def _handle_cliente_creacion(
        self,
        sender: str,
        text: str,
        cliente_service: ClienteService,
    ) -> dict:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()] or [text.strip()]
        nombre = lines[0] if lines else ""
        telefono = lines[1] if len(lines) > 1 else None
        email = lines[2] if len(lines) > 2 else None

        if not nombre:
            self._send_message(sender, "El nombre es obligatorio para crear el cliente.")
            return {"status": "ok"}

        try:
            payload = ClienteRequest(nombre=nombre, telefono=telefono, email=email)
            created = cliente_service.create_cliente(payload)
            self._send_message(
                sender,
                f"Cliente creado: {created.nombre}. Responde A para crear otro o NO para finalizar.",
            )
        except Exception as exc:
            self.logger.error("Error creando cliente: %s", exc)
            self._send_message(sender, f"No se pudo crear el cliente: {exc}")

        self.state.pending_cliente_creacion.discard(sender)
        return {"status": "ok"}

    def _send_message(self, recipient: str, message: str) -> None:
        if self.whatsapp_client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="WhatsApp client no configurado",
            )
        try:
            self.whatsapp_client.send_message(recipient, message)
        except requests.HTTPError as exc:
            resp = exc.response
            detail = f"WhatsApp API error {resp.status_code if resp else ''}: {resp.text if resp else exc}"
            self.logger.error(detail)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=detail,
            ) from exc
