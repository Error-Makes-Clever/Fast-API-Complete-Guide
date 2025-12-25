from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json 

app = FastAPI()

def load_data():    
    with open("patience.json", "r") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patience.json", "w") as f:
        json.dump(data, f)

class Patient(BaseModel):
    
    id : Annotated[str, Path(..., description= "The ID of the patient in DB", example = 'P001')]
    name : Annotated[str, Field(..., description= "The name of the patient", example = 'John Doe')] 
    city : Annotated[str, Field(..., description= "The city of the patient", example = 'New York')]
    age : Annotated[int, Field(..., description= "The age of the patient", example = 30)]
    gender : Annotated[Literal['Male', 'Female', 'Other'], Field(..., description= "The gender of the patient", example = 'Male')]
    height : Annotated[float, Field(..., description= "The height of the patient (in meters)", example = 1.75)]
    weight : Annotated[float, Field(..., description= "The weight of the patient (in kgs)", example = 75.5)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")  
def about():    
    return {"message": "A fully functional API for Patient Management System"}

@app.get("/view")
def view(): 
    data = load_data()
    return data   

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description="The ID of the patient in DB", example = 'P001')):
    data = load_data()

    if patient_id in data:
         return data[patient_id]  
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort(sort_by : str = Query(..., description= 'Sort on the basis of height, weight or BMI'), order : str = Query('asc', description= "Sort in ascending or decending order")):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400, detail= f'Invalid Field, select from valid fields {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code= 400, detail= f'Invalid order, select from valid order asc or desc')
 
    sort_order = True if order=='desc' else False

    data = load_data() 

    sorted_data = sorted(data.values(), key= lambda x: x[sort_by], reverse= sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient : Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code= 400, detail= "Patient already exists")
    
    data[patient.id] = patient.model_dump(exclude= ['id'])

    save_data(data)

    return JSONResponse(status_code= 201, content= {"message": "Patient created successfully"})