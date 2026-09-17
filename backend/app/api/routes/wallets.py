from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import WalletCreate, WalletResponse
from app.database.repositories.wallet_repo import WalletRepository
from app.services.wallet_service import WalletService
from app.api.routes.auth import get_current_user
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/wallets", response_model=list[WalletResponse])
async def list_wallets(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    wallet_repo = WalletRepository(session)
    wallets = await wallet_repo.get_user_wallets(user.id)
    return [WalletResponse.model_validate(w) for w in wallets]


@router.post("/wallets", response_model=WalletResponse)
async def create_wallet(
    req: WalletCreate,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    wallet_service = WalletService(session, settings.test_mode)
    if not wallet_service.is_valid_address(req.address, req.network):
        raise HTTPException(status_code=400, detail="Invalid wallet address")

    wallet_repo = WalletRepository(session)
    wallet = await wallet_repo.create(user.id, req.currency, req.network, req.address, req.label)
    return WalletResponse.model_validate(wallet)


@router.delete("/wallets/{wallet_id}")
async def delete_wallet(
    wallet_id: int,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    wallet_repo = WalletRepository(session)
    wallet = await wallet_repo.get_by_id(wallet_id)
    if not wallet or wallet.user_id != user.id:
        raise HTTPException(status_code=404, detail="Wallet not found")
    await wallet_repo.delete(wallet_id)
    return {"success": True}
