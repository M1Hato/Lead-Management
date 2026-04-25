from fastapi import FastAPI
from src.api import leads

app = FastAPI(title="Lead API")
app.include_router(leads.router)
