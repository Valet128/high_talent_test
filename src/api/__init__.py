from fastapi import APIRouter

from src.api.reservations import router as reservations_router
from src.api.tables import router as tables_router
from src.api.services import router as services_router


main_router = APIRouter()
main_router.include_router(tables_router)
main_router.include_router(reservations_router)
main_router.include_router(services_router)