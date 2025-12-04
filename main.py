import json
import os 

def load_projects():
    data_file = os.path.join("data", "projects.json")

    if not os.path.exists(data_file):
        print(f"Warning: {data_file} not found. Creating empty projects list.")
        return []
    
    with open(data_file, "r", encoding="utf=8") as file:
        data = json.load(file) 
        return data.get("projects", [])

def main():
   projects = load_projects()
   print(f"Loaded{len(projects)} projects.")

   for project in projects: 
       print(f"- {project['title']},({project['category']})")

if __name__ == "__main__":
    main()