# Need to fix list_assignments().


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
    
    def set_priority(self, dueDate): 
        
        if self.priority != 0: 
            return
        else: # if there's one day left till assignment due date, prio goes on 3, if 2 days -> 2 else 1
            today = date.today()
            if dueDate < today: 
                self.priority = -1
            elif dueDate - today == 0: 
                self.priority = 1 # It's really urgent
            elif dueDate - today == 1: 
                self.priority = 2 # It's getting close
            elif dueDate - today == 2: 
                self.priority = 3 # You should start doing it
            else: 
                self.priority = 4 # Not urgent
        
class Classroom: 
    def __init__(self, service, creds):
        self.creds = creds  
        self.service = build('calendar', 'v3', credentials=self.creds)
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
            print("Can't find courses. Finding courses now...") 
            self.list_courses()
        if len(self.courseIds) == 0: 
            print("There are no ids. Creating ids now...")
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
        if len(self.assignments) == 0: 
            self.list_assignments() 
        for info in self.assignments: 
            event = Event(title=info['title'],description=info['description'], date=info['dueDate'], time=info['dueTime'])
            self.calendarUsage.append(event)


class Calendar: 
    def __init__(self, name, creds):
        self.creds = creds
        self.service = build('calendar', 'v3', credentials=self.creds)
        self.name = name
        self.eventIds = [] 
           
    def get_events(self):
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                               maxResults=500, singleEvents=True,
                                               orderBy='startTime').execute()
        self.eventIds = events_result.get('id', [])
    
    def add_event(self, event_info): # the event is an Event() object consisting of chunks of the orginal json classroom response
        '''Adds event to Google Calendar'''
        colorIds = (11, 4, 7, 5) # Those are colorIds for the Google API
        dueDate = event_info.date
        dueTime = event_info.time
        event = {
            'summary': event_info.title,
            'description': event_info.description,
            'start': {
                'dateTime': '{}-{}-{}T'.format(dueDate['year'], dueDate['month'], dueDate['day']) + '00:00:00+02:00'
            },
            'end': {
                'dateTime': '{}-{}-{}T'.format(dueDate['year'], dueDate['month'], dueDate['day']) 
                            + '{}:{}:00.0000'.format(dueTime['hours'], dueTime['minutes']),
                'timeZone': 'GMT+03:00'
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
        if not self.already_exists(event):
            event_info.set_priority(date(dueDate['year'], dueDate['month'], dueDate['day'])) #colorIds don't work fsr
            if event_info.priority < 0: 
                event['colorId'] = str(colorIds[0])
            elif event_info.priority > 3: 
                event['colorId'] = '2'
            else:
                event['colorId'] = str(colorIds[event_info.priority])
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            return True
        else: 
            print("The event already exists. Updating...") 
            return False
        

    
    def sychronize_events(self): 
        classroom_service = build('classroom', 'v1', credentials=self.creds)
        classroom = Classroom(classroom_service, self.creds)
        classroom.create_calendar_events() 
        id_counter = 0
        for event in classroom.calendarUsage:
            if not self.add_event(event): 
                pass
            else: 
                print('Event added successfully')
            
    def already_exists(self, new_event):
        events = self.get_date_events(new_event['start']['dateTime'], self.get_events())
        event_list = [new_event['summary'] for new_event in events]
        if new_event['summary'] not in event_list:
            return False
        else:
            return True

    def get_date_events(self, date, events):
        lst = []
        date = date
        for event in events:
            if event.get('start').get('dateTime'):
                d1 = event['start']['dateTime']
            if d1 == date:
                lst.append(event)
        return lst
         
            



            
            
            
            
        
    
    

