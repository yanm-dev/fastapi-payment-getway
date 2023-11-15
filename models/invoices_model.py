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


class InvoicesModel(Base):
    __tablename__ = "invoices"
    id                          = Column(INTEGER, primary_key=True)
    client_id                   = Column(INTEGER)
    invoice_number              = Column(String)
    sequence_number             = Column(INTEGER)
    recurring                   = Column(INTEGER)
    date                        = Column(DateTime)
    due_date                    = Column(DateTime)
    status_id                   = Column(INTEGER)
    recurring_cycle_id          = Column(INTEGER)
    sub_total                   = Column(FLOAT)
    discount_type               = Column(String)
    discount                    = Column(FLOAT)
    total                       = Column(FLOAT)
    received_amount             = Column(FLOAT)
    due_amount                  = Column(FLOAT)
    notes                       = Column(String)
    terms                       = Column(String)
    created_by                  = Column(INTEGER)
    deleted_at                  = Column(DateTime, default=func.now())
    created_at                  = Column(DateTime, default=func.now())
    updated_at                  = Column(DateTime, default=func.now())


