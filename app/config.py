from distutils.debug import DEBUG
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","sqlite:///../database/resume.db")
    SQLALCHEMY_TRACK_MODIFICATIONS =  os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS",True)
    DEBUG=os.environ.get("DEBUG",True)
    FLASK_RUN_PORT=os.environ.get("FLASK_RUN_PORT",7008)
    FLASK_APP=os.environ.get("FLASK_APP","main.py")
    SECRET_KEY=os.environ.get("SECRET_KEY")
    FLASK_ENV=os.environ.get("FLASK_ENV","development")
    UPLOAD_RESUMES=os.environ.get("UPLOAD_RESUMES","static/resumes/pdf_docx/")
    UPLOAD_RESUMES_IMG=os.environ.get("UPLOAD_RESUMES_IMG","static/resumes/img/")
