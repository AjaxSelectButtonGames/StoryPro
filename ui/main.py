"""
StoryPro - Flet UI Main Application
A simple, powerful Obsidian-like writing app for authors
"""

import flet as ft
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../storyloom_core'))

from storyloom.services.project_service import ProjectService
from ui.pages.editor import EditorPage
from ui.pages.characters import CharactersPage
from ui.pages.worldbuilding import WorldbuildingPage


# Global project service instance
project_service = ProjectService()


def main(page: ft.Page):
    """Main application entry point"""
    page.title = "StoryPro - Story Writing & World Building"
    page.window.width = 1400
    page.window.height = 900
    page.padding = 0
    page.spacing = 0
    
    # Create a new project to start with
    project_service.create_project("My First Story")
    
    # Create pages
    editor_page = EditorPage(project_service)
    characters_page = CharactersPage(project_service)
    worldbuilding_page = WorldbuildingPage(project_service)
    
    # Main content container
    main_content = ft.Container(
        content=editor_page.build(),
        expand=True,
    )
    
    def handle_navigation(e):
        """Handle navigation between pages"""
        index = e.control.selected_index
        if index == 0:
            main_content.content = editor_page.build()
        elif index == 1:
            main_content.content = characters_page.build()
        elif index == 2:
            main_content.content = worldbuilding_page.build()
        page.update()
    
    # Navigation rail (sidebar)
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.EDIT,
                label="Editor",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PEOPLE,
                label="Characters",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PUBLIC,
                label="World",
            ),
        ],
        on_change=handle_navigation,
    )
    
    # Layout
    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1),
                main_content,
            ],
            expand=True,
            spacing=0,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
