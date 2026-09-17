from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import QuoteRequest, QuoteResponse
from app.services.quote_service import QuoteService
from app.api.routes.auth import get_current_user

router = APIRouter()


@router.post("/quotes", response_model=QuoteResponse)
async def create_quote(
    req: QuoteRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    quote_service = QuoteService(session)
    try:
        quote = await quote_service.create_quote(
            user_id=user.id,
            currency=req.currency,
            network=req.network,
            input_amount=req.input_amount,
        )
        return QuoteResponse(
            quote_id=quote.quote_id,
            currency=quote.currency,
            network=quote.network,
            input_amount=quote.input_amount,
            rate=quote.rate,
            fee=quote.fee,
            output_amount=quote.output_amount,
            expires_at=quote.expires_at,
            remaining_seconds=quote.remaining_seconds,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/quotes/{quote_id}", response_model=QuoteResponse)
async def get_quote(
    quote_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    quote_service = QuoteService(session)
    quote = await quote_service.get_quote(quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    if quote.is_expired:
        raise HTTPException(status_code=410, detail="Quote expired")
    return QuoteResponse(
        quote_id=quote.quote_id,
        currency=quote.currency,
        network=quote.network,
        input_amount=quote.input_amount,
        rate=quote.rate,
        fee=quote.fee,
        output_amount=quote.output_amount,
        expires_at=quote.expires_at,
        remaining_seconds=quote.remaining_seconds,
    )
