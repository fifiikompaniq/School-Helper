import unittest
from Events import Classroom
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
          'https://www.googleapis.com/auth/calendar']

class TestClassroom(unittest.TestCase):
    def test_get_course(self): 
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build("classroom", 'v1')
        classroom = Classroom(service)

if __name__ == '__main__': 
    unittest.main()