from flask import Blueprint,render_template

api_app=Blueprint("api_app",__name__)

@api_app.route('/')
def index():
    return {"ok":"ok"}