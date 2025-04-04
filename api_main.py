from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.mexc.views import router as mexc_router

app = FastAPI(
    title='asd', docs_url="/docs"
)

app.include_router(mexc_router, prefix="/api/v1/mexc")


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
