from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Dict, List, Optional, Any
from typing_extensions import Self
from decimal import Decimal

class UsageItemDTO(BaseModel):
    id: Optional[int] = None
    flow_volume: Optional[float] = None
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    total_spent: Optional[Decimal] = None
    
    def to_dict(self) -> dict:
        return self.__dict__
    
class TotalSpentResultDto(BaseModel):
    amount: Optional[Decimal] = None
    usages: Optional[List[UsageItemDTO]] = None
    
    def to_dict(self) -> dict:
        return self.__dict__