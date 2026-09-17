from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.core.config import get_settings
from app.api.routes import rates, quotes, orders, wallets, auth, admin

settings = get_settings()

app = FastAPI(title="Exchange Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rates.router, prefix="/api", tags=["rates"])
app.include_router(quotes.router, prefix="/api", tags=["quotes"])
app.include_router(orders.router, prefix="/api", tags=["orders"])
app.include_router(wallets.router, prefix="/api", tags=["wallets"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"

if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(STATIC_DIR / "index.html"))
