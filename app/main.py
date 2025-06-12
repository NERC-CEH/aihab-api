from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from typing import Optional
from app.models import PredictionResponse
from app.predict import predict_habitat_placeholder

# AI-HAB Habitat Classification API
# This API provides endpoints for habitat classification using AI models.
app = FastAPI(
    title="AI-HAB Habitat Classification API",
    version="0.0.1"
)

# Base url endpoint
@app.get("/")
async def info():
    return {
        "name": "AI-HAB Habitat Classification API",
        "version": "0.0.1",
        "description": "This API provides endpoints for habitat classification using AI models."
    }

#status endpoint
@app.get("/status")
async def status():
    return {"status": "ok"}


# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(
    # image file to classify
    file: UploadFile = File(..., description="Image of habitat for classification"),  # Image file to classify

    # parameters for the prediction
    habitat_classifications: str = Query("ukhab", regex="^(ukhab|eunis)$",description="Type of habitat classification to perform"), 
    top_n: int = Query(3, ge=1,le=3, description="Number of top predictions (1-3)"), 

    # supplementary parameters
    latitude: Optional[float] = Query(None, ge=-90, le=90, description="Latitude between -90 and 90"),
    longitude: Optional[float] = Query(None, ge=-180, le=180, description="Longitude between -180 and 180"),
    species_list: Optional[str] = Query(None, description="Comma-separated list of species names to aid classification"), 

    # Other parameters for classification
    model_version: Optional[str] = Query("0.0.1",description="Version of the computer vision model to use, if not supplied, defaults to the latest version"),  # Version of the model to use, if not supplied, defaults to the latest version

    # UK Habitat Classification parameters
    ukhab_predicted_level: int = Query(3, ge = 1, le =5, description="Level of the UK-Hab hierarchy to predict (1-5)"),
    ukhab_secondary_codes: Optional[bool] = Query(False, description="Whether to identify and return secondary codes for UK-Hab habitat classification")   
    
    ):

    # raise an error if the file is not an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
    
    image_bytes = await file.read()
    result = predict_habitat_placeholder(
        image_bytes,
        habitat_classifications,
        top_n,
        latitude,
        longitude,
        species_list,
        model_version,
        ukhab_predicted_level,
        ukhab_secondary_codes)
    
    return result
