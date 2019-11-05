from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar'] #READONLY scope

#TODO: VERIFY SPECIFIC COLOR CODES FOR EACH EVENT
EXAM_COLOR = "1"
LEISURE_COLOR = "3"
DELIVERY_COLOR = "6"
YELLOW = "5"
BLUEBERRY = "9"


def selectEventType():
        print("What type of event would you like to choose?")
        print("1 - Exam/Test")
        print('2 - Project delivery')
        print('3 - Leisure event')

        type = str(input())

        return type 



def setEvent(service):
    type = selectEventType();

    if type == 1:
        color = EXAM_COLOR
    elif type == 2:
        color = DELIVERY_COLOR
    elif type == 3:
        color = LEISURE_COLOR
    else:
        color = BLUEBERRY

    GMT_0FF = '+00:00'
    name = raw_input("What name do you wish your event to have?")
    startTime = raw_input("What day/time does your event start? Please enter (YYYY)-(MM)-(DD)T(HH):(MM):(SS)")
    endTime = raw_input("What day/time does your event end? Please enter (YYYY)-(MM)-(DD)T(HH):(MM):(SS)")


    EVENT = {
        'summary': '%s' % name,
        'start': {'dateTime' : '%s%s' % (dayTime, GMT_0FF)},
        'end' : {'dateTime' : '%s%s' % (dayTime, GMT_0FF)},
        "colorId": "%s" % color
    }

    e = service.events().insert(calendarId = 'primary', sendNotifications = False, body = EVENT).execute()

    print('****%r event added!****' % e['summary'].encode('utf-8'))
    print('Start: %s' % e['start']['dateTime'])
    print('End: %s' % e['end']['dateTime'])


def deleteEvent(service):
    print('Event name?')
    name = raw_input()

    events = getEvents(service, 100)

    for event in events:
        if event['summary'] == name:
            id = event['id']
            print(id)
            e = service.events().delete(calendarId='primary', eventId=id).execute()
            print('****%r event deleted!****' % e['summary'].encode('utf-8'))



def printEvents(events):
    eventCounter = 0

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        eventCounter = eventCounter + 1



def getEvents(service, numEvents):

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
                                        calendarId='primary', 
                                        timeMin=now,
                                        maxResults=numEvents,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    return events



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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)



    run = True

    while(run):
        print("What would you like to do?")
        print("1 - Check next events")
        print("2 - Set event")
        print('3 - Delete event')
        print('4 - Quit')

        # colors = service.colors().get().execute()
        # print(colors)
        option = input()
        option = int(option)

        if option == 1:
            print("How many events would you like to view?")
            numEvents = input()
            printEvents(getEvents(service, numEvents))
        if option == 2:
            setEvent(service)
        if (option == 3):
            deleteEvent(service)
        if option == 4:
            run = False


if __name__ == '__main__':
    main()