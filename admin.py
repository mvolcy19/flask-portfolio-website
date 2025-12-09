import json 
import os 

def load_projects():
    data_file  = os.path.join("data", "projects.json")

    if not os.path.exists(data_file):
        return []
    
    with open(data_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get("projects", [])
    
def save_projects(projects):
    data_file = os.path.join("data", "projects.json")
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump({"projects": projects}, file, indent=2, ensure_ascii=False)
    print("Project saved!")

def find_project_by_id(projects, project_id):
    """Find a project by its ID."""
    for project in projects:
        if project.get ("id") == project_id:
            return project 
    return None

def add_project():
    print("\n===Add a New Project===")
    title = input("Project Title: ").strip()
    category = input("Category (web development/games/design):").strip().lower()
    description = input("Description: ").strip()
    link = input("Project Link (URL): ").strip()

    techs_input = input("Technologies (comma-separated, e.g., Python, HTML, CSS): ").strip()
    technologies = [t.strip() for t in techs_input.split(",") if t.strip()]

    image = input("Image path (e.g., images/projects/my-project.png) [optional]: ").strip()
    github_url = input("GitHub URL (optional): ").strip() or None 
    live_url = input("Live site URL (optional): ").strip() or None
    figma_prototype = input("Figma Prototype URL (optional): ").strip() or None

    projects = load_projects()

    #find next ID
    next_id = max([p.get("id", 0) for p in projects], default=0) + 1

    #Create neew project
    new_project = {
        "id": next_id,
        "title": title,
        "category": category,
        "description": description,
        "link": link,
        "technologies": technologies,
    }

    #add option fields if provided 
    if image:
        new_project["image"] = image
    if github_url:
        new_project["github_url"] = github_url
    if live_url:
        new_project["live_url"] = live_url
    if figma_prototype:
        new_project["figma_prototype"] = figma_prototype

    #add to list and save 
    projects.append(new_project)
    save_projects(projects)

    print(f"\n Added project: {title} (ID: {next_id})\n")

def list_projects():
    """List all projects in the data file."""
    projects = load_projects()
    if not projects:
        print("\nNo projects found.\n")
        return

    print("\n=== Project List ===")
    for project in projects:
        print(f"\nID: {project['id']}")
        print(f"  Title: {project['title']}")
        print(f"  Category: {project.get('category', 'N/A')}")
        print(f"  Description: {project.get('description', 'N/A')[:50]}...")

#def edit_project():

#def delete_project():

#def search_projects():

def main():
    """Main admin menu"""
    while True:
        print("\n=== Portfolio Admin Panel ===")
        print("1. List Projects")
        print("2. Add New Project")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            list_projects()
        elif choice == "2":
            add_project()
        elif choice == "3":
            print("Exiting admin tool, Goodbye.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

