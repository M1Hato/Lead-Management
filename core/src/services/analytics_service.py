from datetime import date, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from src.models.leads_model import LeadModel


class AnalyticsService:

    @staticmethod
    async def get_group_leads(
            db: AsyncSession,
            affiliate_id: str,
            date_from: date,
            date_to: date,
            limit: int,
            offset: int,
            group_by: Literal["date", "offer"]
    ):

        #межі часу
        start_date = datetime.combine(date_from, datetime.min.time())
        end_date = datetime.combine(date_to, datetime.max.time())

        query = select(LeadModel).where(
            LeadModel.affiliate_id == affiliate_id,
            LeadModel.created_at >= start_date,
            LeadModel.created_at <= end_date,
        ).order_by(LeadModel.created_at.desc()).limit(limit).offset(offset)

        result = await db.execute(query)
        leads = result.scalars().all()

        grouped_leads = {}
        for lead in leads:
            if group_by == "date":
                key = lead.created_at.date().isoformat()
            else:
                key = str(lead.offer_id)

            if key not in grouped_leads:
                grouped_leads[key] = {
                    "count": 0,
                    "lead": []
                }

            grouped_leads[key]["count"] += 1
            grouped_leads[key]["lead"].append({
                "id": lead.id,
                "name": lead.name,
                "phone": lead.phone,
                "country": lead.country,
                "offer_id": str(lead.offer_id),
                "created_at": lead.created_at.isoformat()
            })

        return grouped_leads




