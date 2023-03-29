from flask import Flask , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api , Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:admin1234@localhost:5432/FLASK_RELATIONSHIP'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Doctor(db.Model):
    DoctorId = db.Column(db.Integer, primary_key=True)
    DoctorFirstName = db.Column(db.String(45), nullable=False)
    DoctorLastName = db.Column(db.String(45), nullable=False)
    SpecializationIn = db.Column(db.String(100), nullable=False)
    Shift = db.Column(db.String(20),nullable = False)
    PhoneNumber = db.Column(db.String(10), nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    DoctorEmail = db.Column(db.String(120), unique=True, nullable=False)
    patients = db.relationship('Patient' , backref = 'doctor')
    
    def __repr__(self):
        return f"Doctor(DoctorId={self.DoctorId}, DoctorFirstName='{self.DoctorFirstName}', DoctorLastName='{self.DoctorLastName}')"

class Patient(db.Model):
    PatientId = db.Column(db.Integer, primary_key=True)
    PatientFirstName = db.Column(db.String(45), nullable=False)
    PatientLastName = db.Column(db.String(45), nullable=False)
    SufferingFrom = db.Column(db.String(45), nullable=False)
    DoctorAssigned = db.Column(db.String(45), nullable=False)
    PhoneNumber = db.Column(db.String(10), nullable=False)
    AdmitDate = db.Column(db.Date(),nullable = False)
    Address = db.Column(db.String(100), nullable=False)
    WardNo = db.Column(db.Integer)
    BedNo = db.Column(db.Integer)
    Doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.DoctorId'))
    
    
    def __repr__(self):
        return f"Patient(PatientId={self.PatientId}, PatientFirstName='{self.PatientFirstName}', PatientLastName='{self.PatientLastName}')"


with app.app_context():
    db.create_all()

class PatientSchema(ma.Schema):
    class Meta:
        fields = ("PatientId", "PatientFirstName", "PatientLastName", "SufferingFrom", "DoctorAssigned", "PhoneNumber", "Address", "WardNo", "BedNo" , "Doctor_id")

Patient_Schema = PatientSchema()
Patients_Schema = PatientSchema(many=True)

class DoctorSchema(ma.Schema):
    class Meta:
        fields = ("DoctorId", "DoctorFirstName", "DoctorLastName", "SpecializationIn", "Shift", "PhoneNumber", "Address", "DoctorEmail", "patients")

Doctor_Schema = DoctorSchema()
Doctors_Schema = DoctorSchema(many=True)


#creating CRUD
class PatientList(Resource):
    def get(self):
        try:
            patients = Patient.query.all()
            result = Patients_Schema.dump(patients)
            return jsonify(result)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
class DoctorList(Resource):
    def get(self):
        try:
            doctors = Doctor.query.all()
            result = Doctors_Schema.dump(doctors)
            return jsonify(result)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        

api.add_resource(PatientList, "/GetAllPatients/")
api.add_resource(DoctorList, "/GetAllDoctors/")
    


if __name__ == "__main__":
    app.run(debug=True)