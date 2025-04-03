from .base import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MEXC(Base):
    name: str = Mapped[str]