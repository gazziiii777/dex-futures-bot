from .base import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

class MEXC(Base):
    __tablename__ = "mexc"
    name: Mapped[str] = mapped_column(nullable=True)
    symbol: Mapped[str] = mapped_column(nullable=True)
    slug: Mapped[str] = mapped_column(nullable=True)
    logo: Mapped[str] = mapped_column(nullable=True)
    signal: Mapped[bool] = mapped_column(nullable=True)


    chains: Mapped[list["Chains"]] = relationship(back_populates="mexc", cascade="all, delete-orphan")



class BINGX(Base):
    __tablename__ = "bingx"
    name: Mapped[str] = mapped_column()
    symbol: Mapped[str] = mapped_column()
    slug: Mapped[str] = mapped_column()
    logo: Mapped[str] = mapped_column()
    signal: Mapped[bool] = mapped_column()


    chains: Mapped[list["Chains"]] = relationship(back_populates="bingx", cascade="all, delete-orphan")


class Chains(Base):
    __tablename__ = "chains"
    chain: Mapped[str] = mapped_column()
    token_address: Mapped[str] = mapped_column()

    mexc_id: Mapped[int] = mapped_column(ForeignKey("mexc.id"), nullable=True)
    bingx_id: Mapped[int] = mapped_column(ForeignKey("bingx.id"), nullable=True)

    mexc: Mapped["MEXC"] = relationship(back_populates="chains")
    bingx: Mapped["BINGX"] = relationship(back_populates="chains")
    
    
class Users(Base):
    __tablename__ = "users"
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    api_key: Mapped[str | None] = mapped_column(Text, nullable=True)

    subscription_active: Mapped[bool] = mapped_column(Boolean, default=False)
    last_payment_date: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    
