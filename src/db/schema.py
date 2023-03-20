from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import cast, select, String, TIMESTAMP
from sqlalchemy import ForeignKey
import uuid
import datetime

# Declare database models used by SQLAlchemy ORM
class Base(DeclarativeBase):
    pass

# Declaring mapped classes with the appropriate ORM format.
class Implants(Base):
    __tablename__ = "Implants"
    Implant_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    OS: Mapped[str] = mapped_column(String(64))
    Arch: Mapped[str] =  mapped_column(String(64))
    Arch: Mapped[str] =  mapped_column(String(64))
    IPv4: Mapped[str] = mapped_column(String(64))
    Hostname: Mapped[str] = mapped_column(String(64))
    Username: Mapped[str] = mapped_column(String(64))
    PID: Mapped[int] = mapped_column
    ImplantUpTime: Mapped[datetime.datetime] = TIMESTAMP(timezone = True)
    
class Loot(Base):
    __tablename__ = "Loot"
    Loot_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Loot_Type: Mapped[str] = mapped_column(String(64))
    Implant_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("Implants.Implant_UUID"), nullable = False, default=uuid.uuid4)
    Operator_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("Operators.Operator_UUID"), nullable = False, default=uuid.uuid4)
    CreatedAt: Mapped[datetime.datetime] = TIMESTAMP(timezone = True)

class Operators(Base):
    __tablename__ = "Operators"

    Operator_UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    User: Mapped[str] = mapped_column(String(64))
    Password: Mapped[str] = mapped_column(String(64))