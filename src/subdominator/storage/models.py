from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class EnumerationRun(Base):
    __tablename__ = "enumeration_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    root_domain: Mapped[str] = mapped_column(String(255), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    findings: Mapped[list["FindingRecord"]] = relationship(back_populates="run", cascade="all, delete-orphan")


class FindingRecord(Base):
    __tablename__ = "findings"
    __table_args__ = (
        UniqueConstraint("root_domain", "subdomain", name="uq_root_subdomain"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("enumeration_runs.id", ondelete="CASCADE"))
    root_domain: Mapped[str] = mapped_column(String(255), index=True)
    subdomain: Mapped[str] = mapped_column(String(255), index=True)
    resource: Mapped[str] = mapped_column(String(64), index=True)
    query_target: Mapped[str] = mapped_column(String(255))
    recursion_depth: Mapped[int] = mapped_column(Integer, default=0)
    discovered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    run: Mapped[EnumerationRun] = relationship(back_populates="findings")

