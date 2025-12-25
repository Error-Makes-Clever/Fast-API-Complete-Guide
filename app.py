from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
from pydantic import BaseModel, Field, computed_field
import pickle
import pandas as pd

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class UserInput(BaseModel):

    age : Annotated[int, Field(..., description="Age of the user", gt=0, lt=120)]
    weight : Annotated[float, Field(..., description="Weight of the user", gt=0)]
    height : Annotated[float, Field(..., description="Height of the user", gt=0, lt=2.5)]
    income_lpa : Annotated[float, Field(...,description="Income of the user")]
    smoker : Annotated[bool, Field(..., description="Smoker of the user")]
    city : Annotated[str, Field(..., description="City of the user")]
    occupation : Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="Occupation of the user")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height * self.height), 2)
    
    @computed_field 
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def city_tier(self) -> str:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(user_input: UserInput):
    
    input_df = pd.DataFrame([{
        'bmi' : user_input.bmi,
        'age_group' : user_input.age_group,
        'lifestyle_risk' : user_input.lifestyle_risk,
        'city_tier' : user_input.city_tier,
        'income_lpa' : user_input.income_lpa,
        'occupation' : user_input.occupation
    }])

    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code= 200, content={"predicted_category": prediction})