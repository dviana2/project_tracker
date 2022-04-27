from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db= 'project_tracker_schema'

class Progress:
    def __init__(self, data):
        self.id = data ['id']
        self.date_created = data['date_created']
        self.logged_progress = data['logged_progress']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.project_id = data ['project_id']


    @classmethod
    #
    def save_progress(cls,data):
        query = """INSERT INTO progress (date_created,logged_progress,project_id)
        VALUES (%(date_created)s,%(logged_progress)s, %(project_id)s);"""
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    #we select all the entries pertaining to that specific project
    def get_all_progress_entries(cls,data):
        query = """SELECT * from progress
        join projects on projects.id = progress.project_id WHERE project_id = %(id)s
        """
        results = connectToMySQL(db).query_db(query,data)
        # print (results, "*"*60)
        all_progress= []
        for progress in results:
            all_progress.append(cls(progress))
        return all_progress


    @classmethod
    def get_one_progress_entry(cls,data):
        query = "SELECT * FROM progress join projects on projects.id = progress.project_id WHERE progress.id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return cls (results[0])

    @classmethod
    def update_progress_entry(cls, data):
        query = """
                UPDATE progress
                SET date_created= %(date_created)s, logged_progress =%(logged_progress)s
                WHERE id= %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy_progress_entry(cls,data):
        query = "DELETE FROM progress WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
