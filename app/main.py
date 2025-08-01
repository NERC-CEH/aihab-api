from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from typing import Optional
from app.models import PredictionResponse
from app.predict import predict_habitat, load_model_hf, is_model_loaded
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model when the app starts
    load_model_hf()
    yield
    # Cleanup if needed when the app stops (e.g., unload model, close connections)
    # Currently, no cleanup is required for this simple example.
    pass

# AI-HAB Habitat Classification API
# This API provides endpoints for habitat classification using AI models.
app = FastAPI(
    title="AI-HAB Habitat Classification API",
    version="0.0.1",
    lifespan=lifespan
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
    if is_model_loaded():
        return {"status": "ok", "model": "loaded"}
    else:
        raise HTTPException(status_code=503, detail="Model not loaded")


# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(
    # image file to classify
    file: UploadFile = File(..., description="Image of habitat for classification"),  # Image file to classify

    # date and time of the image capture
    date_time: Optional[str] = Query(None, description="Date and time of the image capture in ISO 8601 format (e.g., '2023-10-01T12:00:00Z')"),
    sensor_type: Optional[str] = Query("app", description="Type of sensor used to capture the image (e.g., 'app', 'camera_trap')"),

    # parameters for the prediction
    habitat_classifications: str = Query("ukhab", regex="^(ukhab|eunis)$",description="Type of habitat classification to perform"), 
    top_n: int = Query(3, ge=1,le=3, description="Number of top predictions (1-3)"), 

    # supplementary parameters
    latitude: Optional[float] = Query(None, ge=-90, le=90, description="Latitude between -90 and 90"),
    longitude: Optional[float] = Query(None, ge=-180, le=180, description="Longitude between -180 and 180"),
    species_list: Optional[str] = Query(None, description="Comma-separated list of species names to aid classification (scientific names, underscore, species level, lower case e.g. 'quercus_robur,salix_alba')"), 

    # Other parameters for classification
    model_version: Optional[str] = Query(None,description="Version of the computer vision model to use, if not supplied, defaults to the latest version"), 

    # UK Habitat Classification parameters
    ukhab_predicted_level: int = Query(3, ge = 1, le =5, description="Level of the UK-Hab hierarchy to predict (1-5)"),
    ukhab_secondary_codes: Optional[bool] = Query(False, description="Whether to identify and return secondary codes for UK-Hab habitat classification"),  

    # gradcam
    gradcam: Optional[bool] = Query(False, description="Whether to return a Grad-CAM visualization of the model's attention on the image")   
    
    ):

    # raise an error if the file is not an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
    
    image_bytes = await file.read()
    result = predict_habitat(
        image_bytes,
        date_time,
        sensor_type,
        habitat_classifications,
        top_n,
        latitude,
        longitude,
        species_list,
        model_version,
        ukhab_predicted_level,
        ukhab_secondary_codes,
        gradcam)
    
    return result