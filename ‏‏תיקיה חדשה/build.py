import os

# מבנה התיקיות והקבצים שצריך ליצור
structure = {
    "ZeKal": {
        "_config.yml": "",
        "_includes": {
            "header.html": "",
            "footer.html": ""
        },
        "_layouts": {
            "default.html": ""
        },
        "assets": {
            "css": {
                "style.css": ""
            },
            "js": {
                "script.js": ""
            }
        },
        "topics": {
            "programming-languages.md": "",
            "web-development.md": "",
            "networking.md": "",
            "cybersecurity.md": "",
            "databases.md": "",
            "cloud-computing.md": "",
            "artificial-intelligence.md": "",
            "hardware-components.md": "",
            "software-development-methodologies.md": "",
            "operating-systems.md": ""
        },
        "index.md": "",
        "README.md": ""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)  # Recursion to create inner folders and files
        else:
            with open(path, 'w') as f:
                f.write(content)

# צור את המבנה
base_path = "ZeKal"
create_structure(base_path, structure)

print(f"Folder structure created at {os.path.abspath(base_path)}")
