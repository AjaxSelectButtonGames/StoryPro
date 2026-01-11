from dataclasses import dataclass, field
from uuid import uuid4
from typing import List
from datetime import datetime

@dataclass
class Character:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    role: str = ""
    description: str = ""
    goals: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    