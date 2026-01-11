"""
Integration Test - Verify all components work together
Run this to validate the setup before launching the UI
"""

import sys
import os

# Add the storyloom_core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'storyloom_core'))

def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    try:
        from storyloom.models.character import Character
        from storyloom.models.location import Location
        from storyloom.models.project import Project
        from storyloom.models.scene import Scene
        from storyloom.models.relationship import Relationship
        from storyloom.services.project_service import ProjectService
        print("  ✓ All backend modules imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_models():
    """Test that all models work"""
    print("\nTesting models...")
    try:
        from storyloom.models.character import Character
        from storyloom.models.location import Location
        from storyloom.models.project import Project
        
        # Create instances
        char = Character(name="Test Character", role="Hero")
        loc = Location(name="Test Location", type="City")
        proj = Project(title="Test Project")
        
        assert char.name == "Test Character"
        assert loc.name == "Test Location"
        assert proj.title == "Test Project"
        
        print("  ✓ All models work correctly")
        return True
    except Exception as e:
        print(f"  ✗ Model test failed: {e}")
        return False

def test_project_service():
    """Test the project service"""
    print("\nTesting ProjectService...")
    try:
        from storyloom.services.project_service import ProjectService
        from storyloom.models.character import Character
        
        service = ProjectService()
        
        # Create a project
        project = service.create_project("Test Story")
        assert project.title == "Test Story"
        print("  ✓ Project creation works")
        
        # Test character detection
        text = """
        Once upon a time, Alice met Bob in the forest.
        Alice and Charlie became friends.
        They met Destiny and Edward.
        """
        
        detected = service.detect_characters_in_text(text)
        print(f"  ✓ Character detection works (found {len(detected)} characters)")
        
        # Add characters
        for char in detected:
            service.add_character(char)
        
        chars = service.get_characters()
        assert len(chars) > 0
        print(f"  ✓ Character management works ({len(chars)} characters in project)")
        
        # Update content
        service.update_project_content(text)
        assert service.current_project.content == text
        print("  ✓ Content management works")
        
        # Test location management
        from storyloom.models.location import Location
        loc = Location(name="Dark Forest", type="Natural")
        service.add_location(loc)
        locations = service.get_locations()
        assert len(locations) > 0
        print(f"  ✓ Location management works ({len(locations)} location)")
        
        return True
    except Exception as e:
        print(f"  ✗ ProjectService test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_imports():
    """Test that UI modules can be imported"""
    print("\nTesting UI modules...")
    try:
        # We need to add both paths for the UI to work
        sys.path.insert(0, os.path.dirname(__file__))
        
        from ui.pages.editor import EditorPage
        from ui.pages.characters import CharactersPage
        from ui.pages.worldbuilding import WorldbuildingPage
        
        print("  ✓ All UI modules can be imported")
        return True
    except Exception as e:
        print(f"  ✗ UI import test failed: {e}")
        print("    Note: This is expected if Flet is not installed")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("StoryPro Integration Tests")
    print("=" * 60)
    
    results = []
    
    # Run critical tests
    results.append(("Import Test", test_imports()))
    results.append(("Model Test", test_models()))
    results.append(("ProjectService Test", test_project_service()))
    results.append(("UI Import Test", test_ui_imports()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! You're ready to run:")
        print("   python run.py")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
