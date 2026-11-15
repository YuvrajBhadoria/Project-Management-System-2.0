from fastapi import APIRouter
from service.serverHealth import serviceHealth
router = APIRouter()

@router.get("/health")
def health():
    return serviceHealth()