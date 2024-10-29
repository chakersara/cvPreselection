import pytest
from main import app
from api_skills.skills_service import add_skill, delete_skill_by_id, find_skills, pagination_skills
from api_resume.services.resume_service import resume_add, resume_del, get_all_education_cvs, get_all_countries_cvs, get_all_skills_cvs, get_languages, get_languages_homepage, get_countries_homepage
import os
from models.resumeEntity import Skill, Resume, db
from werkzeug.datastructures import FileStorage
from sqlalchemy.exc import IntegrityError, PendingRollbackError

@pytest.fixture(scope='module')
def client():
    """Set up test client for Flask app"""
    with app.test_client() as client:
        yield client



def test_main_route(client):
    """Test the main route of the application"""
    response = client.get('/')
    # Handle redirect (302) if authentication is required
    assert response.status_code in [200, 302]
    if response.status_code == 200:
        assert b'Welcome' in response.data

def test_add_skill(client):
    """Integration test for adding a skill"""
    skill_name = "testskill"
    try:
        new_skill = add_skill(skill_name)
        assert new_skill.skill_name == skill_name
    except IntegrityError as e:
        pytest.fail(f"IntegrityError occurred: {e}")


def test_find_skills(client):
    """Integration test for finding skills if it exists"""
    skill_name = "testskill"
    found_skills = find_skills(skill_name)
    assert len(found_skills) > 0
    assert found_skills[0].skill_name == skill_name

def test_delete_skill(client):
    """Integration test for deleting a skill"""
    skill_name = "testskill"
    skill = Skill.query.filter_by(skill_name=skill_name).first()

    if skill:
        skill_id = skill.id_skill
        delete_skill_by_id(skill_id)

        assert db.session.get(Skill, skill_id) is None
    else:
        pytest.fail(f"Skill '{skill_name}' not found, cannot delete.")


def test_resume_add(client):
    """Integration test for adding a resume"""
    resume_file = FileStorage(
        stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
        filename='test_resume.pdf',
        content_type='application/pdf'
    )
    resume = resume_add(resume_file)
   
# def test_resume_delete(client):
#     """Integration test for deleting a resume"""
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         resume = Resume.query.first()
#         resume_del(resume.id_resume)
#         assert Resume.query.get(resume.id_resume) is None
#     finally:
#         if resume:
#             db.session.rollback()
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         resume = Resume.query.first()
#         resume_del(resume.id_resume)
#         assert Resume.query.get(resume.id_resume) is None
#     except (IntegrityError, PendingRollbackError) as e:
#         pytest.fail(f"Database error occurred: {e}")

# def test_get_all_education_cvs(client):
#     """Integration test for retrieving all education entries from resumes"""
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         education_entries = get_all_education_cvs()
#         assert len(education_entries) > 0
#     finally:
#         resume = Resume.query.first()
#         if resume:
#             resume_del(resume.id_resume)
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         education_entries = get_all_education_cvs()
#         assert len(education_entries) > 0
#     except IntegrityError as e:
#         pytest.fail(f"IntegrityError occurred: {e}")

# def test_get_all_countries_cvs(client):
#     """Integration test for retrieving all countries from resumes"""
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         countries = get_all_countries_cvs()
#         assert len(countries) > 0
#     finally:
#         resume = Resume.query.first()
#         if resume:
#             resume_del(resume.id_resume)
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         countries = get_all_countries_cvs()
#         assert len(countries) > 0
#     except IntegrityError as e:
#         pytest.fail(f"IntegrityError occurred: {e}")

# def test_get_all_skills_cvs(client):
#     """Integration test for retrieving all skills from resumes"""
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         skills = get_all_skills_cvs()
#         assert len(skills) > 0
#     finally:
#         resume = Resume.query.first()
#         if resume:
#             resume_del(resume.id_resume)
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         skills = get_all_skills_cvs()
#         assert len(skills) > 0
#     except IntegrityError as e:
#         pytest.fail(f"IntegrityError occurred: {e}")

# def test_get_languages_homepage(client):
#     """Integration test for retrieving language statistics for homepage"""
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         languages = get_languages_homepage()
#         assert len(languages) > 0
#     finally:
#         resume = Resume.query.first()
#         if resume:
#             resume_del(resume.id_resume)
#     resume_file = FileStorage(
#         stream=open(os.path.join(os.path.dirname(__file__), '../test_resume.pdf'), 'rb'),
#         filename='test_resume.pdf',
#         content_type='application/pdf'
#     )
#     try:
#         resume_add(resume_file)
#         languages = get_languages_homepage()
#         assert len(languages) > 0
#     except IntegrityError as e:
#         pytest.fail(f"IntegrityError occurred: {e}")
