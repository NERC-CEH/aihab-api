import time
import random
import string
from datetime import datetime
from typing import List, Optional

# Placeholder function to simulate habitat prediction
def predict_habitat_placeholder(
    image_bytes: bytes,
    habitat_classifications: str,
    top_n: int,
    latitude: Optional[float],
    longitude: Optional[float],
    species_list: Optional[str],
    model_version: str,
    ukhab_predicted_level: int,
    ukhab_secondary_codes: Optional[bool]
) -> dict:
    
    start_time = time.time()

    #validate inputs
    if habitat_classifications not in ["ukhab", "eunis"]:
        raise ValueError("Invalid habitat classification type. Must be 'ukhab' or 'eunis'.")
    
    #validate inputs
    if model_version not in ["0.0.1"]:
        raise ValueError("Model version not supported")
    

    # placeholder code
    def random_confidence():
        return round(random.uniform(0.5, 0.99), 2)


    def random_ukhab_classification():
        l1_codes = [
            {"code": "T", "name": "Terrestrial habitats"},
            {"code": "F", "name": "Freshwater habitats"},
            {"code": "M", "name": "Marine habitats"}
        ]
        l2_codes = [
            {"code": "g", "name": "Grassland"},
            {"code": "w", "name": "Woodland"},
            {"code": "a", "name": "Arable and horticulture"}
        ]
        l3_codes = [
            {"code": "g1", "name": "Acid grassland"},
            {"code": "g2", "name": "Calcareous grassland"},
            {"code": "g3", "name": "Neutral grassland"}
        ]
        l4_codes = [
            {"code": "g1a", "name": "Lowland dry acid grassland"},
            {"code": "g1b", "name": "Upland acid grassland"},
        ]
        l5_codes = [
            {"code": "g1a5", "name": "Inland dunes with open grasslands"},
            {"code": "g1a6", "name": "Oher lowland dry acid grassland"},
        ]

        #this is super verbose, but it is a placeholder for the actual logic that would be used to determine the habitat classification
        if ukhab_predicted_level == 1:
            overall_code = random.choice(l1_codes)["code"]
            overall_name = random.choice(l1_codes)["name"]
            hierarchy = [{
                "uk_hab_level": 1,
                "code": overall_code,
                "name": overall_name,
                "confidence": 1
            }]
        elif ukhab_predicted_level == 2:
            overall_code = random.choice(l2_codes)["code"]
            overall_name = random.choice(l2_codes)["name"]
            hierarchy = [{
                "uk_hab_level": 1,
                "code": "T",
                "name": "Terrestrial habitats",
                "confidence": 1
            },{
                "uk_hab_level": 2,
                "code": overall_code,
                "name": overall_name,
                "confidence": random_confidence()
            }]
        elif ukhab_predicted_level == 3:
            overall_code = random.choice(l3_codes)["code"]
            overall_name = random.choice(l3_codes)["name"]
            hierarchy = [
                {
                    "uk_hab_level": 1,
                    "code": "T",
                    "name": "Terrestrial habitats",
                    "confidence": 1
                },
                {
                    "uk_hab_level": 2,
                    "code": "G",
                    "name": "Grassland",
                    "confidence": random_confidence()
                },
                {
                    "uk_hab_level": 3,
                    "code": overall_code,
                    "name": overall_name,
                    "confidence": random_confidence()
                }
            ]
        elif ukhab_predicted_level == 4:
            overall_code = random.choice(l4_codes)["code"]
            overall_name = random.choice(l4_codes)["name"]
            hierarchy = [
                {
                    "uk_hab_level": 1,
                    "code": "T",
                    "name": "Terrestrial habitats",
                    "confidence": 1
                },
                {
                    "uk_hab_level": 2,
                    "code": "G",
                    "name": "Grassland",
                    "confidence": random_confidence()
                },
                {
                    "uk_hab_level": 3,
                    "code": "g1",
                    "name": "Acid grassland",
                    "confidence": random_confidence()
                },
                {
                    "uk_hab_level": 4,
                    "code": overall_code,
                    "name": overall_name,
                    "confidence": random_confidence()
                }
            ]
        elif ukhab_predicted_level == 5:
            overall_code = random.choice(l5_codes)["code"]
            overall_name = random.choice(l5_codes)["name"]
            hierarchy = [
                {
                    "uk_hab_level": 1,
                    "code": "T",
                    "name": "Terrestrial habitats",
                    "confidence": 1
                },
                {
                    "uk_hab_level": 2,
                    "code": "G",
                    "name": "Grassland",
                    "confidence": random_confidence()
                },
                {
                    "uk_hab_level": 3,
                    "code": "g1",
                    "name": "Acid grassland",
                    "confidence": random_confidence()
                },
                {
                    "uk_hab_level": 4,
                    "code": "g1a",
                    "name": "Lowland dry acid grassland",
                    "confidence": random_confidence()
                },
                {
                    "uk_hab_level": 5,
                    "code": overall_code,
                    "name": overall_name,
                    "confidence": random_confidence()
                }
            ]
    
    
        secondary_codes = [
            {"name": "Mid-field swale", "code": "606", "confidence": random_confidence()},
            {"name": "Beetle bank", "code": "607", "confidence": random_confidence()},
            {"name": "Underfield drainage", "code": "608", "confidence": random_confidence()}
        ]

        
        if ukhab_secondary_codes:
            secondary_codes = random.sample(secondary_codes, k=random.randint(0, 3))
        else:
            secondary_codes = []

        habitat = {
            "predicted_level": ukhab_predicted_level,
            "confidence": random_confidence(), 
            "code": overall_code,
            "name": overall_name,
            "definition": "Habitat definition placeholder text.",
            "primary_habitat_hierarchy": hierarchy,
            "secondary_codes": secondary_codes,
            "ukhab_version": "2.01"
        }

        return habitat
    
    # Simulate a delay for processing
    time.sleep(random.uniform(0.1, 0.5))  # Simulate processing time

    #use random_ukhab_classification to generate a random habitat classification based on top_n
    # Generate placeholder predictions
    habitats = [random_ukhab_classification() for _ in range(top_n)]

    # Sort by confidence (descending)
    habitats.sort(key=lambda x: x["confidence"], reverse=True)
    # Add rank field (1-based index)
    for idx, h in enumerate(habitats, start=1):
        h["rank"] = idx

    #generate response
    response = {
        "results": {
            "ukhab": habitats
        },
        "timestamp": datetime.now().isoformat(),
        "inference_time_ms": int((time.time() - start_time) * 1000),
        "model_version": model_version,
        "user_message": "This is a placeholder prediction. Results are randomly generated."
    }

    return response