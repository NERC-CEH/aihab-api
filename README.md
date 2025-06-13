# AI-HAB Habitat Classification API

This project provides a FastAPI-based web API for habitat classification using AI models. The API allows users to upload images and receive habitat predictions based on different classification schemes.

## Features

- Upload an image and receive habitat classification predictions.
- Supports UKHab and EUNIS classification schemes.
- Optional geolocation and species list parameters.
- Configurable prediction depth and secondary codes for UKHab.

## Project Structure

```
app/
  main.py         # FastAPI application and endpoints
  models.py       # Pydantic models for API responses
  predict.py      # Placeholder prediction logic
model/
tests/
.gitignore
```

## API Endpoints

### `GET /`
Returns API information.

### `GET /status`
Returns API status.

### `POST /predict`
Accepts an image and parameters, returns habitat predictions.

#### Request Parameters

- `file`: Image file to classify (required)
- `habitat_classifications`: `"ukhab"` or `"eunis"` (default: `"ukhab"`)
- `top_n`: Number of top predictions to return (1-3, default: 3)
- `latitude`: Latitude for geolocation (optional)
- `longitude`: Longitude for geolocation (optional)
- `species_list`: Comma-separated species names (optional)
- `model_version`: Model version (default: `"0.0.1"`)
- `ukhab_predicted_level`: UKHab hierarchy level (1-5, default: 3)
- `ukhab_secondary_codes`: Include secondary codes (default: `False`)

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

3. **Run the API:**
   ```sh
   uvicorn app.main:app --reload
   ```

4. **Access the docs:**
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## Notes

- The current prediction logic is a placeholder and returns randomly generated results.
- See [`app/main.py`](app/main.py), [`app/models.py`](app/models.py), and [`app/predict.py`](app/predict.py) for implementation details.