-- Patients
-- SELECT QUERY
SELECT * FROM Patients;

-- SELECT QUERY to populate Patients table view
SELECT patient_id, patient_first_name, patient_last_name, patient_date_of_birth, patient_phone_number, patient_street_address, patient_city, patient_state, patient_zip_code, insurance_provider, insurance_policy_number, Pharmacies.pharmacy_name 
FROM Patients INNER JOIN Pharmacies ON Patients.pharmacy_id = Pharmacies.pharmacy_id;

-- SELECT QUERY to get pharmacy name
SELECT pharmacy_name FROM Pharmacies;

-- INSERT QUERY to add a new patient
INSERT INTO Patients (patient_first_name, patient_last_name, patient_date_of_birth, patient_phone_number, patient_street_address, patient_city, patient_state, patient_zip_code, insurance_provider, insurance_policy_number, pharmacy_id)
VALUES (:patient_first_name_input, :patient_last_name_input, :patient_date_of_birth_input, :patient_phone_number_input, :patient_street_address_input, :patient_city_input, :patient_state_input, :patient_zip_code_input, :insurance_provider_input, :insurance_policy_number_input, :pharmacy_id_input);

-- UPDATE QUERY to update a patient's data based on the Update Patient form
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


-- DELETE QUERY to delete a patient
DELETE FROM Patients WHERE patient_id = :patient_id_input;

-- Doctors
-- SELECT QUERY
SELECT * FROM Doctors;

-- INSERT QUERY to add a new doctor to the database
INSERT INTO Doctors (doctor_first_name, doctor_last_name, doctor_email, doctor_phone_number, specialty, license, location) 
VALUES (:doctor_first_name_input, :doctor_last_name_input, :doctor_email_input, :doctor_phone_number_input, :specialty_input, :license_input, :location_input);

-- UPDATE QUERY to update a doctor's data based on the Update Doctor form
UPDATE Doctors
SET doctor_first_name = :doctor_first_name_input, 
    doctor_last_name = :doctor_last_name_input, 
    doctor_email = :doctor_email_input, 
    doctor_phone_number = :doctor_phone_number_input, 
    specialty = :specialty_input, 
    license = :license_input, 
    location = :location_input
WHERE doctor_id = :doctor_id_input;

-- DELETE QUERY to delete a doctor from the database
DELETE FROM Doctors WHERE doctor_id = :doctor_id_input;

-- Appointments
--SELECT QUERY
SELECT * FROM Appointments;

-- SELECT QUERY to populate Appointments table view
SELECT SELECT appointment_id, appointment_date, appointment_time, reason, CONCAT(Patients.patient_first_name, ' ', Patients.patient_last_name) AS patient_name, CONCAT(Doctors.doctor_first_name, ' ', Doctors.doctor_last_name) AS doctor_name 
FROM Appointments
INNER JOIN Patients ON Appointments.patient_id = Patients.patient_id
INNER JOIN Doctors ON Appointments.doctor_id = Doctors.doctor_id;

-- SELECT QUERY to get the patient's first name and last name
SELECT patient_first_name, patient_last_name FROM Patients;

-- SELECT QUERY to get the doctor's first name and last name
SELECT doctor_first_name, doctor_last_name FROM Doctors;

-- INSERT QUERY to add a new appointment based on the Add Appointment form
INSERT INTO Appointments (appointment_date, appointment_time, reason, patient_id, doctor_id)
VALUES (:appointment_date_input, :appointment_time_input, :reason_input, :patient_id_input, :doctor_id_input);

-- UPDATE QUERY to update an appointment's data
UPDATE Appointments
SET appointment_date = :appointment_date_input,
    appointment_time = :appointment_time_input, 
    reason = :reason_input, 
    patient_id = :patient_id_input, 
    doctor_id = :doctor_id_input
WHERE appointment_id = :appointment_id_input;

-- DELETE QUERY to delete an appointment
DELETE FROM Appointments WHERE appointment_id = :appointment_id_input;


-- Medications
-- SELECT QUERY
SELECT * FROM Medications;

-- INSERT QUERY to add a new medication to the database
INSERT INTO Medications (medication_name, dosage, description, side_effect)
VALUES (:medication_name_input, :dosage_input, :description_input, :side_effect_input);

-- UPDATE QUERY to update an existing medication's data
UPDATE Medications
SET medication_name = :medication_name_input, 
    dosage = :dosage_input, 
    description = :description_input, 
    side_effect = :side_effect_input
WHERE medication_id = :medication_id;

-- DELETE QUERY to delete a medication from the database
DELETE FROM Medications WHERE medication_id = :medication_id;

-- Pharmacies
-- SELECT QUERY
SELECT * FROM Pharmacies;

-- INSERT QUERY to add a new pharmacy to the database
INSERT INTO Pharmacies (pharmacy_name, pharmacy_phone_number, pharmacy_street_address, pharmacy_city, pharmacy_state, pharmacy_zip_code) 
VALUES (:pharmacy_name_input, :pharmacy_phone_number_input, :pharmacy_street_address_input, :pharmacy_city_input, :pharmacy_state_input, :pharmacy_zip_code_input);

-- UPDATE QUERY to update an existing pharmacy's data within the database
UPDATE Pharmacies
SET pharmacy_name = :pharmacy_name_input, 
    pharmacy_phone_number = :pharmacy_phone_number_input, 
    pharmacy_street_address = :pharmacy_street_address_input, 
    pharmacy_city = :pharmacy_city_input, 
    pharmacy_state = :pharmacy_state_input, 
    pharmacy_zip_code = :pharmacy_zip_code_input
WHERE pharmacy_id = :pharmacy_id_input;

-- DELETE QUERY to delete a pharmacy from the database
DELETE FROM Pharmacies WHERE pharmacy_id = :pharmacy_id_input;

-- Patient Records
-- SELECT QUERY
SELECT * FROM PatientRecords;

-- SELECT QUERY to get the patient's id
SELECT patient_id FROM Patients;

-- INSERT QUERY to add a new patient record
INSERT INTO PatientRecords (condition_name, diagnosis_date, notes, patient_id) 
VALUES (:condition_name_input, :diagnosis_date_input, :notes_input, :patient_id_input);

-- UPDATE QUERY to update a patient's record based on the Update Patient Records form
UPDATE PatientRecords
SET condition_name = :condition_name_input, 
    diagnosis_date = :diagnosis_date_input, 
    notes = :notes_input, 
    patient_id = :patient_id_input
WHERE patient_records_id = :patient_records_id_input;

-- DELETE QUERY to delete a patient's record from the database
DELETE FROM PatientRecords WHERE patient_records_id = :patient_records_id_input;