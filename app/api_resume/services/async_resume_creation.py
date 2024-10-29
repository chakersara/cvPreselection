from .extract import ResExtract
import asyncio
from time import time
from models.resumeEntity import Email,Phone,Resume,db

async def get_countries(ext):
    return ext.getCountry()

async def get_education(ext):
    return ext.getEducation()

async def get_emails(extract,res):
    return [ Email(email=email,resume=res) for email in extract.getEmail()]

async def get_skills(extract):
    return extract.getSkills()

async def get_phone(extract,res):
    return [Phone(number=num,resume=res) for num in extract.getPhoneNumber()]

async def get_language(extract):
    return extract.language

async def save_resume(path_file,path_image,path):
    ext=ResExtract(path)
    res=Resume(
        path_file=path_file,
        path_image=path_image,
    )
    task_country=asyncio.create_task(get_countries(ext))
    task_phones=asyncio.create_task(get_phone(ext,res))
    task_email=asyncio.create_task(get_emails(ext,res))
    task_language=asyncio.create_task(get_language(ext))
    print("nına")

    task_skills=asyncio.create_task(get_skills(ext))
    task_education=asyncio.create_task(get_education(ext))
    country,language,phones,emails,skills,education=\
    await task_country,await task_language,await task_phones,task_email,await task_skills,await task_education
    res.country=country
    res.language=language
    res.educations.extend(education)
    res.skills.extend(skills)
    print("nına")
    db.session.add(res)
    db.session.add_all(phones)
    db.session.add_all(emails)
    db.session.commit()
    print(res,"saved")







