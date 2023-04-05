from typing import List, Optional
from datetime import date
from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Canary(Base):
    __tablename__ = "canary"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ring: Mapped[Optional[str]] = mapped_column(String(30), unique=True)
    sex: Mapped[str] = mapped_column(String(30))
    color: Mapped[str] = mapped_column(String(30))
    birthday: Mapped[Optional[date]] = mapped_column(Date())

    # CANARY <---> SPAWNS
    # spawns: Mapped[List["Spawn"]] = relationship(back_populates="spawn")

    # EGG <---> CANARY
    egg_id: Mapped[Optional[int]] = mapped_column(ForeignKey("egg.id"))
    egg: Mapped[Optional["Egg"]] = relationship(back_populates="canary")

    def __repr__(self) -> str:
        return f"Canary(id={self.id}, sex={self.sex}, color={self.color})"


class Egg(Base):
    __tablename__ = "egg"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(30))

    # EGG <---> SPAWN
    spawn_id: Mapped[int] = mapped_column(ForeignKey("spawn.id"))
    spawn: Mapped["Spawn"] = relationship(back_populates="eggs")

    # EGG <---> CANARY
    canary: Mapped[Optional["Canary"]] = relationship(back_populates="egg")

    def __repr__(self) -> str:
        return f"Egg(id={self.id}, status={self.status})"


class Spawn(Base):
    __tablename__ = "spawn"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    spawned_at: Mapped[date] = mapped_column(Date())

    # CANARY <---> SPAWNS
    father_id: Mapped[int] = mapped_column(ForeignKey("canary.id"))
    father: Mapped["Canary"] = relationship("Canary", foreign_keys=[father_id])
    mother_id: Mapped[int] = mapped_column(ForeignKey("canary.id"))
    mother: Mapped["Canary"] = relationship("Canary", foreign_keys=[mother_id])

    # EGG <---> SPAWN
    eggs: Mapped[List["Egg"]] = relationship(back_populates="spawn")

    def __repr__(self) -> str:
        return f"Spawn(id={self.id}, father_id={self.father_id}, mother_id={self.mother_id}, eggs_count={len(self.eggs)})"
