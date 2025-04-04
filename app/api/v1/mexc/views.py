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
