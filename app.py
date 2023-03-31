from flask import Flask , jsonify , request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api , Resource
from marshmallow import Schema, fields

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
    doctors = db.relationship('Doctor')
    
    
    def __repr__(self):
        return f"Patient(PatientId={self.PatientId}, PatientFirstName='{self.PatientFirstName}', PatientLastName='{self.PatientLastName}')"


with app.app_context():
    db.create_all()

class DoctorSchema(Schema):
    DoctorId = fields.Int()
    DoctorFirstName = fields.Str()
    DoctorLastName = fields.Str()
    SpecializationIn = fields.Str()
    Shift = fields.Str()
    PhoneNumber = fields.Str()
    Address = fields.Str()
    DoctorEmail = fields.Str()

Doctor_Schema = DoctorSchema()
Doctors_Schema = DoctorSchema(many=True)

class PatientSchema(Schema):
    PatientId = fields.Int()
    PatientFirstName = fields.Str()
    PatientLastName = fields.Str()
    SufferingFrom = fields.Str()
    DoctorAssigned = fields.Str()
    PhoneNumber = fields.Str()
    AdmitDate = fields.Date()
    Address = fields.Str()
    WardNo = fields.Int()
    BedNo = fields.Int()
    doctors = fields.Nested(DoctorSchema)
    
Patient_Schema = PatientSchema()
Patients_Schema = PatientSchema(many=True)


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
    
    
    def post(self):
        try:
            NewPatient = Patient (
                PatientId = request.json["PatientId"],
                PatientFirstName = request.json["PatientFirstName"],
                PatientLastName = request.json["PatientLastName"],
                SufferingFrom = request.json["SufferingFrom"],
                DoctorAssigned = request.json["DoctorAssigned"],
                PhoneNumber = request.json["PhoneNumber"],
                AdmitDate = request.json["AdmitDate"],
                Address = request.json["Address"],
                WardNo = request.json["WardNo"],
                BedNo = request.json["BedNo"],
                Doctor_id = request.json["Doctor_id"]
            )
            db.session.add(NewPatient)
            db.session.commit()
            Patient_Schema.dump(NewPatient)
            return {"Message" : "Successfully added!!"},200
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
            print(doctors)
            result = Doctors_Schema.dump(doctors)
            return jsonify(result)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
    def post(self):
        try:
            NewDoctor = Doctor (
                DoctorId = request.json["DoctorId"],
                DoctorFirstName = request.json["DoctorFirstName"],
                DoctorLastName = request.json["DoctorLastName"],
                SpecializationIn = request.json["SpecializationIn"],
                Shift = request.json["Shift"],
                PhoneNumber = request.json["PhoneNumber"],
                Address = request.json["Address"],
                DoctorEmail = request.json["DoctorEmail"]
            )
            db.session.add(NewDoctor)
            db.session.commit()
            Doctor_Schema.dump(NewDoctor)
            return {"Message" : "Successfully added the Doctor!!"},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df


class DoctorResource(Resource):
    def get(self, DoctorId):
        try:
            doctor = Doctor.query.get(DoctorId)
            if doctor is None:
                return "Sorry! Doctor with provided ID doesn't exist. Please check the DoctorId again."
            Result1 = Doctor_Schema.dump(doctor)
            return jsonify(Result1)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
    def patch(self, DoctorId):
        try:
            doctor = Doctor.query.get(DoctorId)
            if doctor is None:
                    return "Sorry! doctor with provided ID doesn't exist. Please check the doctorId again."
            if "DoctorId" in request.json:
                doctor.DoctorId = request.json["DoctorId"]
            if "DoctorFirstName" in request.json:
                doctor.DoctorFirstName = request.json["DoctorFirstName"]
            if "DoctorLastName" in request.json:
                doctor.DoctorLastName = request.json["DoctorLastName"]
            if "SpecializationIn" in request.json:
                doctor.SpecializationIn = request.json["SpecializationIn"]
            if "Shift" in request.json:
                doctor.Shift = request.json["Shift"]
            if "PhoneNumber" in request.json:
                doctor.PhoneNumber = request.json["PhoneNumber"]
            if "Address" in request.json:
                doctor.Address = request.json["Address"]
            if "DoctorEmail" in request.json:
                doctor.DoctorEmail = request.json["DoctorEmail"]
                
            db.session.commit()
            Doctor_Schema.dump(doctor)
            return {"Message" : "Successfully updated doctor!!"},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
        
    def put(self,DoctorId):
        try:
            doctor = Doctor.query.get(DoctorId)
            if doctor is None:
                return "Sorry! Doctor with provided ID doesn't exist. Please check the DoctorId again."
            #doctor = Doctor_Schema.load(request.json)
            doctor.DoctorId = request.json["DoctorId"]
            doctor.DoctorFirstName = request.json["DoctorFirstName"]
            doctor.DoctorLastName = request.json["DoctorLastName"]
            doctor.SpecializationIn = request.json["SpecializationIn"]
            doctor.Shift = request.json["Shift"]
            doctor.PhoneNumber = request.json["PhoneNumber"]
            doctor.Address = request.json["Address"]
            doctor.DoctorEmail = request.json["DoctorEmail"]
            db.session.commit()
            Doctor_Schema.dump(doctor)
            return {"Message" : "Successfully updated doctor!!"},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
    def delete(self, DoctorId):
        try:
            doctor = Doctor.query.get(DoctorId)
            if doctor is None:
                    return "Sorry! Doctor with provided ID doesn't exist. Please check the DoctorId again."
            db.session.delete(doctor)
            db.session.commit()
            return {"Message" : "Successfully Deleted your record."},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df



