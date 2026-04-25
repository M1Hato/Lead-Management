from fastapi import FastAPI
from src.api import login_affiliate
from src.api import get_leads

app = FastAPI(title="Core API")

app.include_router(login_affiliate.router)
app.include_router(get_leads.router)