import hashlib
import hmac
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.core.config import get_settings
from app.core.database import get_db
from app.database.repositories.user_repo import UserRepository

router = APIRouter()
settings = get_settings()


async def get_current_user(
    authorization: str = Header(None),
    session: AsyncSession = Depends(get_db),
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        telegram_id = payload.get("sub")
        if not telegram_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(int(telegram_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def verify_telegram_init_data(init_data: str, bot_token: str) -> dict:
    try:
        data_check_string = "\n".join(
            sorted(k + "=" + v for k, v in [
                line.split("=", 1) for line in init_data.split("\n") if "=" in line and line.split("=", 1)[0] != "hash"
            ])
        )
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        provided_hash = dict(line.split("=", 1) for line in init_data.split("\n") if "=" in line).get("hash")
        if calculated_hash != provided_hash:
            raise HTTPException(status_code=401, detail="Invalid init data")
        return dict(line.split("=", 1) for line in init_data.split("\n") if "=" in line)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid init data")


@router.post("/auth/telegram")
async def auth_telegram(
    init_data: str,
    session: AsyncSession = Depends(get_db),
):
    data = verify_telegram_init_data(init_data, settings.bot_token)
    user_info = dict(line.split("=", 1) for line in data.get("user", "{}").split(",") if "=" in line)

    telegram_id = int(user_info.get("id", 0))
    username = user_info.get("username", "")
    first_name = user_info.get("first_name", "")

    user_repo = UserRepository(session)
    user = await user_repo.get_or_create(telegram_id, username, first_name)

    token = jwt.encode({"sub": str(telegram_id)}, settings.jwt_secret, algorithm="HS256")
    return {"token": token, "user": {"id": user.id, "telegram_id": user.telegram_id, "username": user.username}}
