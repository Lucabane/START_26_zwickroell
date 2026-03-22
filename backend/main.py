from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router
from backend.api.data import router as data_router
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse


app = FastAPI(title="START Hack 26 API", version="0.1.0")


# Ce middleware intercepte TOUTES les erreurs du backend
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 1. On extrait le traceback complet
    error_trace = traceback.format_exc()
    
    # 2. On l'affiche en rouge dans ton terminal Uvicorn
    print("\n" + "="*50)
    print("🚨 BACKEND CRASH DETECTED")
    print(error_trace)
    print("="*50 + "\n")
    
    # 3. On renvoie l'erreur détaillée au frontend au lieu d'une simple 500
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "traceback": error_trace,
            "message": "Check your terminal for the full red traceback."
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# On ajoute le préfixe "/api" ici pour correspondre aux appels du frontend
app.include_router(chat_router, prefix="/api")

# Optionnel : Tu peux aussi mettre un préfixe pour les données si nécessaire
app.include_router(data_router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
