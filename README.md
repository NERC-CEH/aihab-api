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


## Hosting on Posit Connect

Install the python package `rsconnect` with `pip install rsconnect`.

Install a version of Python to match the version of python on Posit Connect (it needs to match or it won't work). If you change to an older version of Python to ensure compatability with the version on Posit Connect then you may need to downgrade the versions of the python packages in the `reqirements.txt` folder. You can then specify the path to the python version with -p.

```
rsconnect deploy fastapi -p C:\Users\simrol\AppData\Local\Programs\Python\Python39\python.exe -x "data/models/*" --entrypoint app.main:app ./
```

You will then need to add the environment variable using the Posit Connect web interface: https://docs.posit.co/connect/user/content-settings/#content-vars

The model will load on the first predict call.

You can then call the API with using the API key

```
curl -X 'GET' <api endpoint>/greetings' -H 'accept: application/json' -H "Authorization: Key ${CONNECT_API_KEY}"
 ``` 