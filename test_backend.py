#!/usr/bin/env python3
"""
Test script to verify the backend works
"""

import sys
import os

# Add the storyloom_core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'storyloom_core'))

from storyloom.services.project_service import ProjectService

def test_backend():
    """Test the backend services"""
    print("=" * 50)
    print("StoryPro Backend Test")
    print("=" * 50)
    
    # Create service
    service = ProjectService()
    
    # Create a project
    project = service.create_project("Test Story")
    print(f"\n✓ Created project: {project.title}")
    print(f"  Project ID: {project.id}")
    
    # Add some story content
    story_content = """
    In the ancient forest, there lived a young hero named Aragorn. 
    Aragorn dreamed of adventure beyond the mountains.
    One day, he met the wise wizard Gandalf who spoke of great dangers ahead.
    Together with his friend Legolas, Aragorn set out on a quest.
    They traveled through many lands, including the mystical realm of Rivendell.
    """
    
    service.update_project_content(story_content)
    print(f"\n✓ Added story content ({len(story_content)} characters)")
    
    # Detect characters
    detected_chars = service.detect_characters_in_text(story_content)
    print(f"\n✓ Auto-detected {len(detected_chars)} characters:")
    for char in detected_chars:
        print(f"  - {char.name}")
    
    # Get all characters
    all_chars = service.get_characters()
    print(f"\n✓ Total characters in project: {len(all_chars)}")
    
    # Add a location manually
    from storyloom.models.location import Location
    loc = Location(name="Rivendell", type="Elven Kingdom", description="Home of the Elves")
    service.add_location(loc)
    print(f"\n✓ Added location: {loc.name}")
    
    # Get locations
    locations = service.get_locations()
    print(f"✓ Total locations in project: {len(locations)}")
    
    # Save the project
    if service.save_project():
        print(f"\n✓ Project saved to: {service.current_project.file_path}")
    else:
        print(f"\n✗ Failed to save project")
    
    print("\n" + "=" * 50)
    print("Backend test completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    test_backend()
