import pytest
from main import app
from api_skills.skills_service import add_skill, delete_skill_by_id, find_skills, pagination_skills
from api_resume.services.resume_service import resume_add, resume_del, get_all_education_cvs, get_all_countries_cvs, get_all_skills_cvs, get_languages, get_languages_homepage, get_countries_homepage
import os
from models.resumeEntity import Skill, Resume
from werkzeug.datastructures import FileStorage

@pytest.fixture(scope='module')
def client():
    """Set up test client for Flask app"""
    with app.test_client() as client:
        yield client

def test_main_route(client):
    """Test the main route of the application"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_add_skill(client):
    """Integration test for adding a skill"""
    skill_name = "testskill"
    new_skill = add_skill(skill_name)
    assert new_skill.skill_name == skill_name

def test_find_skills(client):
    """Integration test for finding skills"""
    skill_name = "testskill"
    add_skill(skill_name)
    found_skills = find_skills("React")
    assert len(found_skills) > 0
    assert found_skills[0].skill_name == skill_name

def test_delete_skill(client):
    """Integration test for deleting a skill"""
    skill_name = "testskill"
    new_skill = add_skill(skill_name)
    skill_id = new_skill.id_skill
    delete_skill_by_id(skill_id)

def test_resume_add(client):
    """Integration test for adding a resume"""
    resume_file = FileStorage(
        stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
        filename='../test_resume.pdf',
        content_type='application/pdf'
    )
    resume_add(resume_file)

def test_resume_delete(client):
    """Integration test for deleting a resume"""
    resume_file = FileStorage(
        stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
        filename='../test_resume.pdf',
        content_type='application/pdf'
    )
    resume_add(resume_file)
    resume = Resume.query.first()
    resume_del(resume.id_resume)

def test_get_all_education_cvs(client):
    """Integration test for retrieving all education entries from resumes"""
    resume_file = FileStorage(
        stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
        filename='../test_resume.pdf',
        content_type='application/pdf'
    )
    resume_add(resume_file)
    education_entries = get_all_education_cvs()
    assert len(education_entries) > 0

def test_get_all_countries_cvs(client):
    """Integration test for retrieving all countries from resumes"""
    resume_file = FileStorage(
        stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
        filename='../test_resume.pdf',
        content_type='application/pdf'
    )
    resume_add(resume_file)
    countries = get_all_countries_cvs()
    assert len(countries) > 0

def test_get_all_skills_cvs(client):
    """Integration test for retrieving all skills from resumes"""
    resume_file = FileStorage(
        stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
        filename='../test_resume.pdf',
        content_type='application/pdf'
    )
    resume_add(resume_file)
    skills = get_all_skills_cvs()
    assert len(skills) > 0

def test_get_languages_homepage(client):
    """Integration test for retrieving language statistics for homepage"""
    resume_file = FileStorage(
        stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
        filename='../test_resume.pdf',
        content_type='application/pdf'
    )
    resume_add(resume_file)
    languages = get_languages_homepage()
    assert len(languages) > 0

def test_resume_filter():
    """Integration test for resume filter service"""
    resume_service = ResumeService()
    filtered_resumes = resume_service.filter_resumes(criteria={"experience": "3+ years"})
    assert isinstance(filtered_resumes, list)
    assert len(filtered_resumes) >= 1
