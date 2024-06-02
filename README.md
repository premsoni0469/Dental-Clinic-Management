<h1 align="center" id="title">Dental Clinic Management</h1>

<p id="description">Dental Clinic Management is a Django-based application designed to streamline the operations of a dental clinic. It facilitates the booking of appointments (both regular and emergency) verifies appointments via email confirmation and handles rescheduling conflicts. The application also enables doctors to manage their schedules cancel appointments and provide prescriptions to patients.</p>

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Appointment Booking: Patients can book both regular and emergency appointments.
*   OTP Verification: An OTP is sent to the patient's registered email ID for account verification.
*   Email Confirmation: An email confirmation is sent to the patient upon successful booking of an appointment
*   Appointment Rescheduling: In case an emergency appointment overlaps with a regular appointment the regular appointment can be rescheduled and a notification email is sent to the patient.
*   Appointment Cancellation: Doctors can cancel a particular appointment if necessary.
*   Prescription Management: Doctors can give prescriptions to patients through the application.

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the Repository</p>

```
git clone https://github.com/yourusername/dental-clinic-management.git
cd dental-clinic-management
```
<br>
<p>2. Create and Activate a Virtual Environment</p>

```
python -m venv
env source env/bin/activate # On Windows use `env\Scripts\activate`
```
<br>
<p>3. Install Dependencies</p>

```
pip install -r requirements.txt
```
<br>
<p>4. Run Migrations</p>

```
python manage.py migrate
```
<br>
<p>5. Create a Superuser</p>

```
python manage.py createsuperuser
```
<br>
<p>6. Run the Server</p>

```
python manage.py runserver
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Python 3.x
*   Django 3.x or later
*   A configured email backend for sending emails

<h2>💖Like my work?</h2>

For any inquiries or support please contact me at premsoni0469@gmail.com
