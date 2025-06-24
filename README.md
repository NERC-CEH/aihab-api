# AI-HAB Habitat Classification API

This project provides a FastAPI-based web API for habitat classification using AI models. The API allows users to upload images and receive habitat predictions based on different classification schemes.

## Features

- Upload an image and receive habitat classification predictions.
- Supports UKHab and EUNIS classification schemes.
- Optional geolocation and species list parameters.
- Configurable prediction depth and secondary codes for UKHab.

## API Endpoints

### `GET /`
Returns API information.

### `GET /status`
Returns API status.

### `POST /predict`
Accepts an image and parameters, returns habitat predictions.

#### Request Parameters

API endoints and their status in development.

- `file`: Image file to classify (required) ✅
- `date_time`: Date and time of the image capture ❌ (Not implemented in model or API)
- `sensor_type`: Type of sensor used to capture the image (e.g., 'app', 'camera_trap') ❌ (Not implemented in model or API)
- `habitat_classifications`: `"ukhab"` or `"eunis"` (default: `"ukhab"`) ✅ (only UK-Hab supported)
- `top_n`: Number of top predictions to return (1-5, default: 3) ✅
- `latitude`: Latitude for geolocation (optional) ❌ (Not implemented in model or API)
- `longitude`: Longitude for geolocation (optional) ❌ (Not implemented in model or API)
- `species_list`: Comma-separated species names (optional) ❌ (Not implemented in model or API)
- `model_version`: Model version (optional) ❌ (Not implemented in API)
- `ukhab_predicted_level`: UKHab hierarchy level (1-5, default: 3) ❌ (Not implemented in model or API, predicts to level 3 irrespective of given value)
- `ukhab_secondary_codes`: Include secondary codes (default: `False`) ❌ (Not implemented in model or API, returns empty)

For more details run the app and nagivate to `/docs` to read the swagger documentation (https://fastapi.tiangolo.com/reference/openapi/docs/)

## Getting Started

1. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # Or, on macOS/Linux:
   # source venv/bin/activate
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Get the model from HuggingFace:**

   Generate a Hugging face token: https://huggingface.co/docs/hub/en/security-tokens (Fine-grained tokens are more secure).
   
   Create a `.env` file like the following:
   
   ```
   HF_AUTH_TOKEN = hf_yourtokenhere
   ```

3. **Run the API:**
   ```sh
   uvicorn app.main:app --reload
   ```

4. **Access the docs:**
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.
