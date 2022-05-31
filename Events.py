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
        
class Classroom: 
    
    def __init__(self, creds):
        self.creds = creds  
        self.service = build('classroom', 'v1', credentials=self.creds)
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
        page_token = None
        while True:
            response = self.service.courses().list(pageToken=page_token,
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
            return self.assignments

class Calendar: 
    def __init__(self, name, creds):
        self.creds = creds
        self.service = build('calendar', 'v3', credentials=self.creds)
        self.name = name
        self.eventIds = [] 
        self.event_names = []
        self.counter = 0
           
    def get_events(self):
        events_result = self.service.events().list(calendarId='primary',
                                               maxResults=500, singleEvents=True,
                                               orderBy='startTime').execute()
        with open("times_entered.txt", "w+") as fp: 
            fp.write(str(self.counter))
        return events_result.get('items', [])
    
    def add_event(self, event_info, event_coef): 
        # the event is an Event() object consisting of chunks of the orginal json classroom response
        # the event_coef determines whether it needs to be updated or not.
        '''Adds event to Google Calendar'''
        
        dueTime = event_info['dueTime']
        dueDate = event_info['dueDate']
        if event_coef:
            today = date.today()
            dueDate = date(year=event_info['dueDate']['year'], month=event_info['dueDate']['month'], day=event_info['dueDate']['day']) 
            print("The event already exists. Updating...")
            existing = self.get_events()
            for event in existing: 
                if event['summary'] == event_info['title']: 
                    eventId = event['id']
                    event = self.service.events().get(calendarId='primary', eventId=eventId).execute()
                    # [Changes start here]
                    if dueDate - today == 1 or dueDate - today == 0: 
                        event_info['colorId'] = '4'
                    elif dueDate - today == 2: 
                        event_info['colorId'] = '5'
                    elif dueDate - today == 3: 
                        event_info['colorId'] = '6'
                    elif dueDate < today:
                        event_info['colorId'] = '11'
                    else:
                        event_info['colorId'] = '8'
                    # [Changes end here]
                    updated_event = self.service.events().update(calendarId='primary', eventId=eventId, body=event).execute()
                else: 
                    pass
        else:
            event = {
            'summary': event_info['title'],
            'description': event_info['description'],
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
        today = date.today()
        dueDate = date(year=event_info['dueDate']['year'], month=event_info['dueDate']['month'], day=event_info['dueDate']['day'])
        if dueDate - today == 1 or dueDate - today == 0:             
            event_info['colorId'] = '4'
        elif dueDate - today == 2: 
            event_info['colorId'] = '5'
        elif dueDate - today == 3: 
            event_info['colorId'] = '6'
        elif dueDate < today:
            event_info['colorId'] = '11'
        else:
            event_info['colorId'] = '8'
        event = self.service.events().insert(calendarId='primary', body=event).execute()

        

    
    def sychronize_events(self):
        classroom = Classroom(creds=self.creds)
        events = classroom.list_assignments()
        for event in events: 
            self.add_event(event, self.generate_event_coefficient(event))
        
            
    def generate_event_coefficient(self, event):
        event_list = self.get_events()
        for i in event_list:
            if i['summary'] == event['title']: 
                return True
        return False 
            

        
                
                
                
         
            



            
            
            
            
        
    
    

