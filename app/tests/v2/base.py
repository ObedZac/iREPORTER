""" This is the base class for all the tests"""

import unittest
from unittest import TestCase
from flask import current_app
from app import create_app
from app.db_con import Database


class BaseTestCase(TestCase):
    """
        This class allows for an instateneous creation of the database and
        provides a blank database after every run
    """
    
    def setUp(self):
        """
            Setup the flask app for testing.
            It initializes the app and app context.
        """
        APP = create_app("testing")
        self.app = APP.test_client()
        self.app_context = APP.app_context()
        self.app_context.push()
        with APP.app_context():
            db = Database()
            db.init_db(APP)
            db.drop('incident')
            db.drop('users')
            db.create_app_tables()
        self.token = 0

        self.red_flag = {
            "record_type": "redflag",
            "title": "Kenya",
            "location": "40N, 80E",
            "images": "images",
            "video": "video",
            "comment": "say no to corruption"
        }
        self.redflag_location = {
            "location": "40N, 80E"
        }
        self.redflag_comment = {
            "comment": "say no to corruption"
        }
        self.red_flag2 = {
            "record_type": "redflag",
            "title": "Kenya",
            "location": "40N, 80E",
            "images": "images",
            "video": "video",
            "comment": "say no to corruption"
        }
        self.red_flag3 = ()


        self.update_redflag = {
            "record_type": "redflag",
            "title": "Kenya",
            "location": "40N, 80E",
            "images": "images",
            "video": "video]",
            "comment": "say no to corruption"
        }
        self.redflag_no_title = {
            "record_type": "redflag",
            "title": "",
            "location": "40N, 80E",
            "images": "images",
            "video": "video",
            "comment": "say no to corruption"
        }
        self.redflag_invalid_type = {
            "record_type": "",
            "title": "Kenya",
            "location": "40N, 80E",
            "images": 'images',
            "video": "video",
            "comment": "say no to corruption"
        }
        self.redflag_invalid_image = {
            "record_type": "redflag",
            "title": "Kenya",
            "location": "40N, 80E",
            "video": "video",
            "comment": "say no to corruption"
        }
        self.redflag_invalid_location = {
            "record_type": "redflag",
            "title": "Kenya",
            "images": "images",
            "video": "video",
            "comment": "say no to corruption"
        }
        self.redflag_no_comment = {
            "record_type": "redflag",
            "title": "Kenya",
            "location": "40N, 80E",
            "images": "images",
            "video": "video",
            "comment": ""
        }
       
        self.redflag_invalid_video = {
            "record_type": "redflag",
            "title": "NCA site auth",
            "location": "40N, 80E",
            "images": "images",
            "comment": "say no to corruption"
        }
        self.status_resolved = {
            "status": "resolved"
        }
        self.status_rejected = {
            "status": "rejected"
        }
        self.person = {
            "firstname": "carol",
            "lastname": "mumbi",
            "email": "carolmumbi@gmail.com",
            "phoneNumber": "0708123123",
            "username": "carolmobic",
            "password": "mae12#emA"
        }
        self.person1 = {
            "firstname": "mwaniki",
            "lastname": "mumbi",
            "email": "carolmumbi@gmail.com",
            "phoneNumber": "0708123123",
            "username": "carolnice",
            "password": "mae12#emA"
        }
        self.person_no_username = {
            "email": "bluish@gmail.com",
            "password": "mae12#emA"
        }
        self.person_no_email = {
            "username": "zac",
            "password": "mae12#emA"
        }
        self.person_no_password = {
            "username": "zac",
            "email": "azakkx@gmail.com",
        }
        self.person_invalid_email = {
            "username": "zac",
            "email": "azakkx.com",
            "password": "mae12#emA"
        }
        self.person_invalid_username = {
            "username": "",
            "email": "azakkx@gmail.com",
            "password": "mae12#embili"
        }
        self.person_invalid_password = {
            "username": "azakkx",
            "email": "azakkx@gmail.com",
            "password": "calculus"
        }
        self.person_existing_user = {
            "firstname": "carolol",
            "lastname": "mumbi",
            "email": "carolmumbi@gmail.com",
            "phoneNumber": "0708123123",
            "username": "carolmobic",
            "password": "calculus3"
        }

        self.correct_login = {
            "username": "carolmobic",
            "email": "carolmumbi@gmail.com",
            "password": "mae12#emA"
            }
        self.correct_login1 = {
            "username": "carolmobic",
            "password": "calculus3"
            }

        self.wrong_login = {"username": "carolmoboc",
                            "password": "azakkx"}
        self.no_username = {"username": "",
                            "password": "maembemA"}
        self.no_password = {"username": "zac",
                            "password": ""}
        self.admin = {
            "id": 1,
            "firstname": "carol",
            "lastname": "mumbi",
            "email": "carolmumbi@gmail.com",
            "phoneNumber": "0708123123",
            "username": "carolmobic",
            "registered": "26/11/2018"
        }

        self.admin_correct = {"username": "admin",
                              "password": "admn1234"}
        self.admin_wrong = {"username": "lawrence",
                            "password": "caaa"}

    def tearDown(self):
        """
            This method is called if setUp() succeeds.
            It destroys the app context.
        """
        pass


