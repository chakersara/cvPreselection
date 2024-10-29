import os
from random import randint
from pdf2image import convert_from_bytes
from PIL import Image
from sqlalchemy import func
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
            file_filename = f"{randint(0, 100)}_{file_filename}"
        path = f'{Config.UPLOAD_RESUMES}{file_filename}'
        file.save(os.path.join(path))
        image_name = os.path.splitext(file_filename)[0]
        convert2img(file_filename, image_name)
        save_resume(path_file=path, path_image=image_name + ".jpeg", path_file_name=file_filename)
        return True 
    except Exception as ex:
        print("error in adding resume:", ex)
        return False

def create_resume(path, file, imagefile):
    extract = ResExtract(path)
    resume = Resume(
        path_file=file,
        path_image=imagefile,
        language=extract.language,
        country=extract.getCountry()
    )
    db.session.add(resume)
    resume.educations.extend(extract.getEducation())

    # Add skills to resume by querying them from the database
    skill_names = extract.getSkills()
    add_skills_to_resume(resume, skill_names)

    # Add emails and phones
    emails = [Email(email=email, resume=resume) for email in extract.getEmail()]
    phones = [Phone(number=num, resume=resume) for num in extract.getPhoneNumber()]
    db.session.add_all(phones)
    db.session.add_all(emails)

    # Commit all changes
    db.session.commit()
    return resume


def add_skills_to_resume(resume, skill_names):
    for skill_name in skill_names:
        # Query for the skill in the database
        skill = Skill.query.filter_by(skill_name=skill_name).first()
        if skill is not None:
            # Add the skill to the resume if it is not already linked
            if skill not in resume.skills:
                resume.skills.append(skill)
        else:
            print(f"Skill '{skill_name}' not found in the database.")


def get_all_education_cvs():
    educ = []
    for resume in Resume.query.all():
        educ.extend(resume.educations)
    return [(ed.degree, ed.degree) for ed in set(educ)]


def get_all_countries_cvs():
    return sorted(list(map(lambda count: (count[0], count[0].capitalize()),
                    Resume.query.with_entities(Resume.country.distinct()).
                    filter(Resume.country != None)
                    .all())))


def get_countries_homepage():
    resumes = Resume.query.with_entities(Resume.country, func.count(Resume.country)).group_by(Resume.country).all()
    resumes = {res[0].capitalize(): res[1] for res in resumes if res[0] is not None}
    resumes["Pas définie"] = len(Resume.query.all()) - sum(resumes.values())
    return resumes


def get_all_skills_cvs():
    skills = []
    for resume in Resume.query.all():
        skills.extend(resume.skills)
    return sorted([(skill.skill_name, skill.skill_name) for skill in set(skills)])


def get_languages():
    return list(map(lambda lang: ("fr", "Français") if lang[0] == "fr"
                    else (("en", "Anglais") if lang[0] == "en" else (lang[0], lang[0])),
                    Resume.query.with_entities(Resume.language.distinct()).
                    filter(Resume.language != None).all()))


def get_languages_homepage():
    resumes = Resume.query.with_entities(Resume.language, func.count(Resume.language)).group_by(Resume.language).all()
    lan = {"fr": "Français", "en": "Anglais"}
    resumes = {lan.get(res[0], res[0]): res[1] for res in resumes if res[0] is not None}

    none_val = len(Resume.query.all()) - sum(resumes.values())
    if none_val:
        resumes["Pas définie"] = none_val
    return resumes
