
from app.db_con import Database
from flask_jwt_extended import get_jwt_identity
import psycopg2
import datetime

class Incident(Database):

    def __init__(self, incident_id=None, record_type=None,location=None, status=None,
                images=None, video=None, title=None, comment=None, createdBy=None):
        super().__init__('main')
        self.createdBy = self.current_user()
        self.incident_id = incident_id
        self.createdOn = datetime.datetime.now()
        self.modifiedOn = datetime.datetime.now()
        self.record_type = record_type
        self.location = location
        self.status = status
        self.images = images
        self.video = video
        self.title = title
        self.comment = comment

    def __repr__(self):
        return f'{self.comment} incident in incident Database.'

    def serialize(self):
        return dict(createdBy=self.createdBy,
                    incident_id=self.incident_id,
                    record_type=self.record_type,
                    location=self.location,
                    status=self.status,
                    comment=self.comment,
                    createdOn=self.createdOn,
                    modifiedOn=self.modifiedOn,
                    images=self.images,
                    video=self.video,
                    title=self.title
                    )

    def get_all_incidents(self):
        """
            This method returns all the posted incidents
        """
        try:
            self.cur.execute(
                "SELECT * FROM incident"
            )
            data = self.fetch_all()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
    
    def find_incidences_by_user_id(self, createdBy):
        """
        Fetch all incident records by user_id.

        :param user_id:
        :return: Incidents
        """
        command = f"SELECT * FROM incident WHERE CreatedBY={createdBy}"
        self.query(command)
        incidents = self.fetch_all()
        self.save()

        if incidents:
            return incidents
        return None

    def find_incidence_by_id(self, incident_id):
        """
        Find a record by their id

        :param record_id: record_id
        :type record_id: int
        :return: record item
        """
        command = f"SELECT * FROM incident WHERE incident_id={incident_id}"
        self.query(command)
        incidents = self.fetch_one()
        self.save()

        if incidents:
            return incidents
        return None

    def save_to_db(self):
        self.cur.execute("""
                INSERT INTO incident (record_type, createdOn, modifiedOn, title, video, images, location, status, comment, createdBy) 
                VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (self.record_type, self.createdOn, 
                self.modifiedOn, self.title, self.video, self.images, self.location, self.status, self.comment, self.createdBy))
        self.save()
        self.close()

    def get_all(self):
        self.query("SELECT * FROM incident")
        incidents = self.fetch_all()
        self.save()

        if incidents:
            return incidents
        return None

    def edit_location(self, location):
        """
        Update incident location

        :param location:
        :return: incident
        """
        self.cur.execute("""
                        UPDATE incident SET location = %s 
                        WHERE id = %s;""",
                            (location, self.incident_id))
        self.save()

    def edit_comment(self, comment):
        """
        Update incident comment

        :param comment:
        :return: Incident
        """
        self.cur.execute("""
                                UPDATE incident SET comment = %s 
                                WHERE id = %s;""",
                            (comment, self.incident_id))
        self.save()

    def edit_status(self, status):
        """
        Update incident status

        :param status:
        :return: Incident
        """
        self.cur.execute("""
                                UPDATE incident SET status = %s 
                                WHERE id = %s;""",
                            (status, self.incident_id))
        self.save()

    def delete_incident(self, incident_id):
        """
            This method removes an incident by id from the database.
            It takes the id of the incident as parameter and,
            It returns the list of incidents.
        """
        try:
            self.cur.execute(
                "DELETE FROM incident WHERE incident_id=%s", (incident_id,)
                )
            self.save()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
    
    def current_user(self):
        """
            This method gets the logged in user from a jwt token.
            It returns the username.
        """
        self.user = get_jwt_identity()
        return self.user

    