import time
from datetime import datetime
from typing import List, Optional
from torchvision.transforms import v2
import torch
import torch.nn.functional as F  # Add this import for F.softmax
import os
from huggingface_hub import login
import timm
from PIL import Image
import io
from app.get_info import get_habitat_metadata
from dotenv import load_dotenv
from app.produce_gradcam_image import produce_gradcam


# Load environment variables from .env file
load_dotenv()

model = None
device = torch.device("cpu")

def load_model_hf():    
    token = os.getenv("HF_AUTH_TOKEN", None)
    model_name = "hf_hub:whitegivefive/aihab-supcon-swint-v0"     
    global model
    if model is None:
        try:
            login(token)
            # Now create the model without explicitly passing the token.
            model = timm.create_model(model_name, pretrained=True,cache_dir = "data/models")
            model.to(device)
            model.eval()
            return "Logged in successfully and model loaded."
        except Exception as e:
            return f"Error loading model: {str(e)}"
        
def is_model_loaded() -> bool:
    return model is not None

# Define preprocessing pipeline for images
transform = v2.Compose([
    v2.Resize((384, 384)),
    v2.ToTensor(),
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

#predict habitat
def predict_habitat(
    image_bytes: bytes,
    date_time: Optional[str],
    sensor_type: Optional[str],
    habitat_classifications: str,
    top_n: int,
    latitude: Optional[float],
    longitude: Optional[float],
    species_list: Optional[str],
    model_version: Optional[str],
    ukhab_predicted_level: int,
    ukhab_secondary_codes: Optional[bool],
    gradcam: Optional[bool] = False
) -> dict:
    
    start_time = time.time()

    #validate inputs
    if habitat_classifications not in ["ukhab", "eunis"]:
        raise ValueError("Invalid habitat classification type. Must be 'ukhab' or 'eunis'.")
    
    if habitat_classifications not in ["ukhab"]:
        raise ValueError("UK-Hab is the only habitat classification supported by AI-Hab currently. Parameter 'habitat_classifications' must be 'ukhab'.")
    
    load_model_hf()

    global model
    if model is None:
        raise  RuntimeError("Model is not loaded")
    model_version = "default"

    # conversion from internal model label (numeric) to UKHab label (string)    
    labels = {
        'u1': 0, #'Urban'
        'w1': 1, # 'Broadleaved Mixed and Yew Woodland'
        'w2': 2, # 'Coniferous Woodland'
        'sea': 3, # Sea
        'c1': 4,#  Arable and Horticulture
        'g4': 5,# Improved Grassland
        'g3': 6, # Neutral Grassland
        'g2': 7, #  Calcareous Grassland
        'g1': 8, # Acid Grassland
        'g1c': 9, # Bracken
        'h1': 10, # Dwarf Shrub Heath
        'f2': 11, # Fen, Marsh, Swamp
        'f1': 12, # Bog
        't1': 13, # Littoral Rock
        't2': 14, # Littoral Sediment
        'montane': 15, #Montane
        'r1': 16, # Standing Open Waters and Canals
        's1': 17, # Inland Rock
        's2': 18, # Supra-littoral Rock
        's3': 19 # Supra-littoral Sediment
    }

    # make model prediction
    # Preprocess the image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        output = model(image)

    # Compute probabilities using softmax
    probabilities = F.softmax(output, dim=1)
    # Get the top 3 predictions
    top_probs, top_indices = torch.topk(probabilities, k=top_n, dim=1)

    # Squeeze the batch dimension and convert to Python lists
    top_probs = top_probs.squeeze(0).tolist()
    top_indices = top_indices.squeeze(0).tolist()
    # Convert indices to UKHab labels
    top_labels = [list(labels.keys())[index] for index in top_indices]



    if gradcam:
        cam_base64 = produce_gradcam(
            model=model,
            image=image,
        )

    # Create a list of habitat predictions
    habitats = []

    for i in range(top_n):
        overall_code = top_labels[i]

        # Get habitat metadata
        hierarchy = get_habitat_metadata(overall_code)
        overall_name = hierarchy[-1]["name"]
        prob = top_probs[i]

        habitat = {
            "predicted_level": ukhab_predicted_level,
            "confidence":  prob, # Confidence score for the prediction 
            "code": overall_code,
            "name": overall_name,
            "definition": hierarchy[-1]["definition"],
            "primary_habitat_hierarchy": hierarchy,
            "secondary_codes": [],
            "ukhab_version": "2.01"
        }

        habitats.append(habitat)

    # Sort by confidence (descending)
    habitats.sort(key=lambda x: x["confidence"], reverse=True)
    # Add rank field (1-based index)
    for idx, h in enumerate(habitats, start=1):
        h["rank"] = idx

    #--------------------
    request_metadata = {
        "habitat_classifications": habitat_classifications,
        "date_time": date_time,
        "sensor_type": sensor_type,
        "top_n": top_n,
        "latitude": latitude,
        "longitude": longitude,
        "species_list": species_list,
        "model_version": model_version,
        "ukhab_predicted_level": ukhab_predicted_level,
        "ukhab_secondary_codes": ukhab_secondary_codes
    }

    #generate response
    response = {
        "results": {
            "ukhab": habitats
        },
        "timestamp": datetime.now().isoformat(),
        "inference_time_ms": int((time.time() - start_time) * 1000),
        "model_version": model_version,
        "user_message": "In development, use with caution.",
        "gradcam_image": cam_base64 if gradcam else None,
        "request_metadata": request_metadata
    }

    return response