class PatientResource(Resource):
    def get(self, PatientId):
        try:
            patient = Patient.query.get(PatientId)
            if patient is None:
                return "Sorry! Patient with provided ID doesn't exist. Please check the PatientId again."
            Result1 = Patient_Schema.dump(patient)
            return jsonify(Result1)
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
    
    def put(self,PatientId):
        try:
            patient = Patient.query.get(PatientId)
            if patient is None:
                return "Sorry! Patient with provided ID doesn't exist. Please check the PatientId again."
            patient.PatientId = request.json["PatientId"]
            patient.PatientFirstName = request.json["PatientFirstName"]
            patient.PatientLastName = request.json["PatientLastName"]
            patient.SufferingFrom = request.json["SufferingFrom"]
            patient.DoctorAssigned = request.json["DoctorAssigned"]
            patient.PhoneNumber = request.json["PhoneNumber"]
            patient.AdmitDate = request.json["AdmitDate"]
            patient.Address = request.json["Address"]
            patient.WardNo = request.json["WardNo"]
            patient.BedNo = request.json["BedNo"]
            patient.Doctor_id = request.json["Doctor_id"]
            db.session.commit()
            Patient_Schema.dump(patient)
            return {"Message" : "Successfully updated patient!!"},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
    
    def patch(self, PatientId):
        try:
            patient = Patient.query.get(PatientId)
            if patient is None:
                    return "Sorry! Patient with provided ID doesn't exist. Please check the PatientId again."
            if "PatientId" in request.json:
                patient.PatientId = request.json["PatientId"]
            if "PatientFirstName" in request.json:
                patient.PatientFirstName = request.json["PatientFirstName"]
            if "PatientLastName" in request.json:
                patient.PatientLastName = request.json["PatientLastName"]
            if "SufferingFrom" in request.json:
                patient.SufferingFrom = request.json["SufferingFrom"]
            if "DoctorAssigned" in request.json:
                patient.DoctorAssigned = request.json["DoctorAssigned"]
            if "PhoneNumber" in request.json:
                patient.PhoneNumber = request.json["PhoneNumber"]
            if "AdmitDate" in request.json:
                patient.AdmitDate = request.json["AdmitDate"]
            if "Address" in request.json:
                patient.Address = request.json["Address"]
            if "WardNo" in request.json:
                patient.WardNo = request.json["WardNo"]
            if "BedNo" in request.json:
                patient.BedNo = request.json["BedNo"]
            if "Doctor_id" in request.json:
                patient.Doctor_id = request.json["Doctor_id"]
                
            db.session.commit()
            return {"Message" : "Successfully updated!!"},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
        
    def delete(self, PatientId):
        try:
            patient = Patient.query.get(PatientId)
            if patient is None:
                    return "Sorry! Patient with provided ID doesn't exist. Please check the PatientId again."
            db.session.delete(patient)
            db.session.commit()
            return {"Message" : "Successfully Deleted your record."},200
        except Exception as e:
            df = {
                "Error Status" : "404: Bad Request",
                "Error Message" : e.args[0]
            }
            print("Error : " , e)
            return df
    
    

    

api.add_resource(PatientList, "/GetAllPatients/")
api.add_resource(DoctorList, "/GetAllDoctors/")
api.add_resource(DoctorResource, "/Doctors/<int:DoctorId>/")
api.add_resource(PatientResource, "/Patients/<int:PatientId>/")


if __name__ == "__main__":
    app.run(debug=True)