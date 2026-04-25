from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from src.cfg.redis import get_redis
from src.schemas.lead_schemas import LeadCreate
from src.cfg.auth_utils import verify_token

router = APIRouter(
    prefix="/lead",
    tags=["Lead"]
)

@router.post("/create")
async def create_lead(
        data: LeadCreate,
        redis = Depends(get_redis),
        token_affiliate: Depends = Depends(verify_token)
):
    if str(data.affiliate_id) != str(token_affiliate):
        raise HTTPException(status_code=403, detail="Invalid affiliate id")

    lead_data = data.model_dump_json()

    await redis.lpush("leads_queue", lead_data)
    return {"status": "ok", "message": "Lead accepted and queued"}