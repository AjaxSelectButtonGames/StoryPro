from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

@dataclass
class Scene:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    summary: str = ""
    content: str = ""
    character_ids: List[str] = field(default_factory=list)
    location_id: Optional[str] = None
    order_index: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)