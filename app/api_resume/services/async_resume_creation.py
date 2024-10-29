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

def save_resume(path_file, path_image, path_file_name):
    try:
        ext = ResExtract(path_file)
        res = Resume(
            path_file=path_file_name,
            path_image=path_image,
            language=ext.language,
            country=ext.getCountry()
        )
        
        # Extract data
        education = ext.getEducation()  # Returns list of Education objects
        skills = ext.getSkills()        # Returns list of Skill objects
        emails = [Email(email=email, resume=res) for email in ext.getEmail()]
        phones = [Phone(number=num, resume=res) for num in ext.getPhoneNumber()]
        
        # Assign to resume
        res.educations.extend(education)
        res.skills.extend(skills)
        
        # Add to session
        db.session.add(res)
        db.session.add_all(emails)
        db.session.add_all(phones)
        
        # Commit
        db.session.commit()
        print(f"Resume {res.id_resume} saved successfully.")
        return res
    except Exception as ex:
        db.session.rollback()
        print(f"Error in save_resume: {ex}")






