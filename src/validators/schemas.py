from typing import Optional, Union
from pydantic import BaseModel, Field

class ResponseSchema(BaseModel):
    entity_type: str
    operation: str
    count: int
    details: Optional[Union[str, list, dict, int, float]] = None

class DataResponseSchema(BaseModel):
    data: ResponseSchema
