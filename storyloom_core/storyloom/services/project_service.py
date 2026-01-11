import json
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import re
from ..models.project import Project
from ..models.character import Character
from ..models.scene import Scene
from ..models.location import Location


class ProjectService:
    """Service for managing story projects"""
    
    def __init__(self, projects_dir: str = "projects"):
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(exist_ok=True)
        self.current_project: Optional[Project] = None
    
    def create_project(self, title: str = "Untitled Project") -> Project:
        """Create a new project"""
        project = Project(title=title)
        self.current_project = project
        return project
    
    def open_project(self, file_path: str) -> Optional[Project]:
        """Open a project from file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                project = self._deserialize_project(data)
                project.file_path = file_path
                self.current_project = project
                return project
        except Exception as e:
            print(f"Error opening project: {e}")
            return None
    
    def save_project(self, project: Optional[Project] = None) -> bool:
        """Save project to file"""
        proj = project or self.current_project
        if not proj:
            return False
        
        try:
            # Generate file path if not set
            if not proj.file_path:
                filename = f"{proj.title.replace(' ', '_')}.story"
                proj.file_path = str(self.projects_dir / filename)
            
            # Create directory if needed
            Path(proj.file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Serialize and save
            data = self._serialize_project(proj)
            with open(proj.file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
    
    def detect_characters_in_text(self, text: str) -> List[Character]:
        """Auto-detect characters from text content"""
        # Find capitalized words (potential names)
        potential_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Filter common words and duplicates
        common_words = {
            'The', 'And', 'But', 'That', 'This', 'From', 'With', 'Not',
            'What', 'When', 'Where', 'Why', 'How', 'Which', 'Who', 'About',
            'After', 'Before', 'During', 'Without', 'Within', 'Through',
            'Between', 'Into', 'Over', 'Under', 'Above', 'Below'
        }
        
        names = list(set(n for n in potential_names if n not in common_words and len(n) > 2))
        
        # Check for existing characters
        existing_names = {c.name for c in self.current_project.characters} if self.current_project else set()
        
        # Create new characters
        new_characters = []
        for name in sorted(names):
            if name not in existing_names:
                char = Character(name=name, role="")
                new_characters.append(char)
        
        return new_characters
    
    def add_character(self, character: Character) -> bool:
        """Add character to current project"""
        if self.current_project:
            # Check if character already exists
            if not any(c.name == character.name for c in self.current_project.characters):
                self.current_project.characters.append(character)
                return True
        return False
    
    def remove_character(self, character_id: str) -> bool:
        """Remove character from current project"""
        if self.current_project:
            self.current_project.characters = [c for c in self.current_project.characters if c.id != character_id]
            return True
        return False
    
    def update_character(self, character: Character) -> bool:
        """Update character in current project"""
        if self.current_project:
            for i, c in enumerate(self.current_project.characters):
                if c.id == character.id:
                    self.current_project.characters[i] = character
                    return True
        return False
    
    def get_characters(self) -> List[Character]:
        """Get all characters in current project"""
        return self.current_project.characters if self.current_project else []
    
    def add_location(self, location: Location) -> bool:
        """Add location to current project"""
        if self.current_project:
            self.current_project.locations.append(location)
            return True
        return False
    
    def get_locations(self) -> List[Location]:
        """Get all locations in current project"""
        return self.current_project.locations if self.current_project else []
    
    def update_project_content(self, content: str) -> None:
        """Update main story content"""
        if self.current_project:
            self.current_project.content = content
            self.current_project.updated_at = datetime.now()
    
    def _serialize_project(self, project: Project) -> dict:
        """Serialize project to dict for JSON"""
        return {
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'content': project.content,
            'characters': [
                {
                    'id': c.id,
                    'name': c.name,
                    'role': c.role,
                    'description': c.description,
                    'goals': c.goals,
                    'created_at': c.created_at.isoformat(),
                    'updated_at': c.updated_at.isoformat(),
                }
                for c in project.characters
            ],
            'locations': [
                {
                    'id': l.id,
                    'name': l.name,
                    'type': l.type,
                    'description': l.description,
                    'created_at': l.created_at.isoformat(),
                    'updated_at': l.updated_at.isoformat(),
                }
                for l in project.locations
            ],
            'scenes': [
                {
                    'id': s.id,
                    'title': s.title,
                    'summary': s.summary,
                    'content': s.content,
                    'character_ids': s.character_ids,
                    'location_id': s.location_id,
                    'order_index': s.order_index,
                    'created_at': s.created_at.isoformat(),
                    'updated_at': s.updated_at.isoformat(),
                }
                for s in project.scenes
            ],
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat(),
        }
    
    def _deserialize_project(self, data: dict) -> Project:
        """Deserialize project from dict"""
        characters = [
            Character(
                id=c['id'],
                name=c['name'],
                role=c.get('role', ''),
                description=c.get('description', ''),
                goals=c.get('goals', []),
            )
            for c in data.get('characters', [])
        ]
        
        locations = [
            Location(
                id=l['id'],
                name=l['name'],
                type=l.get('type', ''),
                description=l.get('description', ''),
            )
            for l in data.get('locations', [])
        ]
        
        scenes = [
            Scene(
                id=s['id'],
                title=s['title'],
                summary=s.get('summary', ''),
                content=s.get('content', ''),
                character_ids=s.get('character_ids', []),
                location_id=s.get('location_id'),
                order_index=s.get('order_index', 0),
            )
            for s in data.get('scenes', [])
        ]
        
        return Project(
            id=data['id'],
            title=data.get('title', 'Untitled Project'),
            description=data.get('description', ''),
            content=data.get('content', ''),
            characters=characters,
            locations=locations,
            scenes=scenes,
        )
