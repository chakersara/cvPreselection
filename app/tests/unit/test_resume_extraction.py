import pytest
from api_resume.services.extract import ResExtract
from main import app 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("cv_file_path, expected_language", [
    ("tests/test_resume.pdf", "fr"),
    ("tests/test_resume2.pdf", "en")
])
def test_extract_language(cv_file_path, expected_language):
    """Test to check if the language is extracted correctly from the CVs."""
    extract = ResExtract(cv_file_path)
    language = extract.language
    assert language.lower() == expected_language.lower(), f"Expected {expected_language}, but got {language}"

@pytest.mark.parametrize("cv_file_path, expected_educations", [
    ("tests/test_resume.pdf", ['Licence', 'Mastère', 'Ingénierie']),
    ("tests/test_resume2.pdf", ['Licence','Ingénierie'])
])
def test_extract_education(cv_file_path, expected_educations):
    """Test to check if education details are extracted correctly from the CVs."""
    with app.app_context():
        educations = ResExtract(cv_file_path).getEducation()
        assert len(educations) == len(expected_educations), f"Expected {len(expected_educations)} educations, but got {len(educations)}"
        for expected in expected_educations:
            assert any(expected in edu.degree for edu in educations), f"Expected education '{expected}' not found"

@pytest.mark.parametrize("cv_file_path, expected_skills", [
    ("tests/test_resume.pdf", ["excel", "autocad"]),
    ("tests/test_resume2.pdf", ["python", "html","css"])
])
def test_extract_skills(cv_file_path, expected_skills):
    """Test to check if skills are extracted correctly from the CVs."""
    with app.app_context():
        extracted_skills = {skill.skill_name for skill in ResExtract(cv_file_path).getSkills()}
        for skill in expected_skills:
            assert skill in extracted_skills, f"Expected skill '{skill}' not found"


@pytest.mark.parametrize("cv_file_path, expected_email", [
    ("tests/test_resume.pdf", "kawtartadlaoui.00@gmail.com"),
    ("tests/test_resume2.pdf", "ankitgupta2594@gmail.com")
])
def test_extract_email(cv_file_path, expected_email):
    """Test to check if email is extracted correctly from the CVs."""
    with app.app_context():
        emails = ResExtract(cv_file_path).getEmail()
        assert expected_email in emails, f"Expected email '{expected_email}' not found"

@pytest.mark.parametrize("cv_file_path, expected_phone", [
    ("tests/test_resume.pdf", "+212625215151"),
    ("tests/test_resume2.pdf", "+917566888319")
])
def test_extract_phone_number(cv_file_path, expected_phone):
    """Test to check if phone number is extracted correctly from the CVs."""
    with app.app_context():
        phone_numbers = ResExtract(cv_file_path).getPhoneNumber()
        assert expected_phone in phone_numbers, f"Expected phone number '{expected_phone}' not found"

@pytest.mark.parametrize("cv_file_path, expected_country", [
    ("tests/test_resume.pdf", "maroc"),
    ("tests/test_resume2.pdf", "inde")
])
def test_extract_country(cv_file_path, expected_country):
    """Test to check if country is extracted correctly from the CVs."""
    with app.app_context():
        extracted_country = ResExtract(cv_file_path).getCountry()
        assert extracted_country.lower() == expected_country, f"Expected country '{expected_country}'"