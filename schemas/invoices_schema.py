from typing import Union
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator
from models.user_model import UserModel



class InvoicesOut(BaseModel):
    id                              :Optional[int]
    client_id                       :Optional[int]
    invoice_number                  :Optional[str]
    sequence_number                 :Optional[int]
    recurring                       :Optional[str]
    date                            :Optional[str]
    due_date                        :Optional[int]
    status_id                       :Optional[int]
    recurring_cycle_id              :Optional[int]
    sub_total                       :Optional[float]
    discount_type                   :Optional[str]
    discount                        :Optional[float]
    total                           :Optional[float]
    received_amount                 :Optional[float]
    due_amount                      :Optional[float]
    notes                           :Optional[str]
    terms                           :Optional[str]
    created_by                      :Optional[int]
    deleted_at                      :Optional[str]
    created_at                      :Optional[str]
    updated_at                      :Optional[str]


    class Config:
        orm_mode = True


class Product(BaseModel):
    product_id:int
    name:str
    quantity:int
    price:float
    tax_id:Union[int, None] = None
    amount:float


class AddInvoice(BaseModel):
    client_id                       :int
    date                            :str
    discount_type                   :str
    discount                        :float
    due_amount                      :float
    due_date                        :str
    invoice_number                  :str
    notes                           :str
    products                        :list[Product]
    received_amount                 :float
    recurring                       :str
    status_id                       :int
    sub_total                       :float
    terms                           :str
    total                           :float


