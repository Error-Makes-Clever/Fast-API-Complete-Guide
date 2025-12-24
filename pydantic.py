def insert_patient_data(patient_name : str, patient_age : int):

    if type(patient_name) == str and type(patient_age) == int:
        if patient_age < 0:
            raise ValueError("Age cannot be negative")
        else:
            print(patient_name)
            print(patient_age)

            return "Patient data inserted successfully" 
    else:
        raise ValueError("Invalid input")
    

def update_patient_data(patient_name : str, patient_age : int):

    if type(patient_name) != str and type(patient_age)!= int:
        if patient_age < 0:
            raise ValueError("Age cannot be negative")
        else:
            print(patient_name)
            print(patient_age)

            return "Patient data inserted successfully" 
    else:
        raise ValueError("Invalid input")

insert_patient_data("John Doe", '30')
insert_patient_data("Jane Doe", -1)