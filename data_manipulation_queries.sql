-- Patients -----------------------------------------------------------------------------------------------------------------------------------------------
-- SELECT QUERY
SELECT * FROM Patients;

-- SELECT QUERY to populate Patients table view
SELECT patient_id, patient_first_name, patient_last_name, patient_date_of_birth, patient_phone_number, patient_street_address, patient_city, patient_state, patient_zip_code, insurance_provider, insurance_policy_number, Pharmacies.pharmacy_name 
FROM Patients INNER JOIN Pharmacies ON Patients.pharmacy_id = Pharmacies.pharmacy_id;

-- SELECT QUERY to get pharmacy name
SELECT pharmacy_name FROM Pharmacies;

-- INSERT QUERY to add a new patient functionality with colon : patient being used to denote the variables that will have data from the backend programming language
INSERT INTO Patients (patient_first_name, patient_last_name, patient_date_of_birth, patient_phone_number, patient_street_address, patient_city, patient_state, patient_zip_code, insurance_provider, insurance_policy_number, pharmacy_id)
VALUES (:patient_first_name_input, :patient_last_name_input, :patient_date_of_birth_input, :patient_phone_number_input, :patient_street_address_input, :patient_city_input, :patient_state_input, :patient_zip_code_input, :insurance_provider_input, :insurance_policy_number_input, :pharmacy_id_input);

-- UPDATE QUERY to update a patient's data based on the Update Patient form, using colon : to denote variables that will have data from backend
UPDATE Patients 
SET patient_first_name = :patient_first_name_input,
    patient_last_name = :patient_last_name_input,
    patient_date_of_birth = :patient_date_of_birth_input,
    patient_phone_number = :patient_phone_number_input,
    patient_street_address = :patient_street_address_input,
    patient_city = :patient_city_input,
    patient_state = :patient_state_input, 
    patient_zip_code = :patient_zip_code_input, 
    insurance_provider = :insurance_provider_input, 
    insurance_policy_number = :insurance_policy_number_input,
    pharmacy_id = :pharmacy_id_input
WHERE patient_id = :patient_id_input;

-- DELETE QUERY to delete a patient, using colon : to denote variables that will have data from backend
DELETE FROM Patients WHERE patient_id = :patient_id_input;


-- Doctors ------------------------------------------------------------------------------------------------------------------------------------------------
-- SELECT QUERY
SELECT * FROM Doctors;

-- INSERT QUERY to add a new doctor to the database, using colon : to denote variables that will have data from backend
INSERT INTO Doctors (doctor_first_name, doctor_last_name, doctor_email, doctor_phone_number, specialty, license, location) 
VALUES (:doctor_first_name_input, :doctor_last_name_input, :doctor_email_input, :doctor_phone_number_input, :specialty_input, :license_input, :location_input);

-- UPDATE QUERY to update a doctor's data based on the Update Doctor form, using colon : to denote variables that will have data from backend
UPDATE Doctors
SET doctor_first_name = :doctor_first_name_input, 
    doctor_last_name = :doctor_last_name_input, 
    doctor_email = :doctor_email_input, 
    doctor_phone_number = :doctor_phone_number_input, 
    specialty = :specialty_input, 
    license = :license_input, 
    location = :location_input
WHERE doctor_id = :doctor_id_input;

-- DELETE QUERY to delete a doctor from the database, using colon : to denote variables that will have data from backend
DELETE FROM Doctors WHERE doctor_id = :doctor_id_input;


-- Appointments -------------------------------------------------------------------------------------------------------------------------------------------
--SELECT QUERY
SELECT * FROM Appointments;

-- SELECT QUERY to populate Appointments table view
SELECT appointment_id, appointment_date, appointment_time, reason, CONCAT(Patients.patient_first_name, ' ', Patients.patient_last_name) AS patient_name, CONCAT(Doctors.doctor_first_name, ' ', Doctors.doctor_last_name) AS doctor_name 
FROM Appointments
INNER JOIN Patients ON Appointments.patient_id = Patients.patient_id
INNER JOIN Doctors ON Appointments.doctor_id = Doctors.doctor_id;

-- SELECT QUERY to get the patient's first name and last name
SELECT patient_first_name, patient_last_name FROM Patients;

-- SELECT QUERY to get the doctor's first name and last name
SELECT doctor_first_name, doctor_last_name FROM Doctors;

-- INSERT QUERY to add a new appointment based on the Add Appointment form, using colon : to denote variables that will have data from backend
INSERT INTO Appointments (appointment_date, appointment_time, reason, patient_id, doctor_id)
VALUES (:appointment_date_input, :appointment_time_input, :reason_input, :patient_id_input, :doctor_id_input);

-- UPDATE QUERY to update an appointment's data, using colon : to denote variables that will have data from backend
UPDATE Appointments
SET appointment_date = :appointment_date_input,
    appointment_time = :appointment_time_input, 
    reason = :reason_input, 
    patient_id = :patient_id_input, 
    doctor_id = :doctor_id_input
WHERE appointment_id = :appointment_id_input;

-- DELETE QUERY to delete an appointment, using colon : to denote variables that will have data from backend
DELETE FROM Appointments WHERE appointment_id = :appointment_id_input;


