from . import db

class Admin(db.Model):
    id_admin=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.Text,nullable=False)
    position=db.Column(db.String(150),nullable=False,default="Non spécifiée")
    role=db.Column(db.Text,default="admin")
    image=db.Column(db.Text,default="default.png")
    
    def __init__(self,username,email,password,role="admin",position="Non spécifiée",image="default.png") :
        self.username=username
        self.email=email
        self.password=password
        self.role=role
        self.image=image
        self.position=position
    
    def __repr__(self):
        return """Username:{}
        Email: {}
        Role: {}
        Password: {}
        Image: {}
        Position: {}""".format(self.username,self.email,self.role,self.password,self.image,self.position)