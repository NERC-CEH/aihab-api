import json

def get_habitat_metadata(habitat_code):
    """
    Load habitat metadata from a JSON file.
    
    Returns:
        dict: Parsed JSON data containing habitat metadata.
    """
    try:
        with open("data/ukhab.json", "r") as file:
            metadata = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Habitat metadata file not found.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding habitat metadata JSON file.")

    #ukhab level as the number of characters in the habitat code minus 1
    ukhab_level= len(habitat_code)+1

    # level override if habitat code is "sea" or "montane" (non-standard codes)
    if habitat_code == "sea" or habitat_code == "montane":
        primary_habitat_hierarchy = {
                "uk_hab_level": 1,
                "code": habitat_code,
                "name": metadata[habitat_code]["name"],
                "definition": ""
        }
        return primary_habitat_hierarchy

    # get full habitat hierarchy
    primary_habitat_hierarchy = []

    for i in range(1, ukhab_level, 1):
        code_i = habitat_code[:i]
        habitat_i = metadata[code_i]
        primary_habitat_hierarchy.append(
            {
                "uk_hab_level": i+1,
                "code": code_i,
                "name": habitat_i["name"],
                "definition": habitat_i["definition"],
            }
        )

    return primary_habitat_hierarchy
    

