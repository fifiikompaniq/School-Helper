from datetime import datetime, date

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient import errors

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
          'https://www.googleapis.com/auth/calendar']
EMAIL = 'studentdemo767@gmail.com'
PASSWORD = 'MyNameIsJeff99'
class Event: 
    def __init__(self, title, description, date, time):
        self.title = title
        self.description = description
        self.date = date
        self.time = time
        self.priority = 0
    
    def set_priority(self): 
        if self.priority != 0: 
            return
        else: # if there's one day left till assignment due date, prio goes on 3, if 2 days -> 2 else 1
            pass
        
class Classroom: 
    def __init__(self, service, creds): 
        self.service = service
        self.creds = creds 
        self.courses = []
        self.assignments = []
        self.courseIds = []
        self.calendarUsage = []
        
        
    def get_course(self, course_id):
        """ Retrieves a classroom course by its id. """
        service = self.service
        # [START classroom_get_course]
        try:
            course = service.courses().get(id=course_id).execute()
            print('Course "{%s}" found.' % course.get('name'))
            return True
        except errors.HttpError as error:
            print('Course with ID "{%s}" not found.' % course_id)
        # [END classroom_get_course]
            return error
    
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
        """ Gets all the assignments from a course """
        service = self.service
        page_token = None
        while True: 
            response = service.courses().courseWork().list(courseId=course_id, pageToken=page_token, pageSize=100).execute()
            self.assignments.extend(response.get('courseWork', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
        if len(self.assignments) == 0:
            print('No assignments found.')
            return
        else:
            print('Assignments:')
            for ass in self.assignments:
                print(ass.get('title'), ass.get('dueDate'))
            return True
      
    def list_assignments(self): 
        """ Lists all the assignments available """
        service = self.service
        page_token = None
        if len(self.courses) == 0: 
            print("There are no courses availble!")
            return
        elif len(self.courseIds) == 0: 
            self.list_courses() 
        for id in self.courseIds: 
                while True:
                    coursework = service.courses().courseWork()
                    response = coursework.list(pageToken=page_token,courseId=id, pageSize=10).execute()

                    self.assignments.extend(response.get('courseWork', []))
                    page_token = response.get('nextPageToken', None)
                    if not page_token:
                        break
                if len(self.assignments) == 0:
                    print('No assignments found.')
                    return False
                else:
                    print('Assignemnts:')
                for assignment in self.assignments:
                    print(assignment.get('title'), assignment.get('dueDate'))
                
                return True;
    def create_calendar_events(self):
        if not self.assignments: 
            self.list_assignments()
        else: 
            for info in self.assignments: 
                event = Event(title=info.get('title'),description=info.get('description'), date=info.get('dueDate'), time=info.get('dueTime'))
                self.calendarUsage.append(event)


class Calendar: 
    def __init__(self, service, name, creds):
        self.service = service
        self.creds = creds
        self.name = name
        self.id = 0
    
    def create_calendar(self): # Creates a secondary calendar, only for the assignments
        request_body = {
            'summary': self.name
        }
        response = self.service.calendars().insert(body=request_body)
        print('New calendar with name: {}'.format(self.name))
        
    
    def add_event(self, event_info): # info should be a classroom assignment json file or dictionary. 
        dueDate = event_info.get('date')
        dueTime = event_info.get('time')
        event = {
            'summary': event_info['title'],
            'description': event_info['description'],
            'start': {
                'dateTime': '{}-{}-{}T'.format(dueDate['year'], dueDate['month'], dueDate['day']) + '00:00:00+02:00'
            },
            'end': {
            '   dateTime': '{}-{}-{}T'.format(dueDate['year'], dueDate['month'], dueDate['day']) + '{}:{}:{}+02:00'.format(dueTime['hour'])
            },
            'attendees': [
                {'email': EMAIL }
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 48 * 60},
                {'method': 'popup', 'minutes': 48 * 60},
                {'method': 'popup', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 60},
                ],
            },
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()

    
    def sychronize_events(self): 
        classroom_service = build('classroom', 'v1', credentials=self.creds)
        classroom = Classroom(classroom_service, self.creds)
        classroom.create_calendar_events()
        dueDate = date()
        today = date.today()
        for event in classroom.calendarUsage: 
            if dueDate-today < 0: 
                pass
            if dueDate-today > 2: 
                event.set_priority(1)
                self.add_event(event)
            elif dueDate-today == 1:
                event.set_priority(2)
                self.add_event(event)
            else: 
                event.set_priority(3)
                self.add_event(event)
        
            



            
            
            
            
        
    
    

