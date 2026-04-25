import asyncio
import json
import logging
import uuid
from sqlalchemy.exc import IntegrityError

from src.models.affiliates_model import AffiliatesModel
from src.models.offers_model import OffersModel
from src.database import get_async_session
from src.models.leads_model import LeadModel
from src.cfg.redis import redis_client
from src.database import new_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

async def process_leads():
    logger.info("Starting to process leads")

    while True:
        try:
            result = await redis_client.brpop("leads_queue", timeout=0)
            if result is None:
                logger.info("No leads found, waiting 10 seconds")
                continue

            queue_name, data = result
            lead_dict = json.loads(data)

            name = str(lead_dict.get('name', ' ')).strip()
            phone = str(lead_dict.get('phone', ' ')).strip()
            offer_id = str(lead_dict.get('offer_id', ' ')).strip()
            affiliate_id = str(lead_dict.get('affiliate_id', ' ')).strip()

            dedup_key = f"dedup:{name}:{phone}:{offer_id}:{affiliate_id}"
            is_duplicate = await redis_client.get(dedup_key)

            if is_duplicate:
                logger.info("Duplicate found")
                continue

            #if not found
            await redis_client.set(dedup_key, "exists", ex=600)

            logger.info(f"Processing lead for: {lead_dict.get('name')}")

            #write to database
            try:
                async with new_session() as session:
                    new_lead = LeadModel(
                        name=name,
                        phone=phone,
                        country=lead_dict.get('country'),
                        offer_id=uuid.UUID(offer_id),
                        affiliate_id=uuid.UUID(affiliate_id),
                    )
                    session.add(new_lead)
                    await session.commit()
                    logger.info(f"Successfully added new lead: {new_lead}")
            except IntegrityError:
                logger.error(f"Offer or Affiliate not found. Lead skipped.")
                continue

        except Exception as e:
            logger.exception(f"Error processing leads {e}")

if __name__ == "__main__":
    try:
        asyncio.run(process_leads())
    except KeyboardInterrupt:
        logger.info("Stopping worker")