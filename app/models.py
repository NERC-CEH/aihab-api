from pydantic import BaseModel, Field
from typing import List, Optional

class UKHabSecondaryCode(BaseModel):
    name: str = Field(..., description="The name of the secondary habitat code")
    code: str = Field(..., description="The UKHab code for the secondary habitat")
    confidence: Optional[float] = Field(None, description="Confidence score for the secondary habitat prediction (0-1)")

class UKHabLevel(BaseModel):
    uk_hab_level: int = Field(..., description="The hierarchical level of this habitat (1 to 5)")
    code: str = Field(..., description="The UKHab code corresponding to this habitat level, e.g., 'c1'")
    name: str = Field(..., description="The descriptive name of the habitat level, e.g., 'Arable and horticulture'")
    confidence: Optional[float] = Field(None, description="Confidence score for this habitat level prediction (0-1)")

class UKHab(BaseModel):
    predicted_level: int = Field(..., description="The requested or predicted habitat level (1 to 5)")
    confidence: float = Field(..., description="Overall confidence score for this habitat prediction (0-1)")
    rank: int = Field(..., description="The rank of this prediction among top habitat predictions (1 being highest)")
    code: str = Field(..., description="The UKHab code representing the full habitat classification, e.g., 'r2a5'")
    name: str = Field(..., description="The full name of the predicted habitat, e.g., 'Rivers with floating vegetation'")
    definition: str = Field(..., description="The definition or description of the predicted habitat")
    primary_habitat_hierarchy: List[UKHabLevel] = Field(..., description="The hierarchical breakdown of the primary habitat classification")
    secondary_codes: Optional[List[UKHabSecondaryCode]] = Field(default_factory=list, description="Optional list of secondary habitat codes, if applicable")
    ukhab_version: str = Field("2.01", description="The version of the UKHab classification system used")

class HabitatPrediction(BaseModel):
    ukhab: List[UKHab] = Field(..., description="List of top-ranked UKHab habitat predictions")

class PredictionResponse(BaseModel):
    results: HabitatPrediction = Field(..., description="Container for the habitat prediction results")
    timestamp: str = Field(..., description="Timestamp of when the prediction was generated")
    inference_time_ms: int = Field(..., description="Time taken (in milliseconds) to generate the prediction")
    model_version: str = Field(..., description="Version of the machine learning model used for prediction")
    user_message: Optional[str] = Field(None, description="Optional message to the user, e.g., warnings or notes")
    request_metadata: dict = Field(..., description="Metadata about the prediction request, including parameters used")