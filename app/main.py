import asyncio
from pyexpat import model
from flask import Flask,render_template,session
#from validators import email
from api_prediction.api_app import api_app
from api_skills.skills_app import skills_app
from admin.auth_app import auth_app
from api_resume.resume_app import resume_app
from api_resume.services.extract import ResExtract
from admin.auth_service import return_admin
from service import login_required,edit_picture,super_admin_required
from models import db
from models.resumeEntity import Education, Resume,Email
from config import Config


app=Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(api_app,url_prefix="/api/pred")
app.register_blueprint(skills_app,url_prefix="/skills")
app.register_blueprint(auth_app,url_prefix="/admin")
app.register_blueprint(resume_app,url_prefix="/resume")

with app.app_context():
    db.create_all()


@app.route("/create")
@super_admin_required
def create():
    db.create_all()
    return "created"

@app.route('/',methods=['get','post'])
@login_required
def index():
    return render_template("pages/index.html",picture_form=edit_picture())



@app.route('/bata',methods=['get','post'])
async def index2():
    res=ResExtract(path="/home/sarra/Documents/projetGlsi2/app/static/resumes/pdf_docx/JPM_Hedayaty_Amin_Compliance_Analyst.pdf")
    await res.getAllDetails()
    return render_template("pages/index.html",picture_form=edit_picture())

@app.errorhandler(404)
@app.errorhandler(405)
@login_required
def erreur_404(error):
    return render_template("pages/error-404.html",picture_form=edit_picture())


if __name__ == "__main__" :
    app.run(port=8007)

