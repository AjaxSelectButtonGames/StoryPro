"""
StoryPro - PySimpleGUI Main Application
A simple, powerful writing app for authors
"""

import PySimpleGUI as sg
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../storyloom_core'))

from storyloom.services.project_service import ProjectService
from storyloom.models.character import Character
from storyloom.models.location import Location

# Set theme
sg.theme('DarkBlue3')

# Global project service instance
project_service = ProjectService()


def create_editor_tab():
    """Create editor tab layout"""
    return [
        [sg.Text("Editor", font=("Arial", 14, "bold"))],
        [
            sg.Column([
                [sg.Button("Save", key="-SAVE-"), sg.Button("Open", key="-OPEN-"), 
                 sg.Text("", key="-STATUS-", text_color="white")],
                [sg.Text("Project Title:"), sg.InputText("My First Story", key="-TITLE-", size=(40, 1))],
            ]),
        ],
        [sg.Multiline(size=(80, 20), key="-EDITOR-", font=("Arial", 10))],
        [
            sg.Column([
                [sg.Text("Detected Characters:", font=("Arial", 10, "bold"))],
                [sg.Listbox([], size=(60, 4), key="-CHAR-CHIPS-", select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, 
                           enable_events=True, font=("Arial", 9))],
            ])
        ],
        [sg.Text("Words: 0 | Characters: 0 | Status: Ready", key="-STATS-", font=("Arial", 9))],
    ]


def create_characters_tab():
    """Create characters tab layout"""
    return [
        [sg.Text("Characters", font=("Arial", 14, "bold"))],
        [
            sg.Column([
                [sg.Button("Add", key="-ADD-CHAR-"), sg.Button("Edit", key="-EDIT-CHAR-"), 
                 sg.Button("Delete", key="-DEL-CHAR-")],
                [sg.Listbox([], size=(25, 20), key="-CHAR-LIST-", select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                           enable_events=True, font=("Arial", 10))],
            ], vertical_alignment="top"),
            sg.Column([
                [sg.Text("Character Details", font=("Arial", 12, "bold"))],
                [sg.Text("Name:"), sg.InputText("", key="-CHAR-NAME-", disabled=True, size=(30, 1))],
                [sg.Text("Role:"), sg.InputText("", key="-CHAR-ROLE-", disabled=True, size=(30, 1))],
                [sg.Text("Description:"), 
                 sg.Multiline("", key="-CHAR-DESC-", disabled=True, size=(40, 6))],
                [sg.Text("Goals:"), 
                 sg.Multiline("", key="-CHAR-GOALS-", disabled=True, size=(40, 4))],
                [sg.Button("Save Character", key="-SAVE-CHAR-", disabled=True), 
                 sg.Button("Cancel", key="-CANCEL-CHAR-", disabled=True)],
            ], vertical_alignment="top"),
        ],
    ]


def create_world_tab():
    """Create world building tab layout"""
    return [
        [sg.Text("World Building", font=("Arial", 14, "bold"))],
        [
            sg.TabGroup([
                [
                    sg.Tab("Locations", [
                        [sg.Button("Add Location", key="-ADD-LOC-")],
                        [sg.Listbox([], size=(60, 15), key="-LOC-LIST-", 
                                   font=("Arial", 10))],
                    ]),
                    sg.Tab("Relationships", [
                        [sg.Text("Character & Location Relationships", font=("Arial", 10, "bold"))],
                        [sg.Text(f"Total Characters: {len(project_service.get_characters())}", 
                                key="-REL-CHARS-")],
                        [sg.Text(f"Total Locations: {len(project_service.get_locations())}", 
                                key="-REL-LOCS-")],
                    ]),
                    sg.Tab("Story Graph", [
                        [sg.Text("Story Graph Visualization", font=("Arial", 10, "bold"))],
                        [sg.Text("Your story structure will be visualized here")],
                    ]),
                ]
            ])
        ],
    ]


def update_editor_stats():
    """Update editor statistics"""
    text = window["-EDITOR-"].get()
    word_count = len(text.split())
    char_count = len(text)
    window["-STATS-"].update(f"Words: {word_count} | Characters: {char_count} | Status: Ready")


def update_character_list():
    """Update character list display"""
    characters = project_service.get_characters()
    char_names = [f"{c.name} ({c.role})" if c.role else c.name for c in characters]
    window["-CHAR-LIST-"].update(char_names)
    window["-CHAR-CHIPS-"].update(char_names)


