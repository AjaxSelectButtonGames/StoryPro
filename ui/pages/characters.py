"""
Characters Page - Character management and details
"""

import flet as ft
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../storyloom_core'))

from storyloom.services.project_service import ProjectService
from storyloom.models.character import Character


class CharactersPage:
    """Character management interface"""
    
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service
        self.selected_character = None
        self.character_list = ft.ListView(
            expand=True,
            spacing=5,
        )
        self.details_column = ft.Column(
            [
                ft.Text("Select a character to view details", color=ft.colors.GREY_700),
            ],
            expand=True,
        )
    
    def build(self) -> ft.Container:
        """Build the characters page UI"""
        self._refresh_character_list()
        
        return ft.Container(
            content=ft.Row(
                [
                    # Characters list
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Characters", size=18, weight=ft.FontWeight.BOLD),
                                ft.Divider(height=1),
                                self.character_list,
                                ft.Button(
                                    "Add Character",
                                    icon=ft.icons.ADD,
                                    width=float('inf'),
                                    on_click=self._add_character,
                                ),
                            ],
                            spacing=10,
                            expand=True,
                        ),
                        width=300,
                        padding=15,
                        border=ft.border.only(right=ft.BorderSide(1, ft.colors.GREY_300)),
                    ),
                    
                    # Character details
                    ft.Container(
                        content=self.details_column,
                        padding=15,
                        expand=True,
                    ),
                ],
                expand=True,
                spacing=0,
            ),
            expand=True,
        )
    
    def _refresh_character_list(self):
        """Refresh the character list from project"""
        self.character_list.controls.clear()
        characters = self.project_service.get_characters()
        
        for char in characters:
            item = self._create_character_item(char)
            self.character_list.controls.append(item)
    
    def _create_character_item(self, character: Character) -> ft.Container:
        """Create a character list item"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(character.name, weight=ft.FontWeight.BOLD),
                    ft.Text(character.role or "No role assigned", size=12, color=ft.colors.GREY_700),
                ],
                spacing=2,
            ),
            padding=10,
            border_radius=5,
            bgcolor=ft.colors.GREY_100,
            on_click=lambda e, char=character: self._select_character(char),
        )
    
    def _select_character(self, character: Character):
        """Select a character to view details"""
        self.selected_character = character
        self._show_character_details(character)
    
    def _show_character_details(self, character: Character):
        """Show character details in the details panel"""
        name_field = ft.TextField(label="Name", value=character.name)
        role_field = ft.TextField(label="Role", value=character.role)
        description_field = ft.TextField(
            label="Description",
            value=character.description,
            multiline=True,
            min_lines=4,
        )
        goals_field = ft.TextField(
            label="Goals (comma-separated)",
            value=", ".join(character.goals),
            multiline=True,
            min_lines=3,
        )
        
        def save_changes(e):
            """Save character changes"""
            character.name = name_field.value
            character.role = role_field.value
            character.description = description_field.value
            character.goals = [g.strip() for g in goals_field.value.split(",") if g.strip()]
            
            self.project_service.update_character(character)
            self._refresh_character_list()
            
            # Show confirmation
            snack = ft.SnackBar(
                ft.Text("Character updated"),
                duration=2000,
            )
            self.details_column.page.overlay.append(snack)
            snack.open = True
            self.details_column.page.update()
        
        def delete_character(e):
            """Delete character"""
            if self.project_service.remove_character(character.id):
                self._refresh_character_list()
                self.selected_character = None
                self.details_column.controls.clear()
                self.details_column.controls.append(
                    ft.Text("Select a character to view details", color=ft.colors.GREY_700)
                )
                self.details_column.page.update()
        
        self.details_column.controls.clear()
        self.details_column.controls.extend([
            ft.Row([
                ft.Text(character.name, size=20, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.IconButton(
                    ft.icons.DELETE,
                    icon_size=20,
                    on_click=delete_character,
                ),
            ]),
            ft.Divider(),
            name_field,
            role_field,
            description_field,
            goals_field,
            ft.Row([
                ft.Button("Save", on_click=save_changes),
                ft.Button("Cancel", variant=ft.ButtonVariant.TEXT),
            ]),
        ])
        
        if self.details_column.page:
            self.details_column.page.update()
    
    def _add_character(self, e):
        """Add a new character"""
        new_char = Character(name="New Character", role="")
        self.project_service.add_character(new_char)
        self._refresh_character_list()
        self._select_character(new_char)
