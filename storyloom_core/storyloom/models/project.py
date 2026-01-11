from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime
from typing import List
from .character import Character
from .scene import Scene
from .location import Location

@dataclass
class Project:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = "Untitled Project"
    description: str = ""
    content: str = ""  # Main story text
    characters: List[Character] = field(default_factory=list)
    scenes: List[Scene] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    file_path: str = ""  # Local file path for saving
