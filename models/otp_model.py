from sqlalchemy import (
    Column,
    INTEGER,
    FLOAT,
    MetaData,
    String,
    DateTime,
    UniqueConstraint,
    ForeignKey


)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class OTPModel(Base):
    __tablename__ = "otp_generators"

    id                  = Column(String, primary_key=True)
    user_id             = Column(INTEGER)
    email               = Column(String)
    phone_number        = Column(String)
    code                = Column(String)
    is_verified         = Column(INTEGER)
    otp_for             = Column(String)
    ip_address          = Column(String)
    expired_at          = Column(INTEGER)
    created_at          = Column(DateTime, default=func.now())
    updated_at          = Column(DateTime, default=func.now())