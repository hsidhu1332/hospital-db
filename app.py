from flask import Flask, render_template, json, request, redirect, flash
from datetime import datetime
import os
import re
import database.db_connector as db

# File based on app.py from https://github.com/osu-cs340-ecampus/flask-starter-app
# Date: 11/19/2024

# Configuration
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
db_connection = None

def is_valid_email(email):
    # Regex to match a valid email address
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def is_valid_phone_number(phone):
    # Regex to only allow numbers with dashes
    pattern = r"^\d{3}-\d{3}-\d{4}$"
    return bool(re.match(pattern, phone))

def is_valid_future_date(date_str):
    try:
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d')  # assuming the date format is 'YYYY-MM-DD'
        return appointment_date > datetime.now()
    except ValueError:
        return False

def get_patient_data():
    # Gets all the data for the tables and makes them dictionaries
    query = """
    SELECT 
        p.patient_id,
        p.patient_first_name,
        p.patient_last_name,
        p.patient_date_of_birth,
        p.patient_phone_number,
        p.patient_street_address,
        p.patient_city,
        p.patient_state,
        p.patient_zip_code,
        p.insurance_provider,
        p.insurance_policy_number,
        ph.pharmacy_name AS pharmacy_name
    FROM 
        Patients p
    LEFT JOIN 
        Pharmacies ph
    ON 
        p.pharmacy_id = ph.pharmacy_id;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    patients = cursor.fetchall()
    
    query2 = query = """
    SELECT 
        pm.patient_id,
        pm.medication_id,
        m.medication_name,
        p.patient_first_name,
        p.patient_last_name
    FROM 
        PatientMedication pm
    JOIN 
        Medications m ON pm.medication_id = m.medication_id
    JOIN 
        Patients p ON pm.patient_id = p.patient_id;
    """
    cursor2 = db.execute_query(db_connection=db_connection, query=query2)
    patient_medications = cursor2.fetchall()

    query3 = """
    SELECT 
        pd.patient_id,
        pd.doctor_id,
        d.doctor_first_name,
        d.doctor_last_name,
        p.patient_first_name,
        p.patient_last_name
    FROM 
        PatientDoctor pd
    JOIN 
        Doctors d ON pd.doctor_id = d.doctor_id
    JOIN 
        Patients p ON pd.patient_id = p.patient_id;
    """
    cursor3 = db.execute_query(db_connection=db_connection, query=query3)
    patient_doctors = cursor3.fetchall()

    return patients, patient_medications, patient_doctors


def get_pharmacy_data():
    # Gets all the pharmacy data
    query_pharmacy = "SELECT * FROM Pharmacies;"
    cursor_pharmacy = db.execute_query(db_connection=db_connection, query=query_pharmacy)
    pharmacies = cursor_pharmacy.fetchall()
    return pharmacies

def get_medication_data():
    # Gets all the medication data
    query_medication = "SELECT * FROM Medications;"
    cursor_medication = db.execute_query(db_connection=db_connection, query=query_medication)
    medications = cursor_medication.fetchall()
    return medications

def get_doctor_data():
    # Gets all the doctor data
    query_doctor = "SELECT * FROM Doctors;"
    cursor_doctor = db.execute_query(db_connection=db_connection, query=query_doctor)
    doctors = cursor_doctor.fetchall()
    return doctors

def get_appointment_data():
    # Gets all the appointment data
    query_appointment = """
    SELECT a.appointment_id, a.appointment_date, a.appointment_time, a.reason,
           p.patient_first_name, p.patient_last_name,
           d.doctor_first_name , d.doctor_last_name
    FROM Appointments a
    JOIN Patients p ON a.patient_id = p.patient_id
    LEFT JOIN Doctors d ON a.doctor_id = d.doctor_id
    """
    cursor_appointment = db.execute_query(db_connection=db_connection,query=query_appointment)
    appointments = cursor_appointment.fetchall()
    return appointments

def get_patientrecords_data():
    # Gets all the PatientRecords data
    query = """
        SELECT 
        pr.patient_records_id,
        pr.condition_name,
        pr.diagnosis_date,
        pr.notes,
        p.patient_first_name,
        p.patient_last_name
    FROM 
        PatientRecords pr
    JOIN 
        Patients p ON pr.patient_id = p.patient_id;
    """
    cursor = db.execute_query(db_connection=db_connection, query=query)
    patientrecords = cursor.fetchall()
    return patientrecords

# Routes 
@app.route('/')
def root():
    # Renders the homepage
    return render_template("index.html")

@app.route('/patients')
def patients():
    # Get the dictionaries using the helper method
    patients, patient_medications, patient_doctors = get_patient_data()

    # Render all the tables while ensuring the forms are hidden
    return render_template('patients.j2', patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, form_type='view')
    


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    # Get all the info plus pharmacy info for the add field
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        pharmacies = get_pharmacy_data()

        
        return render_template('patients.j2', patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, pharmacies=pharmacies, form_type='add')
    # Adding an actual patient
    if request.method == 'POST':
        # Handle form submission
        patient_first_name = request.form['firstName']
        patient_last_name = request.form['lastName']
        patient_dob = request.form['dob']
        patient_phone = request.form['phone']
        patient_address = request.form['address']
        patient_city = request.form['city']
        patient_state = request.form['state']
        patient_zip = request.form['zip']
        patient_insurance = request.form['insurance']
        patient_policy_number = request.form['policyNumber']
        pharmacy_id = request.form['pharmacy']
        # Check if the pharmacy field was filled out
        
        if not patient_first_name or not patient_last_name or not patient_dob or not patient_phone or not patient_address or not patient_city or not patient_state or not patient_zip or not patient_insurance or not patient_policy_number:
            flash('All fields except Pharmacy are required.')
            return redirect('/add_patient')
    
        if not is_valid_phone_number(patient_phone):
            flash('Phone number must be exactly 10 digits and in the format XXX-XXX-XXXX.')
            return redirect('/add_patient')
        
        if len(patient_state) > 2:
            flash('State must be two letters')
            return redirect('/add_patient')
        
        if pharmacy_id == "":
            query = "INSERT INTO Patients (patient_first_name, patient_last_name, patient_date_of_birth, patient_phone_number, patient_street_address, patient_city, patient_state, patient_zip_code, insurance_provider, insurance_policy_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patient_first_name, patient_last_name, patient_dob, patient_phone, patient_address, patient_city, patient_state, patient_zip, patient_insurance, patient_policy_number))
        # Otherwise just add all of the data
        else:
            query = "INSERT INTO Patients (patient_first_name, patient_last_name, patient_date_of_birth, patient_phone_number, patient_street_address, patient_city, patient_state, patient_zip_code, insurance_provider, insurance_policy_number, pharmacy_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patient_first_name, patient_last_name, patient_dob, patient_phone, patient_address, patient_city, patient_state, patient_zip, patient_insurance, patient_policy_number, pharmacy_id))
        # Redirect back to patients when we are done (So the form is hidden)
        return redirect('/patients')
    # Render the page with the form visible

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    # Deletes the patient then redirects back to patients to update it
    query = "DELETE FROM Patients WHERE patient_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    return redirect("/patients")

@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        pharmacies = get_pharmacy_data()
        # Get the info for the patient we are editing to pre-fill in the form
        patient = db.execute_query(db_connection=db_connection, query="SELECT * FROM Patients WHERE patient_id = %s", query_params=(id,)).fetchone()

        # Fill out the table and changes to the edit form
        return render_template('patients.j2', patient_edit=patient, patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, pharmacies=pharmacies, form_type='edit')
    
    if request.method == 'POST':
        query = "SELECT * FROM Patients WHERE patient_id = %s"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
        patient_first_name = request.form['firstName']
        patient_last_name = request.form['lastName']
        patient_dob = request.form['dob']
        patient_phone = request.form['phone']
        patient_address = request.form['address']
        patient_city = request.form['city']
        patient_state = request.form['state']
        patient_zip = request.form['zip']
        patient_insurance = request.form['insurance']
        patient_policy_number = request.form['policyNumber']
        pharmacy_id = request.form['pharmacy']
        
        if not patient_first_name or not patient_last_name or not patient_dob or not patient_phone or not patient_address or not patient_city or not patient_state or not patient_zip or not patient_insurance or not patient_policy_number:
            flash('All fields except Pharmacy are required.')
            return redirect(f'/edit_patient/{id}')
    
        if not is_valid_phone_number(patient_phone):
            flash('Phone number must be exactly 10 digits and in the format XXX-XXX-XXXX.')
            return redirect(f'/edit_patient/{id}')
        
        if len(patient_state) > 2:
            flash('State must be two letters')
            return redirect(f'/edit_patient/{id}')
        
        if pharmacy_id == "":
            query = """
                UPDATE Patients 
                SET patient_first_name = %s,
                patient_last_name = %s,
                patient_date_of_birth = %s,
                patient_phone_number = %s,
                patient_street_address = %s,
                patient_city = %s,
                patient_state = %s, 
                patient_zip_code = %s, 
                insurance_provider = %s, 
                insurance_policy_number = %s,
                pharmacy_id = NULL
                WHERE patient_id = %s;
            """
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patient_first_name, patient_last_name, patient_dob, patient_phone, patient_address, patient_city, patient_state, patient_zip, patient_insurance, patient_policy_number, id))
        else:
            query = """
                UPDATE Patients 
                SET patient_first_name = %s,
                patient_last_name = %s,
                patient_date_of_birth = %s,
                patient_phone_number = %s,
                patient_street_address = %s,
                patient_city = %s,
                patient_state = %s, 
                patient_zip_code = %s, 
                insurance_provider = %s, 
                insurance_policy_number = %s,
                pharmacy_id = %s
                WHERE patient_id = %s;
            """
            # The %s's are filled in by the query_params at the end we use the parameter passed from the function for the WHERE statement
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patient_first_name, patient_last_name, patient_dob, patient_phone, patient_address, patient_city, patient_state, patient_zip, patient_insurance, patient_policy_number, pharmacy_id, id))
        return redirect('/patients')
# Listener

@app.route('/add_patientmedication', methods=['GET', 'POST'])
def add_patientmedication():
    # Get all the info plus medication info for the add field
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        medications = get_medication_data()

        return render_template('patients.j2', patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, medications=medications, form_type='add_patientmedication')
    # Adding an actual patient medication entry
    if request.method == 'POST':
        # Handle form submission
        patientmedication_patient_id = request.form['patient']
        patientmedication_medication_id = request.form['medication']

        # Check if the new relationship already exists
        query = """
        SELECT * FROM PatientMedication
        WHERE patient_id = %s AND medication_id = %s
        """
        existing_record = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(patientmedication_patient_id, patientmedication_medication_id)
        ).fetchone()
        
        if existing_record:
            flash('This patient-medication relationship already exists.')
            return redirect(f'/add_patientmedication')
        
        query = "INSERT INTO PatientMedication (patient_id, medication_id) VALUES (%s, %s);"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patientmedication_patient_id, patientmedication_medication_id))
        # Redirect back to patients when we are done (So the form is hidden)
        return redirect('/patients')
    # Render the page with the form visible

@app.route('/delete_patientmedication/<int:patient_id><int:medication_id>')
def delete_patientmedication(patient_id, medication_id):
    # Deletes the patientmedication entry then redirects back to patients to update it
    # We take both ids from the route above to make sure we are deleting the right record
    query = "DELETE FROM PatientMedication WHERE patient_id = %s AND medication_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patient_id, medication_id))
    return redirect("/patients")


@app.route('/edit_patientmedication/<int:patient_id><int:medication_id>', methods=['GET', 'POST'])
def edit_patientmedication(patient_id, medication_id):
    # Get all the info plus medication info for the add field
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        medications = get_medication_data()
        patientmedication = db.execute_query(db_connection=db_connection, query="SELECT * FROM PatientMedication WHERE patient_id = %s AND medication_id = %s", query_params=(patient_id, medication_id)).fetchone()
        return render_template('patients.j2', patientmedication_edit=patientmedication, patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, medications=medications, form_type='edit_patientmedication')
    # Edit an existing medication for a patient
    if request.method == 'POST':
        # Handle form submission
        patientmedication_patient_id = request.form['patient']
        patientmedication_medication_id = request.form['medication']
        
        # Check if the new relationship already exists
        query = """
        SELECT * FROM PatientMedication
        WHERE patient_id = %s AND medication_id = %s
        """
        existing_record = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(patientmedication_patient_id, patientmedication_medication_id)
        ).fetchone()
        
        if existing_record:
            flash('This patient-medication relationship already exists.')
            return redirect(f'/edit_patientmedication/{patient_id}{medication_id}')
      
        query = """
        UPDATE PatientMedication
        SET patient_id = %s,
        medication_id = %s
        WHERE patient_id = %s AND medication_id = %s;
        
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patientmedication_patient_id, patientmedication_medication_id, patient_id, medication_id))
        # Redirect back to patients when we are done (So the form is hidden)
        return redirect('/patients')
    # Render the page with the form visible

