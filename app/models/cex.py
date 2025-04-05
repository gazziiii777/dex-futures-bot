from .base import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MEXC(Base):
    __tablename__ = "mexc"

    name: Mapped[str] = mapped_column()
    sumbol: Mapped[str] = mapped_column()
    slug: Mapped[str] = mapped_column()
    chain: Mapped[str] = mapped_column()
    token_address: Mapped[str] = mapped_column()
    logo: Mapped[str] = mapped_column()
    signal: Mapped[bool] = mapped_column()


class BINGX(Base):
    __tablename__ = "bingx"
    name: Mapped[str] = mapped_column()
    sumbol: Mapped[str] = mapped_column()
    slug: Mapped[str] = mapped_column()
    chain: Mapped[str] = mapped_column()
    token_address: Mapped[str] = mapped_column()
    logo: Mapped[str] = mapped_column()
    signal: Mapped[bool] = mapped_column()

