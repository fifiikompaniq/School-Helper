from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient import errors

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
          'https://www.googleapis.com/auth/calendar']

class Classroom: 
    def __init__(self, service): 
        self.service = service
        self.courses = []
        self.assignments = []
        self.courseIds = []
        
        
    def get_course(self, course_id):
        """ Retrieves a classroom course by its id. """
        service = self.service
        # [START classroom_get_course]
        try:
            course = service.courses().get(id=course_id).execute()
            print('Course "{%s}" found.' % course.get('name'))
        except errors.HttpError as error:
            print('Course with ID "{%s}" not found.' % course_id)
        # [END classroom_get_course]
            return error
        return course
    
    def list_courses(self):
        """ Lists all classroom courses. """
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = self.service
        # [START classroom_list_courses]
        page_token = None

        while True:
            response = service.courses().list(pageToken=page_token,
                                              pageSize=100).execute()
            self.courses.extend(response.get('courses', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not self.courses:
            print('No courses found.')
            return False
        else:
            print('Courses:')
            for course in self.courses:
                self.courseIds.append(course.get('id'))
                print(course.get('name'), course.get('id'))
            return True; 
    
    
    def get_assignments_from_course(self, course_id): 
        service = self.service
        
        page_token = None
        while True: 
            response = service.courses().courseWork().list(courseId=course_id, pageToken=page_token, pageSize=100).execute()
            self.assignments.extend(response.get('courseWork', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
        if not self.assignments:
            print('No assignments found.')
            return False
        else:
            print('Assignments:')
            for ass in self.assignments:
                print(ass.get('title'), ass.get('dueDate'))
            return self.assignments; 
      
    def list_assignments(self): 
        if not self.courses: 
            print("There are no courses availble!")
            return False
        else: 
            if not self.courseIds: 
                i = 0
                for course in self.courses: 
                    self.courseIds[i] = course.get('id')
                    i+=1
            for id in self.courseIds: 
                self.assignments = self.get_assignments_from_course(id)
        return self.assignments

            
            
            
            
        
    
    

