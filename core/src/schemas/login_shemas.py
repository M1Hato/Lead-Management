import uuid
from pydantic import BaseModel

class LoginSchema(BaseModel):
    affiliate_id: uuid.UUID