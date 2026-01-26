from pathlib import Path
import os
import sys
import threading
import time
import webbrowser

from dotenv import load_dotenv
from fastapi import FastAPI
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

DOCS_URL = "http://127.0.0.1:8001/docs"
BROWSER_CANDIDATES = [
    "C://Program Files//Google//Chrome//Application//chrome.exe",
    "C://Program Files (x86)//Google//Chrome//Application//chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
]


def load_environment() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)


def create_app() -> FastAPI:
    load_environment()

    app = FastAPI(
        title="POS API",
        version="1.0.0",
        description="API para la gestion de pedidos",
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    app.include_router(category_router)
    app.include_router(cartera_router)
    app.include_router(caja_router)
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

    @app.get("/")
    def root():
        return {"mensaje": "API POS en ejecucion"}

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
    threading.Thread(target=open_docs_in_browser, daemon=True).start()

    import uvicorn

    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
