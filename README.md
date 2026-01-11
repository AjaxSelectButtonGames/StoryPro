# StoryPro
Python-based writing software for Authors - An Obsidian-like story writing and world-building tool with automatic character detection and management.

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python run.py
```

The app will launch with a modern, clean UI featuring:
- **Editor**: Write your story with automatic character detection
- **Characters**: Manage detected and custom characters
- **World Building**: Organize locations, relationships, and story structure

## ✨ Key Features

### 📝 Smart Editor
- Write freely while the app detects character names in real-time
- View detected characters as interactive chips
- Real-time word and character count
- Save/load your projects

### 👥 Character Management
- Auto-detect character names from your text
- Add, edit, and delete characters
- Track roles, descriptions, and goals
- Visual character list with full details

### 🌍 World Building
- Create and manage story locations
- Track character-location relationships
- Organize your story world
- Foundation for story graph visualization

## 🏗️ Architecture

### Backend (storyloom_core/)
- **Models**: Character, Scene, Location, Relationship, Project
- **Services**: ProjectService for all business logic
- **Features**: JSON persistence, character detection, full CRUD operations

### Frontend (ui/)
- **Framework**: Flet (cross-platform, modern, responsive)
- **Pages**: Editor, Characters, World Building
- **Design**: Clean, distraction-free interface

## 📁 Project Structure

```
StoryPro/
├── storyloom_core/                 # Backend logic
│   └── storyloom/
│       ├── models/                 # Data models
│       │   ├── character.py
│       │   ├── location.py
│       │   ├── scene.py
│       │   ├── project.py
│       │   └── relationship.py
│       └── services/
│           └── project_service.py
│
├── ui/                             # Frontend (Flet)
│   ├── main.py                    # App entry point
│   └── pages/
│       ├── editor.py              # Writing interface
│       ├── characters.py          # Character management
│       └── worldbuilding.py       # World building
│
├── requirements.txt
├── run.py                          # Launch script
├── validate_setup.py               # Validation tests
└── SETUP.md                        # Detailed setup guide
```

## 🧪 Testing

### Validate Setup
```bash
python validate_setup.py
```

This runs integration tests to ensure everything is working.

### Run Backend Tests
```bash
python test_backend.py
```

## 🎯 How It Works

### Auto Character Detection
1. Start typing your story in the Editor
2. The app scans for capitalized names (e.g., "Aragorn", "Gandalf")
3. Detected characters appear as chips below the editor
4. Click any chip to view/edit character details
5. Characters are automatically added to your project

### Project Workflow
1. **Write**: Create your story in the Editor
2. **Manage**: Switch to Characters to refine character details
3. **Build**: Use World Building to organize locations and relationships
4. **Save**: Click Save to persist your project as a JSON file

## 📊 Project Storage

Projects are saved as `.story` JSON files in the `projects/` folder. Each file contains:
- Story content
- All detected/added characters with details
- Locations and relationships
- Metadata (creation date, updates, etc.)

## 🔧 Technology Stack

- **Language**: Python 3.8+
- **UI Framework**: Flet (Flutter-based)
- **Data Format**: JSON
- **Persistence**: File-based (JSON)

## 🚀 Future Enhancements

- Enhanced NLP-based character detection
- Visual story graph visualization
- Character relationship mapping
- Scene organization and outlining
- Export to DOCX, PDF, Markdown
- Cloud sync and version history
- AI-powered suggestions

## 📖 Documentation

See [SETUP.md](SETUP.md) for detailed setup instructions and feature walkthroughs.

## 💡 Development

The codebase is clean and well-documented. To extend:

1. **Add Models**: Create new dataclasses in `storyloom_core/storyloom/models/`
2. **Add Services**: Extend `ProjectService` with new methods
3. **Add UI Pages**: Create new page classes in `ui/pages/`

All imports are properly configured for easy development.

## 📝 License

MIT License - Feel free to use and modify!

