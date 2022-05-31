# 1.0 Click the synchronize button on the tkinter desktop application
# 1.1 With the clicking of the button "Synchronize" Google Classroom makes a list of all the assignments using the Classroom.list_assignments()
# function. 
# 1.1.1 the information is taken from the Google Classroom API using services.assignments.list(courseId)
# 1.1.2 The information is in json-to-python dictionaries so it's easy to extract.
# 1.2 A Calendar is created and it's Id is saved in a file.
# 1.2.1 The calendar takes all of the assignments and sychronizes only those with due date after the sychronization-date
# 1.2.1.1(Example) Today is 19.5.2022, there are three assignments with due date: 18.5.2022, 22.5.2022, 30.5.2022 -> 
# 1.2.1.2 The only dates which are gonna go in the calendar would be 22.5.2022 and 30.5.2022.
# 1.2.2 Every assignment gets a priority point and a notification for two-days before. 
# 1.2.3 Every assignment data is stored in an Event() object which basically extracts all the needed information needed for the Google Calendar
# 1.2.4 After extracting everything in the Event() object we use the Calendar() object to create a new secondary calendar
# 1.2.5 Afterwards the program loops through the list of Event() objects and creates assignments for each of them
# 1.2.6 After finished the program creates a .txt file and writes a number, which is basically the times you have entered
# 1.2 Basically after you click 'Synchronize' once, every other time you turn on your computer the app is going to automatically 
#     update the assignments
# 1.3 The program checks the file and if it's a 1 the program starts on it's own, else it just starts. 
# 1.3.1 The program also makes a file where it keeps the date of starting the program, so it's more efficient
# 1.3.2 It checks the creationDate of the whole list of assignments and adds the ones which have creation date the same day or after the 
#       day of starting the program
# 1.3.3 It basically lists does everything in 1.1 and 1.2 but not for so many elements

from __future__ import print_function

import os.path
from ssl import cert_time_to_seconds

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Events import Calendar, Classroom

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
          'https://www.googleapis.com/auth/calendar']




def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_854789802840-bkh0l2ric3ggjoj542nh0233ro09ohi4.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        calendar = Calendar('School Helper', creds=creds)
        
        calendar.sychronize_events()
        
        

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()



