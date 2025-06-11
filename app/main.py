from fastapi import FastAPI, File, UploadFile, Query
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
    file: UploadFile = File(...),  # Image file to classify

    # parameters for the prediction
    habitat_classifications: str = Query("ukhab", regex="^(ukhab|eunis)$"),  # Type of habitat classification to perform
    top_n: int = Query(3, ge=1,le=3, description="Number of top predictions (1-5)"),  # Number of top predictions to return 

    # supplementary parameters
    latitude: Optional[float] = Query(None, ge=-90, le=90, description="Latitude between -90 and 90"),  # Latitude for geolocation
    longitude: Optional[float] = Query(None, ge=-180, le=180, description="Longitude between -180 and 180"),  # Longitude for geolocation
    species_list: Optional[str] = Query(None),  # Comma-separated list of species names for classification 

    # Other parameters for classification
    model_version: Optional[str] = Query("0.0.1"),  # Version of the model to use, if not supplied, defaults to the latest version

    # UK Habitat Classification parameters
    ukhab_predicted_level: int = Query(3, ge = 1, le =5),  # Level of the hierarchy to predict (1-5)
    ukhab_secondary_codes: Optional[bool] = Query(False)  # Include secondary level for UK habitat classification
    
    ):
    
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