@app.route('/add_patientdoctor', methods=['GET', 'POST'])
def add_patientdoctor():
    # Get all the info plus doctor info for the add field
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        doctors = get_doctor_data()

        return render_template('patients.j2', patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, doctors=doctors, form_type='add_patientdoctor')
    # Adding a doctor for a patient
    if request.method == 'POST':
        # Handle form submission
        patientdoctor_patient_id = request.form['patient']
        patientdoctor_doctor_id = request.form['doctor']

        # Check if the new relationship already exists
        query = """
        SELECT * FROM PatientDoctor
        WHERE patient_id = %s AND doctor_id = %s
        """
        existing_record = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(patientdoctor_patient_id, patientdoctor_doctor_id)
        ).fetchone()
        
        if existing_record:
            flash('This patient-doctor relationship already exists.')
            return redirect(f'/add_patientdoctor')

        query = "INSERT INTO PatientDoctor (patient_id, doctor_id) VALUES (%s, %s);"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patientdoctor_patient_id, patientdoctor_doctor_id))
        # Redirect back to patients when we are done (So the form is hidden)
        return redirect('/patients')
    # Render the page with the form visible

@app.route('/delete_patientdoctor/<int:patient_id><int:doctor_id>')
def delete_patientdoctor(patient_id, doctor_id):
    # Deletes the patientdoctor entry then redirects back to patients to update it
    # We take both ids from the route above to make sure we are deleting the right record
    query = "DELETE FROM PatientDoctor WHERE patient_id = %s AND doctor_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patient_id, doctor_id))
    return redirect("/patients")


