# app.py

import asyncio
from flask import Flask, render_template, session
from sqlalchemy.exc import IntegrityError
from api_resume.services.resume_service import (
    get_countries_homepage,
    get_all_skills_cvs,
    get_languages_homepage
)
from api_skills.skills_app import skills_app
from admin.auth_app import auth_app
from api_resume.resume_app import resume_app
from service import login_required, edit_picture, super_admin_required
from models.resumeEntity import Skill, Education, Email, Phone, Resume, db 
from models.adminEntity import Admin
from config import Config
from werkzeug.security import generate_password_hash 
app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(skills_app, url_prefix="/skills")
app.register_blueprint(auth_app, url_prefix="/admin")
app.register_blueprint(resume_app, url_prefix="/resume")


def initialize_data():
    skills = [
        'Python', 'Java', 'JavaScript', 'C#', 'C++', 'PHP', 'SQL', 'HTML', 'CSS', 'React',
        'Angular', 'Vue.js', 'Django', 'Flask', 'Ruby on Rails', 'ASP.NET', 'Node.js',
        'Express.js', 'Spring Boot', 'Kotlin', 'Swift', 'R', 'MATLAB', 'Git', 'Docker',
        'Kubernetes', 'AWS', 'Azure', 'GCP', 'Terraform', 'AutoCAD', 'Excel', 'Revit', 'Civil 3D',
        'STAAD Pro', 'ETABS', 'SAP2000', 'Primavera', 'MS Project', 'Structural Analysis',
        'Geotechnical Engineering', 'Surveying', 'Concrete Design', 'Steel Design',
        'Project Management', 'Construction Estimation', 'Quantity Surveying',
        'Blueprint Reading', 'Safety Management', 'GIS', 'ArcGIS'
    ]

    education_levels = ['Licence', 'Mastère', 'Ingénierie']

    # Add skills to the database
    for skill_name in skills:
        existing_skill = Skill.query.filter_by(skill_name=skill_name.lower()).first()  # Adjusted to 'name'
        if not existing_skill:
            try:
                new_skill = Skill(name=skill_name.lower()) 
                db.session.add(new_skill)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Skill '{skill_name}' already exists or another integrity error occurred.")

    # Add education levels to the database
    for degree in education_levels:
        existing_degree = Education.query.filter_by(degree=degree).first()
        if not existing_degree:
            try:
                new_education = Education(degree=degree)
                db.session.add(new_education)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Education level '{degree}' already exists or another integrity error occurred.")

    # Add test admin to the database
    test_admin_email = 'test2@gmail.com'
    existing_admin = Admin.query.filter_by(email=test_admin_email).first()
    if not existing_admin:
        try:
            test_admin = Admin(
                username='test2',
                email=test_admin_email,
                password=generate_password_hash('sarratest', method='pbkdf2:sha256'),
                position='hr', 
                role='super_admin'
            )
            db.session.add(test_admin)
            db.session.commit()
            print(f"Test admin '{test_admin_email}' created successfully.")
        except IntegrityError:
            db.session.rollback()
            print(f"Test admin '{test_admin_email}' already exists or another integrity error occurred.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while creating test admin: {e}")
    else:
        print(f"Test admin '{test_admin_email}' already exists.")


with app.app_context():
    db.create_all()
    initialize_data()


@app.route("/create")
@super_admin_required
def create():
    db.create_all()
    initialize_data()
    return "created"


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template(
        "pages/index.html",
        picture_form=edit_picture(),
        countries=get_countries_homepage(),
        languages=get_languages_homepage(),
        skills=get_all_skills_cvs(),
        resumes=len(Resume.query.all())
    )


@app.errorhandler(404)
@app.errorhandler(405)
@login_required
def erreur_404(error):
    return render_template("pages/error-404.html", picture_form=edit_picture())


if __name__ == "__main__":
    app.run(port=8007)
