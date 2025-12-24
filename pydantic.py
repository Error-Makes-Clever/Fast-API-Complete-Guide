from pydantic import BaseModel

class Patient(BaseModel):

    patient_name : str
    patient_age : int

def insert_patient_data(patient : Patient):
    
    print(patient.patient_name)
    print(patient.patient_age)

    return "Patient data inserted successfully" 

patient_info = {'patient_name' : "Sujil S", "patient_age" : 25}
patient_1 = Patient(**patient_info)

insert_patient_data(patient_1)