from pydantic import BaseModel
from typing import List, Dict, Optional

class Patient(BaseModel):

    name : str
    age : int
    weight : float
    height : float
    bmi : float
    married : bool = False
    allergies : Optional[List[str]] = None
    contact_details : Dict[str, str]

def update_patient_data(patient : Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)

    return "Patient data inserted successfully" 

patient_info = {'name' : "Sujil S", "age" : 25, 'weight' : 75, 'height' : 175, 'bmi' : 25, 'contact_details' : {'phone' : '9876543210', 'email' : 'EMAIL'} }

patient_1 = Patient(**patient_info)

update_patient_data(patient_1)