import os
from random import randint
from pdf2image import convert_from_bytes
from PIL import Image 
from werkzeug.utils import secure_filename
from .extract import ResExtract
from models.resumeEntity import Skill,Education,Email,Phone,Resume,db
from config import Config
from .async_resume_creation import save_resume
from time import time

def convert2img(nameFile,image_name):
    image_path=f"{Config.UPLOAD_RESUMES_IMG}{image_name}.jpeg"
    if nameFile.endswith("pdf"):
        image = convert_from_bytes(open(f'{Config.UPLOAD_RESUMES}{nameFile}', "rb").read())[0]
        image.save(image_path, "JPEG")
    else:
        pass

def resume_del(id):
    db.session.delete(Resume.query.get(id))
    db.session.commit()


def resume_add(file):
    file_filename = secure_filename(file.filename)
    while os.path.isfile(f'{Config.UPLOAD_RESUMES}{file_filename}'):
        file_filename=str(randint(0,100))+file_filename
    path=f'{Config.UPLOAD_RESUMES}{file_filename}'
    file.save(os.path.join(path))
    image_name= file_filename.split(".")[0]
    convert2img(file_filename,image_name)
    createResume(path,file_filename,image_name+".jpeg")
    #await save_resume(path=path,path_image=image_name+".jpeg",path_file=file_filename)

def createResume(path,file,imagefile):
    extract=ResExtract(path)
    res=Resume(
        path_file=file,
        path_image=imagefile,
        language=extract.language,
        country=extract.getCountry()    
    )
    res.educations.extend(extract.getEducation())
    res.skills.extend(extract.getSkills())
    emails=[ Email(email=email,resume=res) for email in extract.getEmail()]
    phone=[Phone(number=num,resume=res) for num in extract.getPhoneNumber()]
    db.session.add(res)
    db.session.add_all(phone)
    db.session.add_all(emails)
    db.session.commit()








def resLanguage(res,extract):
    res.language=extract.language

def resCountry(res,extract):
    res.country=extract.getCountry() 

def resEducation(res,extract):
    res.educations.extend(extract.getEducation())

def resSkills(res,extract):
    res.skills.extend(extract.getSkills())

def resEmails(res,extract):
    emails=[ Email(email=email,resume=res) for email in extract.getEmail()]
    db.session.add_all(emails)

def resPhones(res,extract):
    phone=[Phone(number=num,resume=res) for num in extract.getPhoneNumber()]
    db.session.add_all(phone)