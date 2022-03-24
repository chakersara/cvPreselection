import sqlite3

from matplotlib.pyplot import table

class Data:

    def __init__(self,dataBase="database/resume.db"):
        self.dataBase=dataBase

    def  insert_init(self,tableName,rows):
        try:
            with sqlite3.connect(self.dataBase) as connection:
                cursor=connection.cursor() 
                #sous la forme de (?,?...)
                values_str="({})".format(",".join(map(lambda x:"?",rows[0])))
                query="insert into {} values {}".format(tableName, values_str)
                cursor.executemany(query,rows)
        except Exception as ex:
            print(ex)
    
    def get_rows(self,tableName):
        with sqlite3.connect(self.dataBase) as connection:
                cursor=connection.cursor() 
                cursor.execute("select * from {}".format(tableName))
                return cursor.fetchall()

    

class SkillsData(Data):

    def __init__(self, dataBase="database/resume.db"):
        super().__init__(dataBase)
        self.skills=open("database/skills.txt").readlines()

    def __insert_init_skills(self):
        skills_rows=list(map(lambda s:[self.skills.index(s),s.strip('\n')],self.skills))
        super().insert_init("skills",skills_rows)

    def allSkills(self):
        return set(map(lambda x:x[1],super().get_rows("skills")))

    def allSkillsLower(self):
        return set(map(lambda x:x[1].lower(),super().get_rows("skills")))


if __name__ == "__main__"  :
    print(SkillsData().allSkills())


