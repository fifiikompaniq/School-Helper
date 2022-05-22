import unittest as ut
from Events import Classroom
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
          'https://www.googleapis.com/auth/calendar']

class TestClassroom(ut.TestCase):
    def test_get_course(self): 
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build("classroom", 'v1', credentials=creds)
        classroom = Classroom(service)
        self.assertTrue(classroom.get_course(course_id=514348985853))
        
    def test_list_course(self): 
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build("classroom", 'v1', credentials=creds)
        classroom = Classroom(service, creds=creds)
        self.assertTrue(classroom.list_courses())
    
    def test_get_assignment_from_course(self):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build("classroom", 'v1', credentials=creds)
        classroom = Classroom(service, creds=creds)
        self.assertTrue(classroom.get_assignments_from_course(course_id=514348985853))
    
    def test_list_assignments(self): 
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build("classroom", 'v1', credentials=creds)
        classroom = Classroom(service, creds=creds)
        

if __name__ == '__main__': 
    ut.main()