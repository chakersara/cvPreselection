from sqlalchemy import or_
from models import db
from models.resumeEntity import Skill
from flask import url_for


def query_find_skills(search):
    name_like=lambda w:"{0}{1}{0}".format("%",w)
    if not search.isdigit():
        return Skill.query.filter(Skill.skill_name.like(name_like(search)))
    print(search)
    return Skill.query.filter(
        or_(
            Skill.skill_name.like(name_like(search)) ,
            Skill.id_skill==search
        )
    )

def pagination_skills(request,rows_per_pages,filter=""):
    page = request.args.get('page', 1, type=int)
    if filter:
        print(query_find_skills(filter).all())
        return query_find_skills(filter).paginate(page=page, per_page=rows_per_pages)
    return Skill.query.paginate(page=page, per_page=rows_per_pages)

def delete_skill_by_id(id):
    skill_to_delete=Skill.query.filter(Skill.id_skill==id).first()
    db.session.delete(skill_to_delete)
    db.session.commit()

def add_skill(skill_name):
    skill_entity=Skill(skill_name)
    try:
        db.session.add(skill_entity)
        db.session.commit()
    except Exception as ex:
        print(ex)
    return skill_entity



def find_skills(search):
    if not search.isdigit():
        return Skill.query.filter(Skill.skill_name.like("{1}{2}{1}".format("%",search)) ).all()
    return Skill.query.filter((
            Skill.skill_name.like("{1}{2}{1}".format("%",search)) |
            Skill.id_skill==int(search))).all()