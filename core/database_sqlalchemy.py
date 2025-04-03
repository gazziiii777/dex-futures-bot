import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import sessionmaker
from core.config import settings
from asyncio import current_task
from contextlib import asynccontextmanager



class DataSperm:
    def __init__(self):
        self.engine=create_async_engine(
            url=settings.DB_URL,
            pool_size=100,
            echo=True,
            max_overflow=50)

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session
    

    async def session_dependency(self): 
        async with self.session_factory() as session:
            yield session
            await session.close()

    
    async def scoped_session_dependency(self):
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.close()

    
    @asynccontextmanager
    async def scoped_session_dependency_context(self) -> AsyncSession: # type: ignore
        session = self.get_scoped_session()
        yield session
        await session.close()



db_helper = DataSperm()
