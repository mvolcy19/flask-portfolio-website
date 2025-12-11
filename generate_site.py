from flask import Flask, render_template
import json
import os
import shutil
from urllib.parse import quote

app = Flask(__name__, template_folder="templates")


# Base directory of this script (makes paths work regardless of CWD)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_projects():
    """Load projects from data/projects.json and return a list of projects.

    Returns an empty list if the file is missing or malformed.
    """
    data_file = os.path.join(BASE_DIR, "data", "projects.json")

    if not os.path.exists(data_file):
        print(f"Warning: {data_file} not found. Returning empty projects list.")
        return []

    with open(data_file, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except Exception as e:
            print(f"Error loading {data_file}: {e}")
            return []

        # Support two structures:
        # 1) { "projects": [ ... ] }
        # 2) { "Category Name": [ ... ], ... }  -> flatten all lists
        if isinstance(data, dict):
            if "projects" in data:
                return data.get("projects", [])
            # Flatten any top-level lists (useful when JSON groups by category)
            flattened = []
            for k, v in data.items():
                if isinstance(v, list):
                    flattened.extend(v)
            if flattened:
                print(f"Detected category-grouped JSON; flattened {len(flattened)} projects.")
                return flattened
        # If it's a list already, return it
        if isinstance(data, list):
            return data

        return []


def generate_static_site():
    projects = load_projects()

    output_dir = os.path.join(BASE_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Copy images folder if present (check common casings)
    for images_folder in ("images", "Images"):
        src = os.path.join(BASE_DIR, images_folder)
        if os.path.exists(src):
            output_images = os.path.join(output_dir, "images")
            if os.path.exists(output_images):
                shutil.rmtree(output_images)
            shutil.copytree(src, output_images)
            print(f"Copied {src} -> {output_images}")
            break

    # Render index page with the projects list (template expects `projects`)
    with app.app_context():
        index_html = render_template("index.html", projects=projects)
        with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as file:
            file.write(index_html)
        print("Generated index.html")

    # Render each project detail page. Templates link to project-<id>.html
    for project in projects:
        # Prepare embed-friendly URLs for supported providers
        # Figma share URLs need to be wrapped for embedding: https://www.figma.com/embed?embed_host=share&url=<url-encoded-share-url>
        if project.get("figma_prototype"):
            url = project.get("figma_prototype")
            if "figma.com" in url and "embed" not in url:
                project["figma_embed"] = f"https://www.figma.com/embed?embed_host=share&url={quote(url, safe='')}"
            else:
                project["figma_embed"] = url
        with app.app_context():
            project_html = render_template("project.html", project=project)
            filename = f"project-{project['id']}.html"
            with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as file:
                file.write(project_html)
        print(f"Generated {filename}")

    # Render contact page
    with app.app_context():
        contact_html = render_template("contact.html")
        with open(os.path.join(output_dir, "contact.html"), "w", encoding="utf-8") as file:
            file.write(contact_html)
        print("Generated contact.html")

    print(f"\n🎉 Site generated! Open {output_dir}/index.html in your browser.")


if __name__ == "__main__":
    generate_static_site()