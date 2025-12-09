from flask import Flask, render_template
import json 
import os
import shutil 

app = Flask(__name__, template_folder="templates")

def load_project():
    data_file = os.path.join("data", "project.json")

    if not os.path.exists(data_file):
        return []
    
    with open(data_file, "r", encoding= "utf-8") as file:
        data = json.load(file)
        return data.get("project", [])
    
def generate_static_site():
    project = load_project()

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists("images"):
        output_images = os.path.join(output_dir, "images")
        if os.path.exists(output_images):
            shutil.rmtree(output_images)
        shutil.copytree("images", output_images)
        print(f"Copied images folder")

    with app.app_context():
        index_html = render_template("index.html", project=project)
        with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as file:
            file.write(index_html)
        print("Generated index.html")

    for project in project:
        with app.app_context():
            project_html = render_template("project.html", project=project)
            filename = f"project_{project['id']}.html"
            with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as file:
                file.write(project_html)
        print(f"Generated {filename}")

    print(f"\n🎉 Site generated! Open output/index.html in your browser.")

    with app.app_context():
        contact_html = render_template("contact.html")
        with open(os.path.join(output_dir, "contact.html"), "w", encoding="utf-8") as file:
            file.write(contact_html)
        print("Generated contact.html")


if __name__ == "__main__":
    generate_static_site()