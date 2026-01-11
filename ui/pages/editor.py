"""
Editor Page - Main writing interface with auto character detection
"""

import flet as ft
import re
from typing import Set
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../storyloom_core'))

from storyloom.services.project_service import ProjectService
from storyloom.models.character import Character


class EditorPage:
    """Main text editor with automatic character detection"""
    
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service
        self.text_editor = ft.TextField(
            multiline=True,
            min_lines=30,
            expand=True,
            focused_border_color=ft.colors.PRIMARY,
        )
        self.detected_characters = set()
        self.character_chips = ft.Row(
            wrap=True,
            spacing=10,
        )
        self.word_count = ft.Text("Words: 0 | Characters: 0", size=12, color=ft.colors.GREY_700)
        self.title_field = ft.TextField(
            label="Project Title",
            value="Untitled Project",
            width=400,
        )
        self.status_text = ft.Text("Ready", size=11, color=ft.colors.GREY_700)
        
        # Bind text change event
        self.text_editor.on_change = self._on_text_change
    
    def _on_text_change(self, e):
        """Handle text changes and auto-detect characters"""
        text = self.text_editor.value
        
        # Update project content
        self.project_service.update_project_content(text)
        
        # Update word and character count
        word_count = len(text.split())
        char_count = len(text)
        self.word_count.value = f"Words: {word_count} | Characters: {char_count}"
        
        # Auto-detect character names
        new_characters = self.project_service.detect_characters_in_text(text)
        
        if new_characters:
            # Add new characters to project
            for char in new_characters:
                self.project_service.add_character(char)
            
            # Update display
            self.detected_characters = {c.name for c in self.project_service.get_characters()}
            self._update_character_chips()
        
        # Update UI
        if self.word_count.page:
            self.word_count.page.update()
    
    def _extract_names(self, text: str) -> Set[str]:
        """Extract potential character names from text"""
        # Find capitalized words (potential names)
        # This is a basic implementation
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Filter out common words
        common_words = {'The', 'And', 'But', 'That', 'This', 'From', 'With', 'Not'}
        names = {w for w in words if w not in common_words and len(w) > 2}
        
        return names
    
    def _update_character_chips(self):
        """Update the character chips display"""
        self.character_chips.controls.clear()
        for char_name in sorted(self.detected_characters):
            chip = ft.Chip(
                label=ft.Text(char_name),
                on_click=lambda e, name=char_name: self._on_character_click(name),
            )
            self.character_chips.controls.append(chip)
        self.character_chips.page.update() if self.character_chips.page else None
    
    def _on_character_click(self, character_name: str):
        """Handle character chip click"""
        print(f"Clicked character: {character_name}")
        # TODO: Navigate to character details or open character panel
    
    def build(self) -> ft.Container:
        """Build the editor page UI"""
        return ft.Container(
            content=ft.Column(
                [
                    # Toolbar
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.icons.SAVE,
                                tooltip="Save Project",
                                on_click=self._save_project,
                            ),
                            ft.IconButton(
                                ft.icons.FOLDER_OPEN,
                                tooltip="Open Project",
                                on_click=self._open_project,
                            ),
                            ft.Divider(),
                            ft.IconButton(
                                ft.icons.UNDO,
                                tooltip="Undo",
                            ),
                            ft.IconButton(
                                ft.icons.REDO,
                                tooltip="Redo",
                            ),
                            ft.Divider(),
                            ft.IconButton(
                                ft.icons.FORMAT_BOLD,
                                tooltip="Bold",
                            ),
                            ft.IconButton(
                                ft.icons.FORMAT_ITALIC,
                                tooltip="Italic",
                            ),
                            ft.IconButton(
                                ft.icons.SETTINGS,
                                tooltip="Settings",
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Divider(height=1),
                    
                    # Title
                    self.title_field,
                    
                    # Detected Characters
                    ft.Text(
                        "Detected Characters:",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.GREY_700,
                    ),
                    self.character_chips,
                    
                    ft.Divider(height=1),
                    
                    # Editor
                    self.text_editor,
                    
                    # Status bar
                    ft.Row(
                        [
                            self.word_count,
                            ft.Container(expand=True),
                            self.status_text,
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                expand=True,
            ),
            padding=15,
            expand=True,
        )
    
    def _save_project(self, e):
        """Save project"""
        self.title_field.value = self.project_service.current_project.title
        if self.project_service.save_project():
            self.status_text.value = "✓ Project saved"
            self.status_text.color = ft.colors.GREEN
        else:
            self.status_text.value = "✗ Failed to save"
            self.status_text.color = ft.colors.RED
        
        if self.status_text.page:
            self.status_text.page.update()
    
    def _open_project(self, e):
        """Open project"""
        print("Open project")
        # TODO: Implement file picker
