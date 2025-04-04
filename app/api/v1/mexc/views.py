from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database_sqlalchemy import db_helper
from .services import test


router = APIRouter(tags=['MEXC'])


@router.get("/get")
async def get_count(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await test(session=session)
    return {"return": "kox"}
