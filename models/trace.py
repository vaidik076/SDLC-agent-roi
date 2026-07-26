from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Trace(BaseModel):
    """Canonical trace schema used by downstream evaluation and ROI engines."""

    task_id: str
    resolved: bool
    retries: int = 0
    token_usage: int = 0
    latency_seconds: float = 0.0
    human_intervention: bool = False
    tool_calls: List[dict] = Field(default_factory=list)
    raw_evidence_refs: List[str] = Field(default_factory=list)
    first_timestamp: Optional[datetime] = None
    last_timestamp: Optional[datetime] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
