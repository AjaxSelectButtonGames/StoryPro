"""
World Building Page - Story graph and world elements visualization
"""

import flet as ft
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../storyloom_core'))

from storyloom.services.project_service import ProjectService
from storyloom.models.location import Location


class WorldbuildingPage:
    """World building and story graph interface"""
    
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service
        self.locations_list = ft.Column(expand=True)
        self.selected_location = None
    
    def build(self) -> ft.Container:
        """Build the world building page UI"""
        self._refresh_locations_list()
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("World Building", size=20, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.IconButton(
                                ft.icons.ADD_CIRCLE_OUTLINE,
                                tooltip="Add Location",
                                on_click=self._add_location,
                            ),
                        ],
                    ),
                    
                    ft.Tabs(
                        tabs=[
                            ft.Tab(
                                text="Locations",
                                content=self._build_locations_tab(),
                            ),
                            ft.Tab(
                                text="Relationships",
                                content=self._build_relationships_tab(),
                            ),
                            ft.Tab(
                                text="Story Graph",
                                content=self._build_story_graph_tab(),
                            ),
                        ],
                        expand=True,
                    ),
                ],
                expand=True,
                spacing=15,
            ),
            padding=15,
            expand=True,
        )
    
    def _refresh_locations_list(self):
        """Refresh the locations list"""
        self.locations_list.controls.clear()
        locations = self.project_service.get_locations()
        
        for loc in locations:
            card = self._create_location_card(loc)
            self.locations_list.controls.append(card)
    
    def _build_locations_tab(self) -> ft.Container:
        """Build locations tab"""
        self._refresh_locations_list()
        return ft.Container(
            content=self.locations_list,
        )
    
    def _build_relationships_tab(self) -> ft.Container:
        """Build relationships tab"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Character & Location Relationships", color=ft.colors.GREY_700),
                    ft.Text("Relationships will be automatically detected from your story", size=12),
                    ft.Divider(),
                    ft.Text(f"Total Characters: {len(self.project_service.get_characters())}"),
                    ft.Text(f"Total Locations: {len(self.project_service.get_locations())}"),
                ],
                spacing=10,
            ),
        )
    
    def _build_story_graph_tab(self) -> ft.Container:
        """Build story graph tab"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Story Graph Visualization", color=ft.colors.GREY_700),
                    ft.Text("Your story structure will be visualized here", size=12),
                    ft.Divider(),
                    ft.Text(f"Detected Scenes: 0"),
                    ft.Text(f"Character Appearances: {len(self.project_service.get_characters())}"),
                ],
                spacing=10,
            ),
        )
    
    def _create_location_card(self, location: Location) -> ft.Card:
        """Create a location card"""
        def edit_location(e):
            """Edit location"""
            name_field = ft.TextField(label="Name", value=location.name)
            type_field = ft.TextField(label="Type", value=location.type)
            desc_field = ft.TextField(
                label="Description",
                value=location.description,
                multiline=True,
                min_lines=3,
            )
            
            def save_changes(e):
                location.name = name_field.value
                location.type = type_field.value
                location.description = desc_field.value
                self._refresh_locations_list()
                
            def delete_loc(e):
                self.project_service.current_project.locations.remove(location)
                self._refresh_locations_list()
            
            dialog = ft.AlertDialog(
                title=ft.Text("Edit Location"),
                content=ft.Column([
                    name_field,
                    type_field,
                    desc_field,
                ], spacing=10),
                actions=[
                    ft.TextButton("Delete", on_click=delete_loc),
                    ft.TextButton("Cancel"),
                    ft.TextButton("Save", on_click=save_changes),
                ],
            )
            
            self.locations_list.page.dialog = dialog
            dialog.open = True
            self.locations_list.page.update()
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(
                                            location.name,
                                            weight=ft.FontWeight.BOLD,
                                            size=14,
                                        ),
                                        ft.Text(
                                            location.type,
                                            size=12,
                                            color=ft.colors.GREY_700,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                                ft.Container(expand=True),
                                ft.IconButton(
                                    ft.icons.EDIT,
                                    icon_size=18,
                                    on_click=edit_location,
                                ),
                            ],
                        ),
                        ft.Text(location.description, size=12),
                    ],
                    spacing=10,
                ),
                padding=15,
            ),
        )
    
    def _add_location(self, e):
        """Add a new location"""
        new_location = Location(name="New Location", type="Unknown")
        self.project_service.add_location(new_location)
        self._refresh_locations_list()
