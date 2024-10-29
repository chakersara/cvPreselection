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

def test_resume_add_and_delete(client):
    """Integration test for adding and deleting a resume in the same function"""

    resume_file_path = os.path.join(os.path.dirname(__file__), '../test_resume.pdf')

    with open(resume_file_path, 'rb') as file:
        resume_file = FileStorage(
            stream=file,
            filename='test_resume.pdf',
            content_type='application/pdf'
        )

        try:
            resume = resume_add(resume_file)

            assert resume is not None, "Expected resume to be added to the database"
            resume_id = resume.id_resume

            resume_del(resume_id)

            # Check if the resume has been deleted
            assert Resume.query.get(resume_id) is None, f"Expected the resume with ID {resume_id} to be deleted from the database"

        except (IntegrityError, PendingRollbackError) as e:
            pytest.fail(f"Database error occurred: {e}")

