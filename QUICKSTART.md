# 🚀 Quick Reference - Start Writing Now

## The Fastest Way to Get Started

### 1. Install & Run (2 commands)
```bash
pip install -r requirements.txt
python run.py
```

That's it! The app will open with your first blank project.

---

## What You Can Do Right Now

### ✍️ Write a Story
- Type in the Editor tab
- Watch character names auto-detect as you write
- See stats update in real-time

### 👥 Manage Characters
- Characters tab shows all detected/added characters
- Click any character to edit their details
- Add characters manually with the "Add Character" button
- Delete characters you don't need

### 🌍 Build Your World
- World Building tab has three sections:
  - **Locations**: Add places in your story
  - **Relationships**: See character/location connections
  - **Story Graph**: Visualization area (under development)

### 💾 Save Your Work
- Click the Save icon in the toolbar
- Your project is saved as a `.story` file
- All characters, locations, and content are preserved

---

## Example: Try This

1. Open the app with `python run.py`
2. Paste this story into the Editor:

```
Prince Charming rode into the kingdom to meet Snow White.
Snow White was waiting in the castle with her friends.
Magic Mirror had warned them about the Evil Queen.
When Prince Charming arrived, Snow White smiled.
But Magic Mirror whispered a secret to Prince Charming.
Evil Queen was plotting to destroy them all!
```

3. Watch as characters auto-detect: **Prince Charming**, **Snow White**, **Magic Mirror**, **Evil Queen**
4. Click on any character to edit their role and details
5. Switch to World Building and add locations
6. Click Save to preserve your project

---

## Key Features at a Glance

| Feature | Tab | How to Use |
|---------|-----|-----------|
| Write stories | Editor | Just start typing! |
| Auto-detect characters | Editor | Names appear as you write |
| Manage characters | Characters | Click to edit, Add to create new |
| Add locations | World Building | Click "Add Location" button |
| Save projects | Editor | Click Save icon |
| Edit project title | Editor | Click on title field |

---

## Keyboard Shortcuts (Available Soon)

- `Ctrl+S` - Save project (use button for now)
- `Ctrl+N` - New project (create new manually for now)
- `Ctrl+O` - Open project (coming soon)

---

## File Locations

- **Projects saved to**: `projects/` folder (auto-created)
- **Project format**: `.story` JSON files
- **Config files**: None needed - auto-created on first run

---

## Common Questions

**Q: How does character detection work?**
A: The app scans for capitalized names (like "Aragorn" or "Gandalf") and filters out common words (The, And, But, etc.). Names must be 3+ characters.

**Q: Can I delete characters?**
A: Yes! Go to Characters tab, select a character, and click the Delete button.

**Q: Where are my projects saved?**
A: In the `projects/` folder as `.story` JSON files.

**Q: Can I open old projects?**
A: Not yet, but it's in development. For now, keep your project open while working.

**Q: How detailed can character info be?**
A: You can set: Name, Role, Description, and multiple Goals (comma-separated).

**Q: Can I have multiple projects?**
A: Not simultaneously yet. Create a new project each time (coming soon).

---

## Troubleshooting

**App won't start:**
- Check Python: `python --version` (needs 3.8+)
- Install dependencies: `pip install -r requirements.txt`

**Characters not detecting:**
- Make sure names start with capitals (S**n**ow White, not snow white)
- Names need 3+ characters
- Avoid common words at the start

**Save not working:**
- Check folder permissions in your workspace
- The `projects/` folder is created automatically

---

## Ready?

```bash
python run.py
```

Start writing! Your story awaits. ✨📝

---

**Questions?** See `SETUP.md` for detailed documentation or check the docstrings in the code.
