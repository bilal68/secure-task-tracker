# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth, tasks  

app = FastAPI(
    title="Secure Task Tracker",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS (open in dev; we'll restrict via .env later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # TODO: replace with your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}

@app.get("/", tags=["system"])
def root():
    return {"service": "secure-task-tracker", "docs": "/docs"}

# Routers (we'll uncomment these after we create them)
# from app.api.routers import auth, tasks, admin
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
# app.include_router(admin.router, prefix="/admin", tags=["admin"])
