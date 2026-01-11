from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime

@dataclass
class Relationship:
    id: str = field(default_factory=lambda: str(uuid4()))
    source_id: str = ""
    target_id: str = ""
    type: str = ""  # character_location, character_character, etc
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
