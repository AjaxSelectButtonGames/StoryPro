from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime

@dataclass
class Location:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    type: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
