from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String
from subdominator.modules.handler import dbpath

Base = declarative_base()

class Subdomain(Base):
    __tablename__ = "subdomains"
    domain = Column(String, primary_key=True)
    subdomains = Column(String, default="")  

DBURL = f"sqlite+aiosqlite:///{dbpath}"

async_engine = create_async_engine(DBURL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)