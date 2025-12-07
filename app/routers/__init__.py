from fastapi import APIRouter

from .bank import router as bank_router
from .currency import router as currency_router
from .exchange_rate import router as exchange_rate_router


router = APIRouter(
    prefix="/api",
    # tags=["API"],
    # responses={404: {"description": "Not found"}},
)

router.include_router(bank_router)
router.include_router(currency_router)
router.include_router(exchange_rate_router)
