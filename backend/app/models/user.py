"""User model — dummy/base model to prove DB + migration setup (Phase 3).

Full auth fields Phase 5 me finalize honge.
Table: `helpdesk_users` (prefix se existing ERP tables se collision nahi hoga).
"""
import enum

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import TABLE_PREFIX
from app.core.database import Base
from app.models.mixins import TimestampMixin, UUIDMixin


class UserRole(str, enum.Enum):
    admin = "admin"
    agent = "agent"
    customer = "customer"


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = f"{TABLE_PREFIX}users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="helpdesk_user_role"), default=UserRole.customer, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
