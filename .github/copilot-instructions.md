# Copilot Instructions for Portfolio Site Generator

## Project Overview
A static portfolio website generator built with Python (Flask) that converts project data (JSON) into a fully-rendered static HTML site. The architecture follows a data-driven approach: JSON → Python processing → Jinja2 templates → Static HTML output.

## Architecture & Data Flow

**Three-Layer Design:**
1. **Data Layer** (`data/projects.json`) - Stores all project metadata with fields: `id`, `title`, `category`, `description`, `technologies`, optional fields like `github_url`, `live_url`, `image`, `figma_prototype`
2. **Processing Layer** - Two distinct workflows:
   - **Static Generation** (`generate_site.py`): Flask app context renders templates → writes HTML files to `/output/` directory
   - **Admin Management** (`admin.py`): CLI interface for CRUD operations on projects
3. **Presentation Layer** (`templates/`) - Jinja2 templates extending `base.html`

**Key Data Pattern:** Projects are loaded from JSON, processed with Flask's template engine in-app-context (even for static generation), then written to disk.

## Critical Implementation Notes

### File Naming Inconsistencies (Watch Out!)
- `main.py` and `admin.py` load from `"data/projects.json"`
- **BUT** `generate_site.py` loads from `"data/project.json"` (missing 's') - This is a bug!
- When modifying data loading, ensure consistency across all three files

### Static Site Generation Process
```
generate_site.py → load_project() → generate_static_site():
  1. Create /output/ directory
  2. Copy /images/ folder → /output/images/
  3. Render index.html (passes all projects)
  4. Render project_{id}.html for each project individually
  5. Render contact.html
```
Templates receive individual project objects (not arrays) except for index.html.

### Admin Panel (`admin.py`)
- Interactive CLI with partial implementation (edit/delete/search stubs exist but aren't wired)
- ID auto-increment logic: `max([p.get("id", 0) for p in projects], default=0) + 1`
- Automatically creates `/data/` directory if missing
- User-input driven; optional fields conditionally added to JSON

## Template Structure & Conventions

**Jinja2 Inheritance:** All pages extend `base.html` (Didot serif font, purple gradient nav)
- `base.html` defines layout, styles, nav, and `{% block content %}` insertion point
- `index.html`: Homepage with about section, projects grid, games, blog, gallery, social links
- `project.html`: Individual project detail page (expects single `project` object)
- `contact.html`: Contact/social links page

**Template Variables:**
- Index: `project` (list of all projects) - Note: variable named singular despite being plural data
- Project detail: `project` (single project object)

## Key Conventions & Patterns

1. **JSON Project Schema:** Always validate new fields match existing structure (id, title, category, description, technologies as array, optional URLs/images)
2. **Encoding:** All file operations use `encoding="utf-8"` with `ensure_ascii=False` in json.dump
3. **Path Handling:** Uses `os.path.join()` consistently; relative paths from project root
4. **Error Handling:** Currently minimal - no validation on add_project input or JSON integrity checks

## Common Tasks

**Add a new project field:**
1. Update schema in `data/projects.json` example
2. Modify `admin.py` add_project() input section
3. Update relevant template block in `project.html` to display field
4. Test via `generate_site.py`

**Debug site generation:**
- Run `python generate_site.py` - checks if `/data/project.json` exists (note: singular!)
- Verify `/output/` directory created and contains HTML files
- Check `/output/images/` copied correctly

**Add filtering/search:**
- MVP Phase 2 planned feature - would filter in `generate_site.py` before template rendering
- Store filter state in projects or create separate index structures

## Known Issues & TODOs
- Filename inconsistency: `generate_site.py` loads from `"data/project.json"` instead of `"data/projects.json"`
- `admin.py` has incomplete functions: `edit_project()`, `delete_project()`, `search_projects()` (stubs only)
- `admin.py` menu incomplete: Input handlers not wired for options 1-3
- No validation on project input (empty fields, invalid URLs, etc.)
- Hard-coded image path in index.html needs to be templated
- Missing image path references in generated HTML

## Development Workflow
1. **Modify projects:** Use `admin.py` (or edit `data/projects.json` directly)
2. **Test locally:** Run `python generate_site.py` to regenerate `/output/`
3. **View site:** Open `/output/index.html` in browser
4. **Check data:** `python main.py` loads and prints project count/titles

## Dependencies
- Flask (for Jinja2 template rendering)
- Python 3.8+ (f-strings, dict methods)
- Standard library only: `json`, `os`, `shutil`
