from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, ValidationError
from typing import List, Dict, Optional, Annotated, Any

class Patient(BaseModel):

    name : Annotated[str, Field(..., title= 'Name of the patient', description= 'Give the name of patient must have charcters between  3 to 50', min_length= 3, max_length= 50)]

    email : EmailStr
    linkedin_Url : AnyUrl

    age : Annotated[int, Field(..., description= 'Age of the patient')]

    weight : Annotated[float, Field(..., description= 'Weight of the patient', gt= 0, lt= 500, strict= True)]

    height : Annotated[float, Field(..., description= 'Height of the patient', gt= 0, lt= 500, strict= True)]

    bmi : float

    married : Annotated[bool, Field(False, description= 'Married or not')]

    allergies :  Annotated[Optional[List[str]], Field(None, description= 'Allergies of the patient')]

    contact_details : Dict[str, str]

    @field_validator('email', mode= 'before')
    @classmethod
    def validate_email(cls, email):
        
        valid_domains = ['hdfc.com', 'icici.com']

        domain = email.split('@')[1]
        if domain not in valid_domains:
            raise ValueError('Invalid domain, must be from hdfc.com or icici.com')

        return email  
    
    @field_validator('name', mode= 'before')
    @classmethod
    def transform_name(cls, name):  
        return name.title()
    
    @field_validator('age', mode= 'after')
    @classmethod
    def validate_age(cls, age):
        if 0 < age < 100:
            return age
        else:   
            raise ValueError('Invalid age, must be between 0 and 100')
        
    @model_validator(mode= 'after')
    def vaildate_emergency_contact(self):
        if self.age < 18 and self.contact_details.get('emergency_contact') is None:
            raise ValueError('Emergency contact is required for patients under 18 years of age')
        return self

    @model_validator(mode="wrap")
    @classmethod
    def audit_validation(cls, data: Any, handler):
        try:
            print("🔹 WRAP: before full validation")
            return handler(data)   # ← run ALL field + model validators
        except ValidationError as e:
            print("❌ WRAP: validation failed")
            print("Raw input:", data)
            print("Errors:", e.errors())
            raise

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

patient_info = {'name' : "sujil S", 'email' : 'abc@hdfc.com', 'linkedin_Url' : 'http://linkedin.com/1323', "age" : '25', 'weight' : 75, 'height' : 175, 'bmi' : 25, 'contact_details' : {'phone' : '9876543210'} }

patient_1 = Patient(**patient_info)

update_patient_data(patient_1)