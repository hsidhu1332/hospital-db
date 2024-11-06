
SET FOREIGN_KEY_CHECKS=0;
SET autocommit=0;

-- Patients table
CREATE OR REPLACE TABLE Patients (
    patient_id int AUTO_INCREMENT PRIMARY KEY,
    patient_first_name varchar(150) NOT NULL,
    patient_last_name varchar(150) NOT NULL,
    patient_date_of_birth date NOT NULL,
    patient_phone_number varchar(15) NOT NULL,
    patient_street_address varchar(100) NOT NULL,
    patient_city varchar(50) NOT NULL,
    patient_state varchar(2) NOT NULL,
    patient_zip_code varchar(10) NOT NULL,
    insurance_provider varchar(100),
    insurance_policy_number varchar(50),
    pharmacy_id int NOT NULL,
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacies(pharmacy_id) ON DELETE RESTRICT
);

-- Doctors table
CREATE OR REPLACE TABLE Doctors (
    doctor_id int AUTO_INCREMENT PRIMARY KEY,
    doctor_first_name varchar(150) NOT NULL,
    doctor_last_name varchar(150) NOT NULL,
    doctor_email varchar(100) NOT NULL,
    doctor_phone_number varchar(15) NOT NULL,
    specialty varchar(50) NOT NULL,
    license varchar(20) UNIQUE NOT NULL,
    location varchar(100)
);

-- Pharmacies table
CREATE OR REPLACE TABLE Pharmacies (
    pharmacy_id int AUTO_INCREMENT PRIMARY KEY,
    pharmacy_name varchar(150) NOT NULL,
    pharmacy_phone_number varchar(15) NOT NULL,
    pharmacy_street_address varchar(100) NOT NULL,
    pharmacy_city varchar(50) NOT NULL,
    pharmacy_state varchar(2) NOT NULL,
    pharmacy_zip_code varchar(10) NOT NULL
);

-- Medications table
CREATE OR REPLACE TABLE Medications (
    medication_id int AUTO_INCREMENT PRIMARY KEY,
    medication_name varchar(300) NOT NULL,
    dosage varchar(20) NOT NULL,
    description varchar(300),
    side_effect varchar(300)
);

-- Appointments table
CREATE OR REPLACE TABLE Appointments (
    appointment_id int AUTO_INCREMENT PRIMARY KEY,
    appointment_date date NOT NULL,
    appointment_time time NOT NULL,
    reason varchar(300) NOT NULL,
    status varchar(300) DEFAULT 'Scheduled',
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    patient_id int NOT NULL,
    doctor_id int NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE RESTRICT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE RESTRICT
);

-- PatientRecords table
CREATE OR REPLACE TABLE PatientRecords (
    patient_records_id int AUTO_INCREMENT PRIMARY KEY,
    condition_name varchar(100) NOT NULL,
    diagnosis_date date,
    notes varchar(300),
    patient_id int NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE RESTRICT
);

-- PatientDoctor table
CREATE OR REPLACE TABLE PatientDoctor (
    patient_id int NOT NULL,
    doctor_id int NOT NULL,
    PRIMARY KEY (patient_id, doctor_id),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE RESTRICT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE RESTRICT
);

-- PatientMedication table
CREATE OR REPLACE TABLE PatientMedication (
    patient_id int NOT NULL,
    medication_id int NOT NULL,
    PRIMARY KEY (patient_id, medication_id),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE RESTRICT,
    FOREIGN KEY (medication_id) REFERENCES Medications(medication_id) ON DELETE RESTRICT
);


-- Insert into Pharmacies
INSERT INTO Pharmacies (pharmacy_name, pharmacy_phone_number, pharmacy_street_address, pharmacy_city, pharmacy_state, pharmacy_zip_code) 
VALUES 
    ('Big Pharmacy', '123-555-7890', '123 Chandler Blvd', 'Corvallis', 'OR', '97330'),
    ('CVS Pharmacy', '987-555-3210', '789 Oak St', 'Corvallis', 'OR', '97330'),
    ('Medication Pharmacy', '480-555-4567', '456 Vine Ave', 'Corvallis', 'OR', '97330');

-- Insert into Patients
INSERT INTO Patients (patient_first_name, patient_last_name, patient_date_of_birth, patient_phone_number, patient_street_address, patient_city, patient_state, patient_zip_code, insurance_provider, insurance_policy_number, pharmacy_id)
VALUES 
    ('Sarah', 'Estrella', '1986-04-15', '463-123-4679', '456 Washington Ave', 'Corvallis', 'OR', '97330', 'BCBS', '124541563', (SELECT pharmacy_id FROM Pharmacies WHERE pharmacy_name = 'Big Pharmacy')),
    ('Walter', 'White', '1992-11-22', '512-987-2153', '789 Street Blvd', 'Corvallis', 'OR', '97330', 'Allstate', '465415165', (SELECT pharmacy_id FROM Pharmacies WHERE pharmacy_name = 'CVS Pharmacy')),
    ('Thomas', 'Adams', '1978-02-10', '231-541-1221', '321 Cedar Ct', 'Corvallis', 'OR', '97330', 'Medicare', '456781523', (SELECT pharmacy_id FROM Pharmacies WHERE pharmacy_name = 'Medication Pharmacy'));

