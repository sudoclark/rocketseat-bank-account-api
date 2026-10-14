from typing import Optional, Any
from pydantic import BaseModel

class ResponseSchema(BaseModel):
    entity_type: str
    operation: str
    count: int
    details: Optional[Any] = None

class DataResponseSchema(BaseModel):
    data: ResponseSchema
