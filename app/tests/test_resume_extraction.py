import pytest
from flask import Flask
from api_resume.services.extract import ResExtract
from main import app 

@pytest.fixture
def cv_file_path():
    return "/Users/sarrachaker/Documents/cvPreselection/app/tests/test_resume.pdf"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_extract_language(cv_file_path):
    """Test to check if the language is extracted correctly from the CV."""
    extract = ResExtract(cv_file_path)
    language = extract.language

    expected_language = "fr"
    assert (
        language.lower() == expected_language.lower()
    ), f"Expected {expected_language}, but got {language}"

def test_extract_education(cv_file_path):
    """Test to check if education details are extracted correctly."""
    
    with app.app_context(): 
        extract = ResExtract(cv_file_path)
        educations = extract.getEducation() 
        print(educations)
        expected_educations = ['Licence', 'Mastère','Ingénierie'] 
        assert len(educations) == len(expected_educations), f"Expected {len(expected_educations)} educations, but got {len(educations)}"
        for expected in expected_educations:
            assert any(expected in edu.degree for edu in educations), f"Expected education '{expected}' not found"

def test_extract_skills(cv_file_path):
    """Test to check if skills are extracted correctly."""

    with app.app_context():
        extracted_skills =ResExtract(cv_file_path).getSkills()
        extracted_skills = {skill.skill_name for skill in extracted_skills}

        required_skills = ["excel", "autocad"]

        for skill in required_skills:
            assert skill in extracted_skills, f"Expected skill '{skill}' not found in extracted skills."

def test_extract_email(cv_file_path):
    """Test to check if email is extracted correctly."""
    with app.app_context():
        extract = ResExtract(cv_file_path)
        emails = extract.getEmail()

        expected_email = "kawtartadlaoui.00@gmail.com"
        assert (
            expected_email in emails
        ), f"Expected email '{expected_email}' not found in {emails}"

def test_extract_phone_number(cv_file_path):
    """Test to check if phone number is extracted correctly."""
    with app.app_context(): 
        phone_numbers = ResExtract(cv_file_path).getPhoneNumber()

        expected_phone_number = "+212625215151"
        assert (
            expected_phone_number in phone_numbers
        ), f"Expected phone number '{expected_phone_number}' not found in {phone_numbers}"


def test_extract_country(cv_file_path):
        """Test to check if phone number is extracted correctly."""
        with app.app_context():
            extracted_country = ResExtract(cv_file_path).getCountry()

            expected_country = "maroc"
            assert (expected_country == extracted_country) ,  f"Expected country '{expected_country}' not equal to {expected_country}"
