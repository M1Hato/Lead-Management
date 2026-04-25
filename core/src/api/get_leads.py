from datetime import date
from typing import Literal
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.cfg.auth_utils import verify_token
from src.services.analytics_service import AnalyticsService
from src.database import get_async_session
from src.models.leads_model import LeadModel

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.get("/")
async def get_leads(
        date_from: date,
        date_to: date,
        group: Literal["date", "offer"],
        token_affiliate: Depends = Depends(verify_token),
        db: AsyncSession = Depends(get_async_session)
):
    result = await AnalyticsService.get_group_leads(
        db=db,
        group_by=group,
        date_from=date_from,
        date_to=date_to,
        affiliate_id=token_affiliate
    )
    return result