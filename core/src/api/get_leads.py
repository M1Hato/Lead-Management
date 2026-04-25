from datetime import date
from typing import Literal
from fastapi import APIRouter, Depends, Query
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
        limit: int = Query(default = 10, ge = 1, le = 100),
        offset: int = Query(default = 0, ge = 0),
        token_affiliate: Depends = Depends(verify_token),
        db: AsyncSession = Depends(get_async_session)
):
    result = await AnalyticsService.get_group_leads(
        db=db,
        group_by=group,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
        affiliate_id=token_affiliate
    )
    return result