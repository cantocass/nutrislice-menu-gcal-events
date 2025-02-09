from datetime import datetime
from create_events import create_gcal_event
from check_creds import check_calendar_credentials
from nutrislice import fetch_menu_data_for_week_from_date, MenuEvent
from typing import List

if __name__ == '__main__':
    # check credentials
    check_calendar_credentials()
    # get date
    # Date for the week to fetch (start of the week)
    start_date = datetime.today()  # Update as needed
    year, month, day = start_date.year, start_date.month, start_date.day

    # get menu for week with date
    events: List[MenuEvent] = fetch_menu_data_for_week_from_date(year, month, day)

    # create one event per menu item
    for event in events:
        event: MenuEvent
        create_gcal_event(event.name, event.description, event.start, event.end)