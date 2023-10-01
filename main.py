import os
import yaml
import json

# Define the folder containing YAML files and the path to the JSON file
yaml_folder = '/Users/sagar/Documents/DO/Projects/attackMapper/rules/'
json_file_path = '/Users/sagar/Documents/DO/Projects/attackMapper/attackLayer/v4heatmap_layer.json'

# Function to update JSON based on a YAML file
def update_json_from_yaml(yaml_file_path, json_data):
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
    
    tag = yaml_data.get('tags', [])
    technique_id = tag[0]['techniqueID']
    score = tag[1]['score']
    name = yaml_data.get('title')
    description = yaml_data.get('description')
    json_data['techniques'].append(
        {
            'techniqueID': technique_id,
            'score': score,
            'metadata': [
                {
                    'name': list(yaml_data.items())[0][0],
                    'value': list(yaml_data.items())[0][1]
                },
                {
                    'name': list(yaml_data.items())[3][0],
                    'value': list(yaml_data.items())[3][1]
                }
            ]
        }
    )

# Load or create JSON data if it doesn't exist
if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
else:
    json_data = {
        "name": "heatmap V4",
        "versions": {
            "attack": "13",
            "navigator": "4.8.2",
            "layer": "4.4"
        },
        "domain": "enterprise-attack",
        "description": "An example layer where all techniques have a randomized score",
        "filters": {
            "platforms": [
                "Linux",
                "macOS",
                "Windows",
                "Network",
                "PRE",
                "Containers",
                "Office 365",
                "SaaS",
                "Google Workspace",
                "IaaS",
                "Azure AD"
            ]
        },
        "sorting": 3,
        "layout": {
            "layout": "side",
            "aggregateFunction": "average",
            "showID": False,
            "showName": True,
            "showAggregateScores": False,
            "countUnscored": False
        },
        "hideDisabled": False,
        "gradient": {
            "colors": [
                "#ff6666ff",
                "#ffe766ff",
                "#8ec843ff"
            ],
            "minValue": 0,
            "maxValue": 10
        },
        "legendItems": [],
        "metadata": [],
        "links": [],
        "showTacticRowBackground": False,
        "tacticRowBackground": "#dddddd",
        "selectTechniquesAcrossTactics": False,
        "selectSubtechniquesWithParent": False,
        "techniques": []
    }

# Iterate through YAML files in the folder and update JSON
for yaml_filename in os.listdir(yaml_folder):
    if yaml_filename.endswith('.yml'):
        yaml_file_path = os.path.join(yaml_folder, yaml_filename)
        try:
            update_json_from_yaml(yaml_file_path, json_data)
        except Exception as e:
            print(f"Error processing {yaml_file_path}: {str(e)}")

# Write the updated JSON back to the file
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=2)

print("Heatmap updated successfully.")
