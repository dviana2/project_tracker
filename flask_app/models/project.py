from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


db= 'project_tracker_schema'

class Project:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.date_created = data['date_created']
        self.description = data ['description']
        self.technologies_used = data['technologies_used']
        self.benefits = data['benefits']
        self.status = data ['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data ['user_id']



        self.user_first_name = data ['first_name']
        self.user_last_name= data ['last_name']


    @classmethod
    def save_project(cls,data):
        query = """INSERT INTO projects (title,date_created,description,technologies_used,benefits,status,user_id)
        VALUES (%(title)s,%(date_created)s,%(description)s, %(technologies_used)s, %(benefits)s,%(status)s, %(user_id)s);"""
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def get_all_projects_with_users(cls):
        query = """SELECT * from projects
        join users on users.id = projects.user_id
        """
        results = connectToMySQL(db).query_db(query)
        print (results)
        projects= []
        for project in results:
            projects.append(cls(project))
        return projects


    @classmethod
    def get_one_project(cls,data):
        query = "SELECT * FROM projects join users on users.id = projects.user_id WHERE projects.id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return cls (results[0])

    @classmethod
    def update_project(cls, data):
        query = """
                UPDATE projects
                SET title= %(title)s, date_created= %(date_created)s,description= %(description)s, technologies_used= %(technologies_used)s, %(benefits)s, %(logged_progress)s, %(status)s
                WHERE id= %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def destroy_project(cls,data):
        query = "DELETE FROM projects WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)


    @staticmethod
    def validate_project(data):
        is_valid= True
        if len(data['title']) < 2:
            flash ("Title must be at least 2 characters!")
            is_valid = False
        if len(data['description']) < 10:
            flash ('Description must be at least 10 characters!')
            is_valid = False
        if len(data['technologies_used']) < 1:
            flash ('Please specify at least one technology used!')
            is_valid = False
        if len(data['benefits']) < 10:
            flash ('Benefits must be at least 10 characters!')
            is_valid = False
        return is_valid





