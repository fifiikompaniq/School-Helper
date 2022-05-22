# I can't test since all parts are real-time.

import unittest as ut

from click import pass_context
from Events import Classroom
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
          'https://www.googleapis.com/auth/calendar']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build("calendar", 'v3', credentials=creds)
service = build("classroom", 'v1', credentials=creds)
class TestClassroom(ut.TestCase):
    def test_get_course(self): 
        classroom = Classroom(service)
        self.assertTrue(classroom.get_course(course_id=514348985853))
        
    def test_list_course(self): 
        classroom = Classroom(service, creds=creds)
        self.assertTrue(classroom.list_courses())
    
    def test_get_assignment_from_course(self):
        classroom = Classroom(service, creds=creds)
        self.assertTrue(classroom.get_assignments_from_course(course_id=514348985853))
    
    def test_list_assignments(self):
        classroom = Classroom(service, creds=creds)
        self.assertTrue(classroom.list_assignments())

class TestCalendar(ut.TestCase): 
    def test_get_events(self): 
        pass
    
    def test_add_event(self): 
        pass
    
    def test_synchronize_events(self): 
        pass
    
    def test_update_file(self): 
        pass
    
    def update_event_by_name(self):
        pass
    
        

if __name__ == '__main__': 
    ut.main()