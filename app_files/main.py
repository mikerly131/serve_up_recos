# Example of how to make medication request
# Assuming you have a session object already created
medication_request = MedicationRequest(patient_id=some_patient_id, provider_id=some_provider_id)
medication_request.set_medication_ids(session)  # Retrieve and set medication IDs
session.add(medication_request)
session.commit()

# Retrieve medication IDs from the MedicationRequest instance
medication_ids = medication_request.get_medication_ids()
print("Medication IDs:", medication_ids)
