from fhir.resources.patient import Patient
import datetime
import json

class FHIRJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return super().default(obj)

def convert_hl7v2_to_fhir(file_path):
    with open(file_path, 'r') as file:
        hl7v2_data = file.read()

    patient_data = hl7v2_data.strip().split('\n')[2].split('|')

    patient = Patient()
    patient.id = patient_data[3]
    patient.name = [
        {
            'given': [patient_data[5].split('^')[1]],
            'family': patient_data[5].split('^')[0],
            'suffix': [patient_data[5].split('^')[2]],
        }
    ]
    patient.birthDate = datetime.datetime.strptime(patient_data[7], '%Y%m%d').date()
    patient.gender = patient_data[8]

    address_components = patient_data[11].split('^^')
    patient.address = [
        {
            'line': [address_components[0]],
            'city': address_components[1],
            'state': address_components[2] if len(address_components) >= 3 else None,
            'postalCode': address_components[3] if len(address_components) >= 4 else None,
        }
    ]
    patient.telecom = [
        {
            'system': 'phone',
            'value': patient_data[13],
        }
    ]
    patient.identifier = [
        {
            'system': 'http://example.com/patient-ids',
            'value': patient_data[19],
        }
    ]

    fhir_json = json.dumps(patient.dict(), cls=FHIRJSONEncoder)
    return fhir_json

file_path = r'D:\AJITH\Project\Cloud\patient.hl7.txt'

fhir_json = convert_hl7v2_to_fhir(file_path)
print(fhir_json)
