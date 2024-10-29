from . import db

resume_skill=db.Table('resume_skill',
    db.Column('resume_id',db.Integer,db.ForeignKey('resume.id_resume')),
    db.Column('skill_id',db.Integer,db.ForeignKey('skill.id_skill'))
)

resume_education=db.Table('resume_education',
    db.Column('resume_id',db.Integer,db.ForeignKey('resume.id_resume')),
    db.Column('education_id',db.Integer,db.ForeignKey('education.id_educ'))
)


class Resume(db.Model):
    __table_args__ = {'extend_existing': True}
    id_resume=db.Column(db.Integer,primary_key=True)
    path_file=db.Column(db.Text,nullable=False)
    path_image=db.Column(db.Text,nullable=False)
    language=db.Column(db.String(15),nullable=True)
    country=db.Column(db.String(50),nullable=True)
    name=db.Column(db.Integer,nullable=True)
    emails=db.relationship("Email",backref="resume",cascade="delete, merge, save-update")
    phones=db.relationship("Phone",backref="resume",cascade="delete, merge, save-update")
    educations=db.relationship("Education",secondary="resume_education",backref="resume",lazy=True)
    skills=db.relationship('Skill',secondary="resume_skill",backref="resume")

    def __init__(self,path_file=None,path_image=None,language=None,country=None,name=None):
        self.path_file=path_file
        self.country=country
        self.language=language
        self.path_image=path_image
        self.name=name

    

class Email(db.Model):
    id_email=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.Text)
    resume_id=db.Column(db.Integer,db.ForeignKey('resume.id_resume'))


class Phone(db.Model):
    id_phone=db.Column(db.Integer,primary_key=True)
    number=db.Column(db.Text)
    resume_id=db.Column(db.Integer,db.ForeignKey('resume.id_resume'))

class Education(db.Model):
    id_educ=db.Column(db.Integer,primary_key=True)
    degree=db.Column(db.Text)
    
    def __init__(self,degree) :
        self.degree=degree

    def __repr__(self) :
        return f"Id : {self.id_educ}\nDegree : {self.degree}"

class Skill(db.Model):
    __table_args__ = {'extend_existing': True}
    id_skill = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(90), nullable=False, unique=True)

    def __init__(self, name, id=None):
        self.id_skill = id
        self.skill_name = name