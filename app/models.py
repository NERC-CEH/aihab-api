from pydantic import BaseModel
from typing import List, Optional

# UKHabSecondaryCode model for the API response
class UKHabSecondaryCode(BaseModel):
    name: str
    code: str
    confidence: Optional[float]

# UKHabLevel model for the API response
class UKHabLevel(BaseModel):
    uk_hab_level: int #what level of the hierarchy this is
    code: str # the code for the habitat level e.g. "c1" (a level 3 code)
    name: str # the name for the habitat level e.g. "Arable and horticulture" (a level 3 code)
    confidence: Optional[float] # the confidence of the prediction for this level

# UKHab model for the API response
class UKHab(BaseModel):
    predicted_level: int # To what level the habitat prediction was requested (1-5)
    confidence: float # the overall confidence of the prediction
    rank: int # the rank of the habitat in the prediction (1-5)
    code: str #the overall code for the habitat eg. "r2a5"
    name: str # the overall name for the habitat e.g. "Rivers with floating vegetation"
    definition: str # the definition of the habitat
    primary_habitat_hierarchy: List[UKHabLevel] # Hierarchy of primary habitats
    secondary_codes: Optional[List[UKHabSecondaryCode]] = [] # Optional secondary codes for the habitat
    ukhab_version: str = "2.01"  # Placeholder for UKHab version

# HabitatPrediction model for the API response
class HabitatPrediction(BaseModel):
    ukhab: List[UKHab]  # List of UKHab predictions

# PredictionResponse model for the API response
class PredictionResponse(BaseModel):
    results: HabitatPrediction
    timestamp: str
    inference_time_ms: int
    model_version: str
    user_message: Optional[str] = None 