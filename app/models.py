from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4


class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    store_id: str
    camera_id: str
    visitor_id: str
    event_type: str
    timestamp: datetime
    zone_id: Optional[str] = None
    dwell_ms: Optional[int] = None
    is_staff: bool = False
    confidence: float = 1.0
    metadata: Dict[str, Any] = {}