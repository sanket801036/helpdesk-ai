"""Reusable model mixins (UUID PK + timestamps).

Generic `Uuid` type use kiya gaya hai taaki MySQL (CHAR(32)) aur SQLite dono par chale.
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
