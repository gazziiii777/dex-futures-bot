from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


router = APIRouter(tags=['MEXC'])


@router.get("/get")
async def get_count():
    return {"return": "kox"}



app = FastAPI(
    title='YG', docs_url="/docs"
)

app.include_router(router, prefix="/api/v1")



app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)