@app.route('/edit_patientdoctor/<int:patient_id><int:doctor_id>', methods=['GET', 'POST'])
def edit_patientdoctor(patient_id, doctor_id):
    
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        doctors = get_doctor_data()
        patientdoctor = db.execute_query(db_connection=db_connection, query="SELECT * FROM PatientDoctor WHERE patient_id = %s AND doctor_id = %s", query_params=(patient_id, doctor_id)).fetchone()

        return render_template('patients.j2', patientdoctor_edit=patientdoctor, patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, doctors=doctors, form_type='edit_patientdoctor')
    # Editing an actual patient doctor entry
    if request.method == 'POST':
        # Handle form submission
        patientdoctor_patient_id = request.form['patient']
        patientdoctor_doctor_id = request.form['doctor']
        
        # Check if the new relationship already exists
        query = """
        SELECT * FROM PatientDoctor
        WHERE patient_id = %s AND doctor_id = %s
        """
        existing_record = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=(patientdoctor_patient_id, patientdoctor_doctor_id)
        ).fetchone()
        
        if existing_record:
            flash('This patient-doctor relationship already exists.')
            return redirect(f'/edit_patientdoctor/{patient_id}{doctor_id}')
        
        query = """
        UPDATE PatientDoctor
        SET patient_id = %s,
        doctor_id = %s
        WHERE patient_id = %s AND doctor_id = %s;
        
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patientdoctor_patient_id, patientdoctor_doctor_id, patient_id, doctor_id))
        # Redirect back to patients when we are done (So the form is hidden)
        return redirect('/patients')
    # Render the page with the form visible

@app.route('/doctors')
def doctors():
    # Get the dictionaries using the helper method
    doctors = get_doctor_data()

    # Render all the tables (That form type makes sure the add and edit forms arent rendered)
    return render_template('doctors.j2', doctors=doctors, form_type='view')

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    # Get all the info
    if request.method == "GET":
        doctors = get_doctor_data()

        # Basically the same return but with the added form_type parameter which is a condition in the j2 file to show the add form
        return render_template('doctors.j2', doctors=doctors, form_type='add')
    # Adding an actual doctor
    if request.method == 'POST':
        # Handle form submission
        doctor_first_name = request.form['firstName']
        doctor_last_name = request.form['lastName']
        doctor_email = request.form['email']
        doctor_phone_number = request.form['phone']
        specialty = request.form['specialty']
        license = request.form['license']
        location = request.form['location']

        
        if not doctor_first_name or not doctor_last_name or not doctor_email or not doctor_phone_number or not specialty or not license or not location:
            flash('All fields are required.')
            return redirect('/add_doctor')
    
        if not is_valid_phone_number(doctor_phone_number):
            flash('Phone number must be exactly 10 digits.')
            return redirect('/add_doctor')
        
        if not is_valid_email(doctor_email):
            flash('Email address must be valid and follow the format: example@domain.com.')
            return redirect('/add_doctor')

        query = "INSERT INTO Doctors (doctor_first_name, doctor_last_name, doctor_email, doctor_phone_number, specialty, license, location) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(doctor_first_name, doctor_last_name, doctor_email, doctor_phone_number, specialty, license, location))
        # Redirect back to doctors when we are done (So the form is hidden)
        return redirect('/doctors')
    # Render the page with the form visible

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    # Deletes the doctor then redirects back to doctors to update it
    query = "DELETE FROM Doctors WHERE doctor_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    return redirect("/doctors")

@app.route('/edit_doctor/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    # Same as add gets the data and the doctor for the form
    if request.method == "GET":
        doctors = get_doctor_data()
        # Get the info for the doctor we are editing to pre-fill in the form
        doctor = db.execute_query(db_connection=db_connection, query="SELECT * FROM Doctors WHERE doctor_id = %s", query_params=(id,)).fetchone()

        # Fill out the table with edit form visible
        return render_template('doctors.j2', doctor_edit=doctor, doctors=doctors, form_type='edit')
    # Gather form data
    if request.method == 'POST':
        query = "SELECT * FROM Doctors WHERE doctor_id = %s"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
        doctor_first_name = request.form['firstName']
        doctor_last_name = request.form['lastName']
        doctor_email = request.form['email']
        doctor_phone_number = request.form['phone']
        specialty = request.form['specialty']
        license = request.form['license']
        location = request.form['location']
        
        if not doctor_first_name or not doctor_last_name or not doctor_email or not doctor_phone_number or not specialty or not license or not location:
            flash('All fields are required.')
            return redirect(f'/add_doctor/{id}')
        
        if not is_valid_phone_number(doctor_phone_number):
            flash('Phone number must be exactly 10 digits.')
            return redirect(f'/add_doctor{id}')
        
        if not is_valid_email(doctor_email):
            flash('Email address must be valid and follow the format: example@domain.com.')
            return redirect(f'/add_doctor{id}')
    
        query = """
            UPDATE Doctors 
            SET doctor_first_name = %s,
            doctor_last_name = %s,
            doctor_email = %s,
            doctor_phone_number = %s,
            specialty = %s,
            license = %s,
            location = %s
            WHERE doctor_id = %s;
            """
        # The %s's are filled in by the query_params at the end we use the parameter passed from the function for the WHERE statement
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(doctor_first_name, doctor_last_name, doctor_email, doctor_phone_number, specialty, license, location, id))
        return redirect('/doctors')

@app.route('/appointments')
def appointments():
    # Get the dictionaries using the helper method
    appointments = get_appointment_data()

    # Render all the tables (That form type makes sure the add and edit forms arent rendered)
    return render_template('appointments.j2', appointments=appointments, form_type='view')

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    # Get all the info
    if request.method == "GET":
        appointments = get_appointment_data()
        patients, patient_medications, patient_doctors = get_patient_data()
        doctors = get_doctor_data()

        # Basically the same return but with the added form_type parameter which is a condition in the j2 file to show the add form
        return render_template('appointments.j2', appointments=appointments, patients=patients, doctors=doctors, form_type='add')
    # Adding an actual appointment
    if request.method == 'POST':
        # Handle form submission
        appointment_date = request.form['date']
        appointment_time = request.form['time'] 
        reason = request.form['reason']
        patient_id = request.form['patient']
        doctor_id = request.form['doctor']
        
        # Also the %s's are filled by the query params in the cursor variable
        if not appointment_date or not appointment_time or not reason or not patient_id:
            flash('All fields are required.')
            return redirect('/add_appointment')
    
        if not is_valid_future_date(appointment_date):
            flash('The appointment date must be in the future and in a valid format (YYYY-MM-DD).')
            return redirect('/add_appointment')

        query = "INSERT INTO Appointments (appointment_date, appointment_time, reason, patient_id, doctor_id) VALUES (%s, %s, %s, %s, %s);"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(appointment_date, appointment_time, reason, patient_id, doctor_id))
        # Redirect back to appointments when we are done (So the form is hidden)
        return redirect('/appointments')
    # Render the page with the form visible

@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    # Deletes the appointment then redirects back to appointments to update it
    query = "DELETE FROM Appointments WHERE appointment_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    return redirect("/appointments")

@app.route('/edit_appointment/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    # Same as add gets the data and the appointment for the form
    if request.method == "GET":
        appointments = get_appointment_data()
        patients, patient_medications, patient_doctors = get_patient_data()
        doctors = get_doctor_data()
        # Get the info for the appointment we are editing to pre-fill in the form
        appointment = db.execute_query(db_connection=db_connection, query="SELECT * FROM Appointments WHERE appointment_id = %s", query_params=(id,)).fetchone()

        # Fill out the table (Notice now the form_type is edit so the edit form is showing)
        return render_template('appointments.j2', appointment_edit=appointment, appointments=appointments, patients=patients, doctors=doctors, form_type='edit')
    # Edit is the same as add basically just we check for the id in the query
    if request.method == 'POST':
        query = "SELECT * FROM Appointments WHERE appointment_id = %s"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
        appointment_date = request.form['date']
        appointment_time = request.form['time'] 
        reason = request.form['reason']
        patient_id = request.form['patient']
        doctor_id = request.form['doctor']
        
        if not appointment_date or not appointment_time or not reason or not patient_id:
            flash('All fields are required.')
            return redirect(f'/edit_appointment/{id}')
    
        if not is_valid_future_date(appointment_date):
            flash('The appointment date must be in the future and in a valid format (YYYY-MM-DD).')
            return redirect(f'/edit_appointment/{id}')

        if doctor_id == '':
            query = """
                UPDATE Appointments
                SET appointment_date = %s,
                appointment_time = %s, 
                reason = %s, 
                patient_id = %s, 
                doctor_id = null
                WHERE appointment_id = %s;
                """
            # The %s's are filled in by the query_params at the end we use the parameter passed from the function for the WHERE statement
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(appointment_date, appointment_time, reason, patient_id, id))
            return redirect('/appointments')
        
        else:
            query = """
                UPDATE Appointments
                SET appointment_date = %s,
                appointment_time = %s, 
                reason = %s, 
                patient_id = %s, 
                doctor_id = %s
                WHERE appointment_id = %s;
                """
            # The %s's are filled in by the query_params at the end we use the parameter passed from the function for the WHERE statement
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(appointment_date, appointment_time, reason, patient_id, doctor_id, id))
            return redirect('/appointments')
# Listener


@app.route('/medications')
def medications():
    # Get the dictionaries using the helper method
    medications = get_medication_data()

    # Render all the tables (That form type makes sure the add and edit forms arent rendered)
    return render_template('medications.j2', medications=medications, form_type='view')

@app.route('/add_medication', methods=['GET', 'POST'])
def add_medication():
    # Get all the info
    if request.method == "GET":
        medications = get_medication_data()

        # Basically the same return but with the added form_type parameter which is a condition in the j2 file to show the add form
        return render_template('medications.j2', medications=medications, form_type='add')
    # Adding an actual medication
    if request.method == 'POST':
        # Handle form submission
        medication_name = request.form['name']
        dosage = request.form['dosage']
        description = request.form['description']
        side_effect = request.form['side_effect']
        # Also the %s's are filled by the query params in the cursor variable
        if not medication_name or not dosage or not description or not side_effect:
            flash('All fields are required.')
            return redirect('/add_medication')
    
        query = "INSERT INTO Medications (medication_name, dosage, description, side_effect) VALUES (%s, %s, %s, %s);"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(medication_name, dosage, description, side_effect))
        # Redirect back to medications when we are done (So the form is hidden)
        return redirect('/medications')
    # Render the page with the form visible

@app.route('/delete_medication/<int:id>')
def delete_medication(id):
    # Deletes the medication then redirects back to medications to update it
    query = "DELETE FROM Medications WHERE medication_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    return redirect("/medications")

@app.route('/edit_medication/<int:id>', methods=['GET', 'POST'])
def edit_medication(id):
    # Same as add gets the data and the medication for the form
    if request.method == "GET":
        medications = get_medication_data()
        # Get the info for the medication we are editing to pre-fill in the form
        medication = db.execute_query(db_connection=db_connection, query="SELECT * FROM Medications WHERE medication_id = %s", query_params=(id,)).fetchone()

        # Fill out the table (Notice now the form_type is edit so the edit form is showing)
        return render_template('medications.j2', medication_edit=medication, medications=medications, form_type='edit')
    # Edit is the same as add basically just we check for the id in the query
    if request.method == 'POST':
        query = "SELECT * FROM Medications WHERE medication_id = %s"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
        medication_name = request.form['name']
        dosage = request.form['dosage']
        description = request.form['description']
        side_effect = request.form['side_effect']
        
        if not medication_name or not dosage or not description or not side_effect:
            flash('All fields except are required.')
            return redirect(f'/edit_medication/{id}')
        
        query = """
            UPDATE Medications
            SET medication_name = %s, 
            dosage = %s, 
            description = %s, 
            side_effect = %s
            WHERE medication_id = %s;
            """
        # The %s's are filled in by the query_params at the end we use the parameter passed from the function for the WHERE statement
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(medication_name, dosage, description, side_effect, id))
        return redirect('/medications')
# Listener


@app.route('/pharmacies')
def pharmacies():
    # Get the dictionaries using the helper method
    pharmacies = get_pharmacy_data()

    # Render all the tables (That form type makes sure the add and edit forms arent rendered)
    return render_template('pharmacies.j2', pharmacies=pharmacies, form_type='view')

@app.route('/add_pharmacy', methods=['GET', 'POST'])
def add_pharmacy():
    # Get all the info
    if request.method == "GET":
        pharmacies = get_pharmacy_data()

        # Basically the same return but with the added form_type parameter which is a condition in the j2 file to show the add form
        return render_template('pharmacies.j2', pharmacies=pharmacies, form_type='add')
    # Adding an actual pharmacy
    if request.method == 'POST':
        # Handle form submission
        pharmacy_name = request.form['Name']
        pharmacy_phone = request.form['phone']
        pharmacy_address = request.form['address']
        pharmacy_city = request.form['city']
        pharmacy_state = request.form['state']
        pharmacy_zip = request.form['zip']
        # Also the %s's are filled by the query params in the cursor variable
        if not pharmacy_name or not pharmacy_phone or not pharmacy_address or not pharmacy_city or not pharmacy_state or not pharmacy_zip:
            flash('All fields are required.')
            return redirect('/add_pharmacy')
    
        if not is_valid_phone_number(pharmacy_phone):
            flash('Phone number must be exactly 10 digits.')
            return redirect('/add_pharmacy')
        
        if len(pharmacy_state) > 2:
            flash('State must be two letters')
            return redirect('/add_pharmacy')

        query = "INSERT INTO Pharmacies (pharmacy_name, pharmacy_phone_number, pharmacy_street_address, pharmacy_city, pharmacy_state, pharmacy_zip_code) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(pharmacy_name, pharmacy_phone, pharmacy_address, pharmacy_city, pharmacy_state, pharmacy_zip))
        # Redirect back to pharmacies when we are done (So the form is hidden)
        return redirect('/pharmacies')
    # Render the page with the form visible

@app.route('/delete_pharmacy/<int:id>')
def delete_pharmacy(id):
    # Deletes the pharmacy then redirects back to pharmacies to update it
    query = "DELETE FROM Pharmacies WHERE pharmacy_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    return redirect("/pharmacies")

@app.route('/edit_pharmacy/<int:id>', methods=['GET', 'POST'])
def edit_pharmacy(id):
    # Same as add gets the data and the pharmacy for the form
    if request.method == "GET":
        pharmacies = get_pharmacy_data()
        # Get the info for the pharmacy we are editing to pre-fill in the form
        pharmacy = db.execute_query(db_connection=db_connection, query="SELECT * FROM Pharmacies WHERE pharmacy_id = %s", query_params=(id,)).fetchone()

        # Fill out the table (Notice now the form_type is edit so the edit form is showing)
        return render_template('pharmacies.j2', pharmacy_edit=pharmacy, pharmacies=pharmacies, form_type='edit')
    # Edit is the same as add basically just we check for the id in the query
    if request.method == 'POST':
        query = "SELECT * FROM Pharmacies WHERE pharmacy_id = %s"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
        pharmacy_name = request.form['Name']
        pharmacy_phone = request.form['phone']
        pharmacy_address = request.form['address']
        pharmacy_city = request.form['city']
        pharmacy_state = request.form['state']
        pharmacy_zip = request.form['zip']
        
        if not pharmacy_name or not pharmacy_phone or not pharmacy_address or not pharmacy_city or not pharmacy_state or not pharmacy_zip:
            flash('All fields except Pharmacy are required.')
            return redirect(f'/edit_pharmacy/{id}')
    
        if not is_valid_phone_number(pharmacy_phone):
            flash('Phone number must be exactly 10 digits.')
            return redirect(f'/edit_pharmacy/{id}')
        
        if len(pharmacy_state) > 2:
            flash('State must be two letters')
            return redirect(f'/edit_pharmacy/{id}')
        
        query = """
            UPDATE Pharmacies 
            SET pharmacy_name = %s,
            pharmacy_phone_number = %s,
            pharmacy_street_address = %s,
            pharmacy_city = %s,
            pharmacy_state = %s, 
            pharmacy_zip_code = %s
            WHERE pharmacy_id = %s;
            """
        # The %s's are filled in by the query_params at the end we use the parameter passed from the function for the WHERE statement
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(pharmacy_name, pharmacy_phone, pharmacy_address, pharmacy_city, pharmacy_state, pharmacy_zip, id))
        return redirect('/pharmacies')
# Listener

@app.route('/patientrecords')
def patientRecords():
    # Get the dictionaries using the helper method
    patientrecords = get_patientrecords_data()
    patients, patient_medications, patient_doctors = get_patient_data()

    # Render all the tables (That form type makes sure the add and edit forms arent rendered)
    return render_template('patientrecords.j2', patients=patients, patientrecords=patientrecords, form_type='view')

@app.route('/add_patientrecord', methods=['GET', 'POST'])
def add_patientrecord():
    # Get all the PatientRecord info for the add field
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        patientrecords = get_patientrecords_data()

        return render_template('patientrecords.j2', patients=patients, patientrecords=patientrecords, form_type='add')
    # Adding a record for a patient
    if request.method == 'POST':
        # Handle form submission
        patientdrecord_condition_name = request.form['Name']
        patientdrecord_diagnosis_date = request.form['diagnosis']
        patientdrecord_notes = request.form['notes']
        patientdrecord_patient_id = request.form['patient_id']
        
        if not patientdrecord_condition_name or not patientdrecord_diagnosis_date or not patientdrecord_notes:
            flash('All fields are required.')
            return redirect('/add_patientrecord')
        
        query = "INSERT INTO PatientRecords (condition_name, diagnosis_date, notes, patient_id) VALUES (%s, %s, %s, %s);"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patientdrecord_condition_name, patientdrecord_diagnosis_date, patientdrecord_notes, patientdrecord_patient_id))
        # Redirect back to patients when we are done (So the form is hidden)
        return redirect('/patientrecords')
    # Render the page with the form visible

@app.route('/delete_patientrecord/<int:id>')
def delete_patientrecord(id):
    # Deletes the patientrecord entry then redirects back to patients to update it
    # Since patientrecord has its own primary key, we can remove off that
    query = "DELETE FROM PatientRecords WHERE patient_records_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    return redirect("/patientrecords")


@app.route('/edit_patientrecord/<int:id>', methods=['GET', 'POST'])
def edit_patientrecord(id):
    # Get all the info from patientrecord
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        patientrecords = get_patientrecords_data()
        patientrecord = db.execute_query(db_connection=db_connection, query="SELECT * FROM PatientRecords WHERE patient_records_id = %s", query_params=(id,)).fetchone()

        return render_template('patientrecords.j2', patients=patients, patientrecords=patientrecords, patientrecord_edit=patientrecord, form_type='edit')
    if request.method == 'POST':
        # Handle form submission
        patientdrecord_condition_name = request.form['Name']
        patientdrecord_diagnosis_date = request.form['diagnosis']
        patientdrecord_notes = request.form['notes']
        patientdrecord_patient_id = request.form['patient_id']
        
        if not patientdrecord_condition_name or not patientdrecord_diagnosis_date or not patientdrecord_notes:
            flash('All fields are required.')
            return redirect(f'/edit_patientrecord/{id}')
        
        query = """
        UPDATE PatientRecords
        SET condition_name = %s,
        diagnosis_date = %s,
        notes = %s,
        patient_id = %s
        WHERE patient_records_id = %s;
        
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(patientdrecord_condition_name, patientdrecord_diagnosis_date, patientdrecord_notes, patientdrecord_patient_id, id))
        # Redirect back to patientrecords when we are done (So the form is hidden)
        return redirect('/patientrecords')
    # Render the page with the form visible

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7698)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
   
    app.run(port=port, debug=True)