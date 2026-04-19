from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from subdominator.storage.models import Base


class Database:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{self.path}", future=True)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=False, class_=Session)

    def initialize(self) -> None:
        Base.metadata.create_all(self.engine)
