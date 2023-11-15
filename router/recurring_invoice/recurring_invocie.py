from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import UserAuth, UserOut
from fastapi import Depends
from services.user_services import UserServices

from models.user_model import UserModel



recurring_invoice_router = APIRouter()

@recurring_invoice_router.get('/invoices/recurring', summary="recurring invoice and get list invoice", response_model=UserOut)
async def invoices(data: UserAuth):
    pass