def detect_and_add_characters():
    """Detect characters from editor text"""
    text = window["-EDITOR-"].get()
    new_chars = project_service.detect_characters_in_text(text)
    
    if new_chars:
        for char in new_chars:
            project_service.add_character(char)
        update_character_list()


def update_locations_list():
    """Update locations list display"""
    locations = project_service.get_locations()
    loc_names = [f"{l.name} ({l.type})" if l.type else l.name for l in locations]
    window["-LOC-LIST-"].update(loc_names)


def create_main_window():
    """Create the main application window"""
    layout = [
        [sg.Text("StoryPro - Story Writing & World Building", font=("Arial", 16, "bold"))],
        [
            sg.TabGroup([
                [
                    sg.Tab("Editor", create_editor_tab()),
                    sg.Tab("Characters", create_characters_tab()),
                    sg.Tab("World", create_world_tab()),
                ]
            ])
        ],
    ]
    
    return sg.Window("StoryPro", layout, size=(1000, 700), finalize=True)


def main():
    """Main application"""
    global window
    
    # Create initial project
    project_service.create_project("My First Story")
    
    # Create window
    window = create_main_window()
    
    # Event loop
    while True:
        event, values = window.read(timeout=500)
        
        if event == sg.WINDOW_CLOSED:
            break
        
        # Editor events
        elif event == "-EDITOR-":
            detect_and_add_characters()
            update_editor_stats()
        
        elif event == "-SAVE-":
            project_service.current_project.title = values["-TITLE-"]
            project_service.update_project_content(values["-EDITOR-"])
            if project_service.save_project():
                window["-STATUS-"].update("✓ Project saved!", text_color="green")
            else:
                window["-STATUS-"].update("✗ Save failed", text_color="red")
        
        # Character events
        elif event == "-CHAR-LIST-" and values["-CHAR-LIST-"]:
            chars = project_service.get_characters()
            selected = window["-CHAR-LIST-"].get_indexes()
            if selected:
                char = chars[selected[0]]
                window["-CHAR-NAME-"].update(disabled=False, value=char.name)
                window["-CHAR-ROLE-"].update(disabled=False, value=char.role)
                window["-CHAR-DESC-"].update(disabled=False, value=char.description)
                window["-CHAR-GOALS-"].update(disabled=False, value=", ".join(char.goals))
                window["-SAVE-CHAR-"].update(disabled=False)
                window["-CANCEL-CHAR-"].update(disabled=False)
        
        elif event == "-ADD-CHAR-":
            new_char = Character(name="New Character")
            project_service.add_character(new_char)
            update_character_list()
        
        elif event == "-DEL-CHAR-":
            chars = project_service.get_characters()
            selected = window["-CHAR-LIST-"].get_indexes()
            if selected:
                project_service.remove_character(chars[selected[0]].id)
                update_character_list()
                window["-CHAR-NAME-"].update("", disabled=True)
                window["-CHAR-ROLE-"].update("", disabled=True)
                window["-CHAR-DESC-"].update("", disabled=True)
                window["-CHAR-GOALS-"].update("", disabled=True)
                window["-SAVE-CHAR-"].update(disabled=True)
                window["-CANCEL-CHAR-"].update(disabled=True)
        
        elif event == "-SAVE-CHAR-":
            chars = project_service.get_characters()
            selected = window["-CHAR-LIST-"].get_indexes()
            if selected:
                char = chars[selected[0]]
                char.name = values["-CHAR-NAME-"]
                char.role = values["-CHAR-ROLE-"]
                char.description = values["-CHAR-DESC-"]
                char.goals = [g.strip() for g in values["-CHAR-GOALS-"].split(",") if g.strip()]
                project_service.update_character(char)
                update_character_list()
        
        elif event == "-CANCEL-CHAR-":
            window["-CHAR-NAME-"].update("", disabled=True)
            window["-CHAR-ROLE-"].update("", disabled=True)
            window["-CHAR-DESC-"].update("", disabled=True)
            window["-CHAR-GOALS-"].update("", disabled=True)
            window["-SAVE-CHAR-"].update(disabled=True)
            window["-CANCEL-CHAR-"].update(disabled=True)
        
        # Location events
        elif event == "-ADD-LOC-":
            new_loc = Location(name="New Location", type="Unknown")
            project_service.add_location(new_loc)
            update_locations_list()


if __name__ == "__main__":
    main()
