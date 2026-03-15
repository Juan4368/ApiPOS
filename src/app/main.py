from pathlib import Path
import os
import subprocess
import sys
import threading
import time
import webbrowser

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
# Make sure imports work whether the app runs as a module or a script.
for path in (PROJECT_ROOT, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.append(str(path))

from src.app.controller.category_controller import router as category_router
from src.app.controller.cartera_controller import router as cartera_router
from src.app.controller.caja_controller import router as caja_router
from src.app.controller.cierre_caja_denominacion_controller import (
    router as cierre_caja_denominacion_router,
)
from src.app.controller.caja_sesion_controller import router as caja_sesion_router
from src.app.controller.cajas_cerveza_controller import router as cajas_cerveza_router
from src.app.controller.cliente_controller import router as cliente_router
from src.app.controller.contabilidad_categoria_controller import (
    router as contabilidad_categoria_router,
)
from src.app.controller.cuenta_cobrar_controller import (
    router as cuenta_cobrar_router,
)
from src.app.controller.egreso_controller import router as egreso_router
from src.app.controller.ingreso_controller import router as ingreso_router
from src.app.controller.proveedor_controller import router as proveedor_router
from src.app.controller.movimiento_financiero_controller import (
    router as movimiento_financiero_router,
)
from src.app.controller.product_controller import router as product_router
from src.app.controller.stock_controller import router as stock_router
from src.app.controller.user_controller import router as user_router
from src.app.controller.venta_controller import router as venta_router
from src.app.controller.visita_controller import router as visita_router

DEFAULT_PORT = 8000
DOCS_URL = f"http://127.0.0.1:{DEFAULT_PORT}/docs"
BROWSER_CANDIDATES = [
    "C://Program Files//Google//Chrome//Application//chrome.exe",
    "C://Program Files (x86)//Google//Chrome//Application//chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
]
LOCALHOST_HOSTS = {"127.0.0.1", "::1", "localhost"}


def load_environment() -> None:
    env_candidates = [
        PROJECT_ROOT / ".env",
        Path(__file__).resolve().parent / ".env",
    ]

    for env_path in env_candidates:
        if env_path.exists():
            load_dotenv(env_path)
            break


def create_app() -> FastAPI:
    load_environment()

    docs_mode = os.getenv("SWAGGER_MODE", "off").strip().lower()
    docs_token = os.getenv("SWAGGER_TOKEN", "").strip()

    app = FastAPI(
        title="POS API",
        version="1.0.0",
        description="API para la gestion de pedidos",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.9:5173",
        "https://pos.seustech.com",
        "http://192.168.1.9:4173"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(category_router)
    app.include_router(cartera_router)
    app.include_router(caja_router)
    app.include_router(cierre_caja_denominacion_router)
    app.include_router(caja_sesion_router)
    app.include_router(cajas_cerveza_router)
    app.include_router(cliente_router)
    app.include_router(contabilidad_categoria_router)
    app.include_router(cuenta_cobrar_router)
    app.include_router(egreso_router)
    app.include_router(ingreso_router)
    app.include_router(proveedor_router)
    app.include_router(movimiento_financiero_router)
    app.include_router(product_router)
    app.include_router(stock_router)
    app.include_router(user_router)
    app.include_router(venta_router)
    app.include_router(visita_router)

    @app.get("/")
    def root():
        return {"mensaje": "API POS en ejecucion"}

    @app.post("/open-cash-drawer")
    def open_cash_drawer():
        command = os.getenv("OPEN_CASH_DRAWER_COMMAND", "").strip()
        if not command:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail=(
                    "Configura OPEN_CASH_DRAWER_COMMAND con el comando "
                    "que abre el cajon en este equipo."
                ),
            )

        try:
            subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except subprocess.TimeoutExpired as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Tiempo de espera agotado al abrir el cajon.",
            ) from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"No se pudo abrir el cajon. {stderr or 'Error en comando del sistema.'}",
            ) from exc

        return {"ok": True, "mensaje": "Comando de apertura ejecutado."}

    def assert_docs_access(
        request: Request,
        x_swagger_token: str | None = Header(default=None),
    ) -> None:
        if docs_mode == "local":
            client_host = request.client.host if request.client else ""
            if client_host not in LOCALHOST_HOSTS:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Swagger solo disponible localmente",
                )
            return

        if docs_mode == "token":
            if not docs_token or x_swagger_token != docs_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token de Swagger invalido",
                )
            return

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No encontrado",
        )

    if docs_mode in {"local", "token"}:

        @app.get("/openapi.json", include_in_schema=False)
        async def openapi(request: Request, x_swagger_token: str | None = Header(default=None)):
            assert_docs_access(request, x_swagger_token)
            return JSONResponse(app.openapi())

        @app.get("/docs", include_in_schema=False)
        async def swagger_ui_html(
            request: Request, x_swagger_token: str | None = Header(default=None)
        ):
            assert_docs_access(request, x_swagger_token)
            return get_swagger_ui_html(
                openapi_url="/openapi.json",
                title=f"{app.title} - Swagger UI",
            )

    return app


app = create_app()


def open_docs_in_browser() -> None:
    time.sleep(1)

    for path in BROWSER_CANDIDATES:
        if os.path.exists(path):
            webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(path))
            webbrowser.get("chrome").open_new(DOCS_URL)
            return

    webbrowser.open_new(DOCS_URL)


def main() -> None:
    if os.getenv("SWAGGER_MODE", "off").strip().lower() == "local":
        threading.Thread(target=open_docs_in_browser, daemon=True).start()

    import uvicorn

    port = int(os.getenv("PORT", str(DEFAULT_PORT)))

    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )


if __name__ == "__main__":
    main()
