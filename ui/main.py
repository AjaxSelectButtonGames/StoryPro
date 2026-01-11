"""
StoryPro - Tkinter UI Main Application
A simple, powerful writing app for authors - NO DEPENDENCIES!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../storyloom_core'))

from storyloom.services.project_service import ProjectService
from storyloom.models.character import Character
from storyloom.models.location import Location

# Global project service instance
project_service = ProjectService()


class StoryProApp:
    """Main StoryPro Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("StoryPro - Story Writing & World Building")
        self.root.geometry("1000x700")
        
        # Create initial project
        project_service.create_project("My First Story")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.editor_tab = ttk.Frame(self.notebook)
        self.characters_tab = ttk.Frame(self.notebook)
        self.world_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.editor_tab, text="Editor")
        self.notebook.add(self.characters_tab, text="Characters")
        self.notebook.add(self.world_tab, text="World Building")
        
        # Initialize tabs
        self.setup_editor_tab()
        self.setup_characters_tab()
        self.setup_world_tab()
    
    def setup_editor_tab(self):
        """Setup editor tab"""
        # Toolbar
        toolbar = ttk.Frame(self.editor_tab)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Save", command=self.save_project).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Open", command=self.open_project).pack(side=tk.LEFT, padx=2)
        self.status_label = ttk.Label(toolbar, text="Ready", foreground="green")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Title
        title_frame = ttk.Frame(self.editor_tab)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(title_frame, text="Project Title:").pack(side=tk.LEFT)
        self.title_var = tk.StringVar(value="My First Story")
        ttk.Entry(title_frame, textvariable=self.title_var, width=40).pack(side=tk.LEFT, padx=5)
        
        # Editor
        editor_frame = ttk.Frame(self.editor_tab)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_editor = scrolledtext.ScrolledText(editor_frame, font=("Arial", 10), height=15)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        self.text_editor.bind("<<Change>>", self.on_text_change)
        self.text_editor.bind("<KeyRelease>", self.on_text_change)
        
        # Character chips
        chips_frame = ttk.LabelFrame(self.editor_tab, text="Detected Characters")
        chips_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.chips_var = tk.StringVar()
        self.character_chips = tk.Listbox(chips_frame, listvariable=self.chips_var, height=3, 
                                         font=("Arial", 9))
        self.character_chips.pack(fill=tk.BOTH, expand=True)
        self.character_chips.bind("<<ListboxSelect>>", self.on_chip_select)
        
        # Stats
        self.stats_label = ttk.Label(self.editor_tab, text="Words: 0 | Characters: 0", 
                                    font=("Arial", 9))
        self.stats_label.pack(side=tk.BOTTOM, padx=5, pady=5, anchor=tk.W)
    
    def setup_characters_tab(self):
        """Setup characters tab"""
        # Buttons
        btn_frame = ttk.Frame(self.characters_tab)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(btn_frame, text="Add", command=self.add_character).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Edit", command=self.edit_character).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_character).pack(side=tk.LEFT, padx=2)
        
        # Main frame
        main_frame = ttk.Frame(self.characters_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left: Character list
        left_frame = ttk.LabelFrame(main_frame, text="Characters")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        self.char_listbox = tk.Listbox(left_frame, font=("Arial", 10), width=25, height=20)
        self.char_listbox.pack(fill=tk.BOTH, expand=True)
        self.char_listbox.bind("<<ListboxSelect>>", self.on_char_select)
        
        # Right: Character details
        right_frame = ttk.LabelFrame(main_frame, text="Details")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(right_frame, text="Name:").pack(anchor=tk.W)
        self.char_name_var = tk.StringVar()
        self.char_name_entry = ttk.Entry(right_frame, textvariable=self.char_name_var, state=tk.DISABLED)
        self.char_name_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(right_frame, text="Role:").pack(anchor=tk.W)
        self.char_role_var = tk.StringVar()
        self.char_role_entry = ttk.Entry(right_frame, textvariable=self.char_role_var, state=tk.DISABLED)
        self.char_role_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(right_frame, text="Description:").pack(anchor=tk.W)
        self.char_desc_text = scrolledtext.ScrolledText(right_frame, font=("Arial", 9), height=5, state=tk.DISABLED)
        self.char_desc_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(right_frame, text="Goals (comma-separated):").pack(anchor=tk.W)
        self.char_goals_text = scrolledtext.ScrolledText(right_frame, font=("Arial", 9), height=3, state=tk.DISABLED)
        self.char_goals_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        btn_frame2 = ttk.Frame(right_frame)
        btn_frame2.pack(fill=tk.X, pady=5)
        self.save_char_btn = ttk.Button(btn_frame2, text="Save", command=self.save_character, state=tk.DISABLED)
        self.save_char_btn.pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="Cancel", command=self.cancel_edit).pack(side=tk.LEFT, padx=2)
        
        # Refresh list
        self.refresh_character_list()
    
    def setup_world_tab(self):
        """Setup world building tab"""
        # Notebook for sub-tabs
        world_notebook = ttk.Notebook(self.world_tab)
        world_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Locations tab
        locations_frame = ttk.Frame(world_notebook)
        world_notebook.add(locations_frame, text="Locations")
        
        ttk.Button(locations_frame, text="Add Location", command=self.add_location).pack(padx=5, pady=5)
        
        self.locations_listbox = tk.Listbox(locations_frame, font=("Arial", 10))
        self.locations_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh_locations_list()
        
        # Relationships tab
        rel_frame = ttk.Frame(world_notebook)
        world_notebook.add(rel_frame, text="Relationships")
        
        ttk.Label(rel_frame, text="Character & Location Relationships", font=("Arial", 11, "bold")).pack(padx=5, pady=5)
        ttk.Label(rel_frame, text=f"Total Characters: {len(project_service.get_characters())}").pack(anchor=tk.W, padx=5)
        ttk.Label(rel_frame, text=f"Total Locations: {len(project_service.get_locations())}").pack(anchor=tk.W, padx=5)
        
        # Story Graph tab
        graph_frame = ttk.Frame(world_notebook)
        world_notebook.add(graph_frame, text="Story Graph")
        ttk.Label(graph_frame, text="Story Graph Visualization", font=("Arial", 11, "bold")).pack(padx=5, pady=5)
        ttk.Label(graph_frame, text="Your story structure will be visualized here").pack(anchor=tk.W, padx=5)
    
    # Event handlers
    def on_text_change(self, event=None):
        """Handle text change"""
        text = self.text_editor.get("1.0", tk.END)
        
        # Update stats
        word_count = len(text.split())
        char_count = len(text)
        self.stats_label.config(text=f"Words: {word_count} | Characters: {char_count}")
        
        # Detect characters
        project_service.update_project_content(text)
        new_chars = project_service.detect_characters_in_text(text)
        
        if new_chars:
            for char in new_chars:
                project_service.add_character(char)
            self.refresh_character_list()
    
    def on_chip_select(self, event=None):
        """Handle character chip select"""
        selection = self.character_chips.curselection()
        if selection:
            chars = project_service.get_characters()
            char = chars[selection[0]]
            self.show_character_details(char)
    
    def on_char_select(self, event=None):
        """Handle character list select"""
        selection = self.char_listbox.curselection()
        if selection:
            chars = project_service.get_characters()
            char = chars[selection[0]]
            self.show_character_details(char)
    
    def show_character_details(self, char):
        """Show character details"""
        self.char_name_entry.config(state=tk.NORMAL)
        self.char_role_entry.config(state=tk.NORMAL)
        self.char_desc_text.config(state=tk.NORMAL)
        self.char_goals_text.config(state=tk.NORMAL)
        self.save_char_btn.config(state=tk.NORMAL)
        
        self.char_name_var.set(char.name)
        self.char_role_var.set(char.role)
        self.char_desc_text.delete("1.0", tk.END)
        self.char_desc_text.insert("1.0", char.description)
        self.char_goals_text.delete("1.0", tk.END)
        self.char_goals_text.insert("1.0", ", ".join(char.goals))
        
        self.current_char = char
    
    def refresh_character_list(self):
        """Refresh character list"""
        self.char_listbox.delete(0, tk.END)
        characters = project_service.get_characters()
        for char in characters:
            display = f"{char.name} ({char.role})" if char.role else char.name
            self.char_listbox.insert(tk.END, display)
        
        # Update chips
        chip_names = [c.name for c in characters]
        self.chips_var.set(" ".join(chip_names))
    
    def refresh_locations_list(self):
        """Refresh locations list"""
        self.locations_listbox.delete(0, tk.END)
        locations = project_service.get_locations()
        for loc in locations:
            display = f"{loc.name} ({loc.type})" if loc.type else loc.name
            self.locations_listbox.insert(tk.END, display)
    
    def add_character(self):
        """Add new character"""
        char = Character(name="New Character")
        project_service.add_character(char)
        self.refresh_character_list()
    
    def edit_character(self):
        """Edit character"""
        selection = self.char_listbox.curselection()
        if selection:
            chars = project_service.get_characters()
            char = chars[selection[0]]
            self.show_character_details(char)
    
    def save_character(self):
        """Save character changes"""
        if hasattr(self, 'current_char'):
            self.current_char.name = self.char_name_var.get()
            self.current_char.role = self.char_role_var.get()
            self.current_char.description = self.char_desc_text.get("1.0", tk.END)
            self.current_char.goals = [g.strip() for g in self.char_goals_text.get("1.0", tk.END).split(",") if g.strip()]
            
            project_service.update_character(self.current_char)
            self.refresh_character_list()
            messagebox.showinfo("Success", "Character saved!")
    
    def delete_character(self):
        """Delete character"""
        selection = self.char_listbox.curselection()
        if selection:
            chars = project_service.get_characters()
            char = chars[selection[0]]
            if messagebox.askyesno("Confirm", f"Delete {char.name}?"):
                project_service.remove_character(char.id)
                self.refresh_character_list()
                self.cancel_edit()
    
    def cancel_edit(self):
        """Cancel character edit"""
        self.char_name_entry.config(state=tk.DISABLED)
        self.char_role_entry.config(state=tk.DISABLED)
        self.char_desc_text.config(state=tk.DISABLED)
        self.char_goals_text.config(state=tk.DISABLED)
        self.save_char_btn.config(state=tk.DISABLED)
        
        self.char_name_var.set("")
        self.char_role_var.set("")
        self.char_desc_text.delete("1.0", tk.END)
        self.char_goals_text.delete("1.0", tk.END)
    
    def add_location(self):
        """Add location"""
        loc = Location(name="New Location", type="Unknown")
        project_service.add_location(loc)
        self.refresh_locations_list()
    
    def save_project(self):
        """Save project"""
        project_service.current_project.title = self.title_var.get()
        project_service.update_project_content(self.text_editor.get("1.0", tk.END))
        
        if project_service.save_project():
            self.status_label.config(text="✓ Project saved", foreground="green")
            messagebox.showinfo("Success", "Project saved!")
        else:
            self.status_label.config(text="✗ Save failed", foreground="red")
            messagebox.showerror("Error", "Failed to save project")
    
    def open_project(self):
        """Open project"""
        messagebox.showinfo("Info", "Open functionality coming soon!")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = StoryProApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
