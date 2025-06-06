import json
from pathlib import Path
json_path = Path(__file__).parent.parent / "Data" / "project_metadata.json"

def load_project_metadata(json_path):
      with open(json_path, "r") as f:
          return json.load(f)

def search_project_info(query, metadata):
    for project in metadata.get("projects", []):
        if query.lower() in project["name"].lower() or query.lower() in project["description"].lower():
            return project
    return None