from typing import Optional
from pydantic import BaseModel, Field

class ResponseSchema(BaseModel):
    entity_type: str
    operation: str
    count: int
    details: Optional[str] = None

class DataResponseSchema(BaseModel):
    data: ResponseSchema