-- Insert into Doctors
INSERT INTO Doctors (doctor_first_name, doctor_last_name, doctor_email, doctor_phone_number, specialty, license, location) 
VALUES 
    ('Doug', 'Smith', 'doug.smith@hospital.com', '320-987-6343', 'Cardiology', 'DOC154627', 'Corvallis'),
    ('Johnny', 'Francis', 'johnny.francis@hospital.com', '135-142-1561', 'ENT', 'DOC643254', 'Corvallis'),
    ('Abe', 'Washington', 'abe.washington@hospital.com', '485-451-4414', 'Pediatrics', 'DOC213675', 'Corvallis');

-- Insert into Medications
INSERT INTO Medications (medication_name, dosage, description, side_effect)
VALUES 
    ('Aspirin', '100 mg', 'Pain reliever', 'Nausea'),
    ('Ibuprofen', '200 mg', 'Anti-inflammatory', 'Dizziness'),
    ('Amoxicillin', '300 mg', 'Antibiotic', 'Teeth Staining');

-- Insert into Appointments
INSERT INTO Appointments (appointment_date, appointment_time, reason, patient_id, doctor_id) 
VALUES 
    ('2024-12-10', '15:30:00', 'Follow-up check', 
        (SELECT patient_id FROM Patients WHERE patient_first_name = 'Sarah' AND patient_last_name = 'Estrella' AND patient_date_of_birth = '1986-04-15'), 
        (SELECT doctor_id FROM Doctors WHERE doctor_first_name = 'Doug' AND doctor_last_name = 'Smith' AND license = 'DOC154627')),
    ('2024-11-05', '10:00:00', 'Annual exam', 
        (SELECT patient_id FROM Patients WHERE patient_first_name = 'Walter' AND patient_last_name = 'White' AND patient_date_of_birth = '1992-11-22'), 
        (SELECT doctor_id FROM Doctors WHERE doctor_first_name = 'Johnny' AND doctor_last_name = 'Francis' AND license = 'DOC643254')),
    ('2024-10-20', '15:00:00', 'Sports Physical', 
        (SELECT patient_id FROM Patients WHERE patient_first_name = 'Thomas' AND patient_last_name = 'Adams' AND patient_date_of_birth = '1978-02-10'), 
        (SELECT doctor_id FROM Doctors WHERE doctor_first_name = 'Abe' AND doctor_last_name = 'Washington' AND license = 'DOC213675'));

-- Insert into PatientRecords
INSERT INTO PatientRecords (condition_name, diagnosis_date, notes, patient_id) 
VALUES 
    ('Hypotension', '2024-01-15', 'Patient advised to increase salt intake.', 
        (SELECT patient_id FROM Patients WHERE patient_first_name = 'Sarah' AND patient_last_name = 'Estrella' AND patient_date_of_birth = '1986-04-15')),
    ('COPD', '2024-06-10', 'Inhaler prescribed.', 
        (SELECT patient_id FROM Patients WHERE patient_first_name = 'Walter' AND patient_last_name = 'White' AND patient_date_of_birth = '1992-11-22')),
    ('Diabetes', '2024-10-20', 'Monitoring sugar levels.', 
        (SELECT patient_id FROM Patients WHERE patient_first_name ='Thomas' AND patient_last_name = 'Adams' AND patient_date_of_birth = '1978-02-10'));

-- Insert into PatientDoctor
INSERT INTO PatientDoctor (patient_id, doctor_id) 
VALUES 
    ((SELECT patient_id FROM Patients WHERE patient_first_name = 'Sarah' AND patient_last_name = 'Estrella' AND patient_date_of_birth = '1986-04-15'), 
        (SELECT doctor_id FROM Doctors WHERE doctor_first_name = 'Doug' AND doctor_last_name = 'Smith' AND license = 'DOC154627')),
    ((SELECT patient_id FROM Patients WHERE patient_first_name = 'Walter' AND patient_last_name = 'White' AND patient_date_of_birth = '1992-11-22'), 
        (SELECT doctor_id FROM Doctors WHERE doctor_first_name = 'Johnny' AND doctor_last_name = 'Francis' AND license = 'DOC643254')),
    ((SELECT patient_id FROM Patients WHERE patient_first_name = 'Thomas' AND patient_last_name = 'Adams' AND patient_date_of_birth = '1978-02-10'), 
        (SELECT doctor_id FROM Doctors WHERE doctor_first_name = 'Abe' AND doctor_last_name = 'Washington' AND license = 'DOC213675'));

-- Insert into PatientMedication
INSERT INTO PatientMedication (patient_id, medication_id) 
VALUES 
    ((SELECT patient_id FROM Patients WHERE patient_first_name = 'Sarah' AND patient_last_name = 'Estrella' AND patient_date_of_birth = '1986-04-15'), 
        (SELECT medication_id FROM Medications WHERE medication_name = 'Aspirin')),
    ((SELECT patient_id FROM Patients WHERE patient_first_name = 'Walter' AND patient_last_name = 'White' AND patient_date_of_birth = '1992-11-22'), 
        (SELECT medication_id FROM Medications WHERE medication_name = 'Ibuprofen')),
    ((SELECT patient_id FROM Patients WHERE patient_first_name = 'Thomas' AND patient_last_name = 'Adams' AND patient_date_of_birth = '1978-02-10'), 
        (SELECT medication_id FROM Medications WHERE medication_name = 'Amoxicillin'));


SET FOREIGN_KEY_CHECKS=1;
COMMIT;
