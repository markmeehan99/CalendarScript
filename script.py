from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] #READONLY scope


# def setEvent():


def getEvents(service):

    print("How many events would you like to view?")
    numEvents = input()


    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming %s events:' % numEvents)
    events_result = service.events().list(
                                        calendarId='primary', 
                                        timeMin=now,
                                        maxResults=numEvents,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    eventCounter = 0

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        eventCounter = eventCounter + 1

    if eventCounter < numEvents:
        print("It seems you only had %s events planned" % eventCounter)



def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    service = build('calendar', 'v3', credentials=creds)


    run = True

    while(run):
        print("What would you like to do?")
        print("1 - Check next events")
        print("2 - Set event")
        print('3 - Quit')
        option = input()
        option = int(option)

        if option == 1:
            getEvents(service)
        if option == 2:
            setEvent(service)
        if option == 3:
            run = False



if __name__ == '__main__':
    main()