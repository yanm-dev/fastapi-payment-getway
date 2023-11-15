from fastapi import APIRouter
from router.root import root
from router.user import user_router
from router.invoice import invoice
from router.recurring_invoice import recurring_invocie
from router.payment import payment
from router.product import product
from router.otp import otp
router = APIRouter()

router.include_router(root.root, prefix='/root', tags=["root"])
router.include_router(user_router.user_router,  tags=["AUTH"])
router.include_router(product.product_router, tags=["Product"])
router.include_router(invoice.invoice_router, tags=["Invoice"])
router.include_router(recurring_invocie.recurring_invoice_router, tags=["Recurring Invoice"])
router.include_router(payment.payment_router, tags=["Payment"])
router.include_router(otp.otp_router, tags=["OTP"])


