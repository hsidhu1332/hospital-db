from flask import Flask, render_template, json, request, redirect
import os
import database.db_connector as db

# File based on app.py from https://github.com/osu-cs340-ecampus/flask-starter-app
# Date: 11/19/2024

# Configuration

app = Flask(__name__)
db_connection = None
def get_patient_data():
    # Gets all the data for the tables and makes them dictionaries
    query = "SELECT * FROM Patients;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    patients = cursor.fetchall()
    # These are setup with join statements so that the name is used in the table rather than the id
    # But interally the id is still used
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

# Routes 
@app.route('/')
def root():
    # Just the homepage :)
    return render_template("index.html")

@app.route('/patients')
def patients():
    # Get the dictionaries using the helper method
    patients, patient_medications, patient_doctors = get_patient_data()

    # Render all the tables (That form type makes sure the add and edit forms arent rendered)
    return render_template('patients.j2', patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, form_type='view')
    


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    # Get all the info plus pharmacy info for the add field
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        pharmacies = get_pharmacy_data()

        # Basically the same return but with the added form_type parameter which is a condition in the j2 file to show the add form
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
        # Also the %s's are filled by the query params in the cursor variable
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
    # Same as add gets the data and the pharmacy for the form
    if request.method == "GET":
        patients, patient_medications, patient_doctors = get_patient_data()
        pharmacies = get_pharmacy_data()
        # Get the info for the patient we are editing to pre-fill in the form
        patient = db.execute_query(db_connection=db_connection, query="SELECT * FROM Patients WHERE patient_id = %s", query_params=(id,)).fetchone()

        # Fill out the table (Notice now the form_type is edit so the edit form is showing)
        return render_template('patients.j2', patient_edit=patient, patients=patients, patientMedications=patient_medications, patientDoctors=patient_doctors, pharmacies=pharmacies, form_type='edit')
    # Edit is the same as add basically just we check for the id in the query
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
    # Adding an actual patient
    if request.method == 'POST':
        # Handle form submission
        patientmedication_patient_id = request.form['patient']
        patientmedication_medication_id = request.form['medication']
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
    # Adding an actual patient
    if request.method == 'POST':
        # Handle form submission
        patientdoctor_patient_id = request.form['patient']
        patientdoctor_doctor_id = request.form['doctor']
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
    # Get all the info plus doctor info for the add field
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

# Just so all the other pages render for now :)
@app.route('/doctors')
def doctors():
    return render_template("doctors.html")

@app.route('/appointments')
def appointments():
    return render_template("appointments.html")

@app.route('/medications')
def medications():
    return render_template("medications.html")

@app.route('/pharmacies')
def pharmacies():
    return render_template("pharmacies.html")

@app.route('/patientrecords')
def patientRecords():
    return render_template("patientrecords.html")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7698)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
   
    app.run(port=port, debug=True)