# 🏗️ StoryPro Architecture & Developer Guide

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                  Flet UI (Cross-Platform)               │
│  ┌──────────────┬──────────────┬──────────────────────┐ │
│  │   Editor     │  Characters  │  World Building      │ │
│  │   Page       │  Page        │  Page                │ │
│  └──────────────┴──────────────┴──────────────────────┘ │
└──────────────────┬──────────────────────────────────────┘
                   │
         (Shared ProjectService)
                   │
┌──────────────────▼──────────────────────────────────────┐
│            ProjectService (Business Logic)              │
│  • Character Detection                                  │
│  • CRUD Operations                                      │
│  • Project Persistence                                  │
│  • Data Validation                                      │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              Data Models (Dataclasses)                  │
│  • Project  • Character  • Location                     │
│  • Scene    • Relationship                              │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│        Persistence Layer (JSON Files)                   │
│        projects/*.story                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Models (storyloom_core/storyloom/models/)

#### Character Model
```python
@dataclass
class Character:
    id: str                    # UUID
    name: str                  # Character name
    role: str                  # Role in story
    description: str           # Character description
    goals: List[str]           # Character goals
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last update timestamp
```

#### Project Model
Contains all project data:
- Core content (title, description, story text)
- Collections (characters, scenes, locations)
- Timestamps for versioning

#### Other Models
- **Scene**: Represents story scenes with character/location references
- **Location**: World-building elements
- **Relationship**: Connections between entities

### 2. ProjectService (storyloom_core/storyloom/services/)

The business logic layer. Main responsibilities:

```python
class ProjectService:
    # Project Management
    create_project(title) → Project
    open_project(path) → Project
    save_project() → bool
    
    # Character Management
    detect_characters_in_text(text) → List[Character]
    add_character(character) → bool
    update_character(character) → bool
    remove_character(id) → bool
    get_characters() → List[Character]
    
    # Location Management
    add_location(location) → bool
    get_locations() → List[Location]
    
    # Content Management
    update_project_content(content) → None
    
    # Internal Methods
    _serialize_project(project) → dict
    _deserialize_project(data) → Project
```

### 3. UI Pages (ui/pages/)

#### EditorPage
- Manages text editing
- Triggers character detection
- Handles save operations
- Displays stats (word count, etc.)

#### CharactersPage
- Shows character list
- Enables character editing
- Handles CRUD operations
- Updates character details

#### WorldbuildingPage
- Manages locations
- Displays relationships
- Prepares for story graph visualization

### 4. Main Application (ui/main.py)
- Initializes ProjectService
- Creates all page instances
- Manages navigation
- Handles page updates

---

## Data Flow Examples

### Example 1: Auto Character Detection

```
User types in Editor
    ↓
on_text_change() event
    ↓
ProjectService.update_project_content(text)
    ↓
ProjectService.detect_characters_in_text(text)
    ↓
Regex pattern finds "Aragorn", "Gandalf", etc.
    ↓
Filter out common words
    ↓
Return new Character objects
    ↓
ProjectService.add_character(char) for each new character
    ↓
UI updates character chips
    ↓
User sees: [Aragorn] [Gandalf] as clickable chips
```

### Example 2: Saving a Project

```
User clicks Save button
    ↓
EditorPage._save_project()
    ↓
ProjectService.save_project()
    ↓
Get current_project
    ↓
Call _serialize_project(project)
    ↓
Convert all objects to JSON-serializable dicts
    ↓
Create projects/ directory if needed
    ↓
Write JSON to projects/Project_Title.story
    ↓
Set file_path on project
    ↓
Update status: "✓ Project saved"
```

### Example 3: Editing a Character

```
User clicks on character in list
    ↓
CharactersPage._select_character(character)
    ↓
Display edit form with fields
    ↓
User modifies fields (name, role, description, goals)
    ↓
User clicks Save
    ↓
CharactersPage.save_changes()
    ↓
Update character object with new values
    ↓
ProjectService.update_character(character)
    ↓
Character updated in project.characters list
    ↓
UI refreshes character list
    ↓
Snackbar shows "Character updated"
```

---

## Extension Guide

### Adding a New Feature

#### 1. Add a Service Method
In `ProjectService`:
```python
def my_new_feature(self, data):
    """Description of what this does"""
    if not self.current_project:
        return False
    
    # Business logic here
    self.current_project.updated_at = datetime.now()
    return True
```

#### 2. Call from UI
```python
def my_button_click(self, e):
    result = self.project_service.my_new_feature(data)
    if result:
        self.update_ui()
```

### Adding a New Page

#### 1. Create Page Class
```python
class NewPage:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service
    
    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column([...]),
            expand=True,
        )
```

#### 2. Add to Main App
```python
from ui.pages.new_page import NewPage

new_page = NewPage(project_service)

# Add to navigation
ft.NavigationRailDestination(
    icon=ft.icons.NEW_ICON,
    label="New",
),

# Add to handler
elif index == 3:
    main_content.content = new_page.build()
```

### Enhancing Character Detection

Replace the regex pattern in `ProjectService.detect_characters_in_text()`:

```python
# Current: Simple regex
potential_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)

# Option 1: Use spaCy NER
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
potential_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

# Option 2: Use NLTK
from nltk import pos_tag, word_tokenize
tokens = word_tokenize(text)
tagged = pos_tag(tokens)
potential_names = [word for word, pos in tagged if pos == "NNP"]
```

---

## Database Migration Path

Currently using JSON files. When ready to migrate to SQLite:

```python
# Create a new storage layer
class StorageLayer:
    def save_project(self, project: Project) -> bool
    def load_project(self, id: str) -> Project
    def list_projects(self) -> List[Project]

# SQLite implementation
class SQLiteStorage(StorageLayer):
    def save_project(self, project: Project) -> bool:
        # Convert project to database rows
        # Insert/update in SQLite
        pass

# ProjectService uses storage layer
class ProjectService:
    def __init__(self, storage: StorageLayer):
        self.storage = storage
```

---

## Testing Strategy

### Unit Tests
```python
def test_character_detection():
    service = ProjectService()
    text = "Alice met Bob and Charlie"
    chars = service.detect_characters_in_text(text)
    assert len(chars) == 3
    assert any(c.name == "Alice" for c in chars)
```

### Integration Tests
See `validate_setup.py` for examples.

### UI Tests
Manual testing required (Flet doesn't have great test framework yet).

---

## Performance Considerations

1. **Large Projects**: JSON parsing might slow down with massive stories
   - Solution: Implement lazy loading for UI
   - Move to SQLite for better scalability

2. **Character Detection**: Regex might be slow on huge texts
   - Solution: Detect only new text (diff-based)
   - Consider NLP libraries for accuracy

3. **UI Responsiveness**: File I/O blocking
   - Solution: Implement async save in background thread

---

## Security Considerations

1. **File Permissions**: Ensure projects/ directory is user-owned
2. **Data Validation**: Sanitize input before storing
3. **Backup**: Recommend periodic backups of projects/
4. **Cloud Sync**: Use encryption if implementing cloud features

---

## Deployment Considerations

### Creating Executables

With Flet, you can create standalone executables:

```bash
# Windows
flet pack ui/main.py --app-version=1.0.0 --output-dir=dist

# macOS
flet pack ui/main.py --platform=macos --output-dir=dist

# Linux
flet pack ui/main.py --platform=linux --output-dir=dist
```

### Distribution
- Bundle as single executable
- Include requirements documentation
- Create installer with project templates

---

## Code Style & Standards

- Use type hints for all functions
- Add docstrings to all classes and methods
- Keep methods focused and small
- Use meaningful variable names
- Document non-obvious logic

---

## Debugging Tips

1. **Check Project State**
```python
print(f"Current project: {project_service.current_project}")
print(f"Characters: {[c.name for c in project_service.get_characters()]}")
```

2. **Monitor Events**
```python
def on_text_change(e):
    print(f"Text changed: {len(e.control.value)} chars")
    # ... rest of logic
```

3. **Validate Data**
```python
if not service.current_project:
    print("No project loaded!")
    return
```

---

## References

- **Flet Documentation**: https://flet.dev
- **Python Dataclasses**: https://docs.python.org/3/library/dataclasses.html
- **JSON Module**: https://docs.python.org/3/library/json.html

---

This architecture is scalable, maintainable, and easy to extend. Happy developing! 🚀
