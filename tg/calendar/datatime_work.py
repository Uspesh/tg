import datetime

from tg.calendar.google_api import calendar_id, calendar

def get_calendar(timeMin, timeMax):
    actual_events = calendar.get_events(calendar_id=calendar_id, timeMin=timeMin, timeMax=timeMax)

    time_delta = []
    for event in actual_events:
        time_delta.append({"start": event["start"]["dateTime"], "end": event["end"]["dateTime"]})

    return time_delta
