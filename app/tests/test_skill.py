import pytest
from models.resumeEntity import Skill
from api_skills.skills_service import query_find_skills, pagination_skills
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_query_find_skills_by_name():
    """Test finding skills by name match."""
    with app.app_context():
        results = query_find_skills("Java").all()
        assert len(results) > 0, "Expected at least one skill containing 'Java'"
        assert any("Java" in skill.skill_name for skill in results), "Expected 'Java' in skill names"
