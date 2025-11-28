"""
Main FastAPI Application
Entry point do MCP Tiny ERP Server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from src.api.mcp_server import router as mcp_router
from src.api.test_endpoints import router as test_router

# Inicializa FastAPI
app = FastAPI(
    title="MCP Tiny ERP Server",
    description="Model Context Protocol server for Tiny ERP integration",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra routers
app.include_router(mcp_router)
app.include_router(test_router)

# Health check
@app.get("/health")
async def health():
    return JSONResponse(content={
        "status": "healthy",
        "service": "mcp-tiny-erp-server",
        "version": "2.0.0"
    })

# Root endpoint
@app.get("/")
async def root():
    return JSONResponse(content={
        "name": "MCP Tiny ERP Server",
        "version": "2.0.0",
        "status": "online",
        "mcp_endpoint": "/mcp",
        "docs": "/docs"
    })


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
