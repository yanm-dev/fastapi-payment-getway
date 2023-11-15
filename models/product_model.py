from sqlalchemy import (
    Column,
    INTEGER,
    MetaData,
    String,
    DateTime,
    UniqueConstraint,
    ForeignKey


)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ProductModel(Base):
    __tablename__ = "products"
    id              = Column(INTEGER, primary_key=True)
    name      = Column(String)
    code       = Column(String)
    category_id      = Column(INTEGER, ForeignKey("categories.id"))
    unit_price        = Column(String)
    description      = Column(INTEGER)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())

class CategoryModel(Base):
    __tablename__ = "categories"
    id              = Column(INTEGER, primary_key=True)
    name      = Column(String)
    created_by = Column(INTEGER)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())


class FileModel(Base):
    __tablename__ = "files"
    id              = Column(INTEGER, primary_key=True)
    path      = Column(String)
    fileable_type = Column(INTEGER)
    fileable_id = Column(INTEGER)
    type = Column(String)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now())
