from google.oauth2 import service_account
from googleapiclient.discovery import build


calendar_id = 'uspeshniy.ae@yandex.ru'


class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = '/home/neekee/tg/noisetg-386111-8ded38a9c817.json'


    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH, scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=credentials)


    def get_calendar_list(self):
        return self.service.calendarList().list().execute()


    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id
        }

        return self.service.calendarList().insert(
            body=calendar_list_entry
        ).execute()


    def add_event(self, calendar_id, summary: str, description: str, time_start: str, time_end: str):
        event = {
            'summary': summary,
            'location': 'Краснодар',
            'description': description,
            'start': {
                'dateTime': time_start
                #'dateTime': '2023-05-08T15:00:00+03:00',
            },
            'end': {
                'dateTime': time_end
                #'dateTime': '2023-05-08T17:00:00+03:00',
            }
        }
        return self.service.events().insert(calendarId=calendar_id, body=event).execute()


    def get_events(self, calendar_id, timeMin, timeMax, maxResults: int = 99999):
        events_result = self.service.events().list(calendarId=calendar_id, timeMin=timeMin,
                                              timeMax=timeMax, maxResults=maxResults, singleEvents=True,
                                              orderBy='startTime').execute()
        return events_result.get('items', [])


calendar = GoogleCalendar()
