from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name : Annotated[str, Field(..., title= 'Name of the patient', description= 'Give the name of patient must have charcters between  3 to 50', min_length= 3, max_length= 50)]
    
    email : EmailStr
    linkedin_Url : AnyUrl

    age : Annotated[int, Field(..., description= 'Age of the patient', gt= 0, lt= 100)]

    weight : Annotated[float, Field(..., description= 'Weight of the patient', gt= 0, lt= 500, strict= True)]

    height : float
    bmi : float

    married : Annotated[bool, Field(False, description= 'Married or not')]

    allergies :  Annotated[Optional[List[str]], Field(None, description= 'Allergies of the patient', min_items= 1, max_items= 5)]

    contact_details : Dict[str, str]

def update_patient_data(patient : Patient):
    
    print(patient.name)
    print(patient.email)
    print(patient.linkedin_Url)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)

    return "Patient data inserted successfully" 

patient_info = {'name' : "Sujil S", 'email' : 'abc@gmail.com', 'linkedin_Url' : 'http://linkedin.com/1323', "age" : 25, 'weight' : 75, 'height' : 175, 'bmi' : 25, 'contact_details' : {'phone' : '9876543210'} }

patient_1 = Patient(**patient_info)

update_patient_data(patient_1)