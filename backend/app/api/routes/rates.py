from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.rate_service import RateService
from app.schemas import RateResponse

router = APIRouter()


@router.get("/rates", response_model=list[RateResponse])
async def get_rates(session: AsyncSession = Depends(get_db)):
    rate_service = RateService(session)
    rates = await rate_service.get_all_rates()
    return [RateResponse.model_validate(r) for r in rates]
