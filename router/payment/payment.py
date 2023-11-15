from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import UserAuth, UserOut
from fastapi import Depends
from services.user_services import UserServices

from models.user_model import UserModel



payment_router = APIRouter()

@payment_router.get('/active-payment-methods', summary="get payment menthod", response_model=UserOut)
async def active_payment_method(data: UserAuth):
    pass


@payment_router.post('/add-payment', summary="add payment", response_model=UserOut)
async def add_payment(data: UserAuth):
    pass


@payment_router.post('/payment-histories', summary="get payment history", response_model=UserOut)
async def payment_histories(data: UserAuth):
    pass