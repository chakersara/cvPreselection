import os
from random import randint
from pdf2image import convert_from_bytes
from PIL import Image
from werkzeug.utils import secure_filename
from .extract import ResExtract
from models.resumeEntity import Skill, Education, Email, Phone, Resume, db
from config import Config
from .async_resume_creation import save_resume
from time import time


def convert2img(nameFile, image_name):
    image_path = f"{Config.UPLOAD_RESUMES_IMG}/{image_name}.jpeg"
    if nameFile.endswith("pdf"):
        image = convert_from_bytes(
            open(f'{Config.UPLOAD_RESUMES}{nameFile}', "rb").read())[0]
        image.save(image_path, "JPEG")
    else:
        pass


def resume_del(id):
    db.session.delete(Resume.query.get(id))
    db.session.commit()


def resume_add(file):
    try:
        file_filename = secure_filename(file.filename)
        while os.path.isfile(f'{Config.UPLOAD_RESUMES}{file_filename}'):
            file_filename = str(randint(0, 100))+file_filename
        path = f'{Config.UPLOAD_RESUMES}{file_filename}'
        file.save(os.path.join(path))
        image_name = file_filename.split(".")[0]
        convert2img(file_filename, image_name)
        createResume(path, file_filename, image_name+".jpeg")
    except Exception as ex:
        print(ex)
    # await save_resume(path=path,path_image=image_name+".jpeg",path_file=file_filename)


def createResume(path, file, imagefile):
    extract = ResExtract(path)
    res = Resume(
        path_file=file,
        path_image=imagefile,
        language=extract.language,
        country=extract.getCountry()
    )
    res.educations.extend(extract.getEducation())
    res.skills.extend(extract.getSkills())
    emails = [Email(email=email, resume=res) for email in extract.getEmail()]
    phone = [Phone(number=num, resume=res) for num in extract.getPhoneNumber()]
    db.session.add(res)
    db.session.add_all(phone)
    db.session.add_all(emails)
    db.session.commit()


def get_all_education_cvs():
    educ = []
    for resume in Resume.query.all():
        educ.extend(resume.educations)
    return [(ed.degree, ed.degree) for ed in set(educ)]


def get_all_countries_cvs():
    return list(map(lambda count: (count[0], count[0].capitalize()),
                    Resume.query.with_entities(Resume.country.distinct()).
                    filter(Resume.country != None)
                    .all()))


def get_all_skills_cvs():
    skills = []
    for resume in Resume.query.all():
        skills.extend(resume.skills)
    return [(skill.skill_name, skill.skill_name) for skill in set(skills)]


def get_languages():
    return list(map(lambda lang: ("fr", "Français") if lang[0] == "fr"
                    else (("en", "Anglais") if lang[0] == "en" else (lang[0], lang[0])),
                    Resume.query.with_entities(Resume.language.distinct()).
                    filter(Resume.language != None).all()))