-- Medications --------------------------------------------------------------------------------------------------------------------------------------------
-- SELECT QUERY
SELECT * FROM Medications;

-- INSERT QUERY to add a new medication to the database, using colon : to denote variables that will have data from backend
INSERT INTO Medications (medication_name, dosage, description, side_effect)
VALUES (:medication_name_input, :dosage_input, :description_input, :side_effect_input);

-- UPDATE QUERY to update an existing medication's data, using colon : to denote variables that will have data from backend
UPDATE Medications
SET medication_name = :medication_name_input, 
    dosage = :dosage_input, 
    description = :description_input, 
    side_effect = :side_effect_input
WHERE medication_id = :medication_id;

-- DELETE QUERY to delete a medication from the database, using colon : to denote variables that will have data from backend
DELETE FROM Medications WHERE medication_id = :medication_id;


-- Pharmacies ---------------------------------------------------------------------------------------------------------------------------------------------
-- SELECT QUERY
SELECT * FROM Pharmacies;

-- INSERT QUERY to add a new pharmacy to the database, using colon : to denote variables that will have data from backend
INSERT INTO Pharmacies (pharmacy_name, pharmacy_phone_number, pharmacy_street_address, pharmacy_city, pharmacy_state, pharmacy_zip_code) 
VALUES (:pharmacy_name_input, :pharmacy_phone_number_input, :pharmacy_street_address_input, :pharmacy_city_input, :pharmacy_state_input, :pharmacy_zip_code_input);

-- UPDATE QUERY to update an existing pharmacy's data within the database, using colon : to denote variables that will have data from backend
UPDATE Pharmacies
SET pharmacy_name = :pharmacy_name_input, 
    pharmacy_phone_number = :pharmacy_phone_number_input, 
    pharmacy_street_address = :pharmacy_street_address_input, 
    pharmacy_city = :pharmacy_city_input, 
    pharmacy_state = :pharmacy_state_input, 
    pharmacy_zip_code = :pharmacy_zip_code_input
WHERE pharmacy_id = :pharmacy_id_input;

-- DELETE QUERY to delete a pharmacy from the database, using colon : to denote variables that will have data from backend
DELETE FROM Pharmacies WHERE pharmacy_id = :pharmacy_id_input;


-- Patient Records ----------------------------------------------------------------------------------------------------------------------------------------
-- SELECT QUERY
SELECT * FROM PatientRecords;

-- SELECT QUERY to get the patient's id
SELECT patient_id FROM Patients;

-- INSERT QUERY to add a new patient record, using colon : to denote variables that will have data from backend
INSERT INTO PatientRecords (condition_name, diagnosis_date, notes, patient_id) 
VALUES (:condition_name_input, :diagnosis_date_input, :notes_input, :patient_id_input);

-- UPDATE QUERY to update a patient's record based on the Update Patient Records form, using colon : to denote variables that will have data from backend
UPDATE PatientRecords
SET condition_name = :condition_name_input, 
    diagnosis_date = :diagnosis_date_input, 
    notes = :notes_input, 
    patient_id = :patient_id_input
WHERE patient_records_id = :patient_records_id_input;

-- DELETE QUERY to delete a patient's record from the database, using colon : to denote variables that will have data from backend
DELETE FROM PatientRecords WHERE patient_records_id = :patient_records_id_input;


-- PatientMedication ------------------------------------------------------------------------------------------------------------------------------------------
-- SELECT QUERY
SELECT * FROM PatientMedication;

-- INSERT QUERY to assign a medication to a patient
INSERT INTO PatientMedication (patient_id, medication_id)
VALUES (:patient_id_input, :medication_id_input);

-- UPDATE QUERY to update a patient's specific medication
UPDATE PatientMedication
SET medication_id = :medication_id_input
WHERE patient_id = :patient_id_input AND medication_id = :medication_id_input;

-- UPDATE QUERY to update the patient associated with a specific medication
UPDATE PatientMedication
SET patient_id = :patient_id_input
WHERE patient_id = :patient_id_input AND medication_id = :medication_id_input;

-- DELETE QUERY to delete a specific patient-medication relationship
DELETE FROM PatientMedication WHERE patient_id = :patient_id_input AND medication_id = medication_id_input;



-- PatientDoctor ------------------------------------------------------------------------------------------------------------------------------------------
-- SELECT QUERY
SELECT * FROM PatientDoctor;

-- INSERT QUERY to assign a doctor to a patient
INSERT INTO PatientDoctor (patient_id, doctor_id)
VALUES (:patient_id_input, :doctor_id_input);

-- UPDATE QUERY to update a patient's specific doctor
UPDATE PatientDoctor
SET doctor_id = :doctor_id_input
WHERE patient_id = :patient_id_input AND doctor_id = :doctor_id_input;

-- UPDATE QUERY to update a doctor's specific patient
UPDATE PatientDoctor
SET patient_id = :patient_id_input
WHERE patient_id = :patient_id_input AND doctor_id = :doctor_id_input;

-- DELETE QUERY to delete a specific doctor-patient relationship
DELETE FROM PatientDoctor WHERE patient_id = :patient_id_input AND doctor_id = doctor_id_input;