from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class Evidence(BaseModel):
    """Canonical evidence model for the platform.

    Fields are intentionally generic so adapters can populate metadata and content
    with provider-specific details while downstream components use the canonical
    fields (evidence_id, source, type, timestamp) for linking and confidence.
    """

    evidence_id: str
    source: str
    type: str
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
    content: Dict[str, Any] = Field(default_factory=dict)
    # Confidence (0.0 - 1.0) that this evidence is correct/complete
    confidence: Optional[float] = None

    class Config:
        frozen = True
        json_encoders = {datetime: lambda v: v.isoformat()}
