from .base import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MEXC(Base):
    __tablename__ = "mexc"

    name: str = Mapped[str]
    sumbol: str = Mapped[str]
    slug: str = Mapped[str]
    chain: str = Mapped[str]
    token_address: str = Mapped[str]
    logo: str = Mapped[str]
    signal: bool = Mapped[bool]


class BINGX(Base):
    name: str = Mapped[str]
    sumbol: str = Mapped[str]
    slug: str = Mapped[str]
    chain: str = Mapped[str]
    token_address: str = Mapped[str]
    logo: str = Mapped[str]
    signal: bool = Mapped[bool]
