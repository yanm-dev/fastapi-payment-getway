from sqlalchemy import (
    Column,
    INTEGER,
    MetaData,
    String,
    DateTime,
    UniqueConstraint


)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    id              = Column(INTEGER, primary_key=True)
    first_name      = Column(String)
    last_name       = Column(String)
    email           = Column(String, unique=True)
    password        = Column(String)
    created_by      = Column(INTEGER)
    status_id       = Column(INTEGER)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())



class OauthAccessTokenModel(Base):
    __tablename__ = "oauth_access_tokens"
    id          = Column(String, primary_key=True)
    user_id     = Column(INTEGER)
    client_id   = Column(INTEGER)
    name        = Column(String)
    scopes      = Column(String)
    revoked     = Column(INTEGER)
    created_at  = Column(INTEGER)
    updated_at  = Column(INTEGER)
    expires_at  = Column(String)


class OauthClientModel(Base):
    __tablename__   = "oauth_clients"
    id              = Column(INTEGER, primary_key=True)
    user_id         = Column(INTEGER)
    name            = Column(String)
    secret          = Column(String)
    provider        = Column(String)
    redirect        = Column(String)
    personal_access_client = Column(INTEGER)
    password_client = Column(INTEGER)
    revoked         = Column(INTEGER)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())
