import requests
from datetime import datetime
import os
from typing import List
from dotenv import load_dotenv
import json

load_dotenv()


class MenuEvent:
    def __init__(self, name, description, start, end):
        self.name = name
        self.description = description
        self.start = start
        self.end = end

def read_from_file():
    with open('menu-response.json') as f:
        return json.load(f)

# Function to fetch and process menu data from the Nutrislice API
def fetch_menu_data_for_week_from_date(year, month, day) -> List[MenuEvent]:
    # menu_data = read_from_file()

    url = os.getenv('BASE_API_URL') + f"/{year}/{month:02d}/{day:02d}?format=json"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch menu data. HTTP Status Code: {response.status_code}")
        return []

    calendar_events = []

    # Loop through days in the week and extract menu data
    for day_data in menu_data.get("days", []):
        date = day_data.get("date")
        menu_info = day_data.get("menu_items", [])

        # Skip processing if no menu info is available (e.g., weekends)
        if not menu_info:
            print(f"Skipping {date}: No menu information available.")
            continue

        # Group menu items by category
        entrees = []
        sides = []
        for index, menu_item in enumerate(menu_info):
            food = menu_item.get("food")
            if not food:  # Skip if "food" is None
                continue

            food_name = food.get("name", "Unknown Item")
            category = menu_item.get("category", "Unknown Category")

            if "entree" in category.lower():
                entrees.append(food_name)
            elif index >= 1 & (food_name not in entrees):
                previous_text = menu_info[index - 1].get("text")
                if ("Option" in previous_text) & ("Side" not in previous_text):
                    entrees.append(food_name)
                elif "Side" not in previous_text:
                    sides.append(food_name)

        # Create a single event for the day's menu
        if entrees:
            event_name = " or ".join(entrees)  # Join entrée options with "or"
        else:
            event_name = "Lunch Menu"

        event_description = ", ".join(sides) if sides else "No sides available."

        # Assume lunch starts at 12:00 PM
        start_datetime = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%dT12:00:00")
        end_datetime = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%dT12:30:00")  # 30 minutes duration

        menu = MenuEvent(event_name, event_description, start_datetime, end_datetime)
        calendar_events.append(menu)

    return calendar_events


# Main execution
if __name__ == "__main__":

    # Date for the week to fetch (start of the week)
    start_date = datetime.today().date()  # Update as needed
    year, month, day = start_date.year, start_date.month, start_date.day

    # Fetch and display the menu URLs
    menu_events = fetch_menu_data_for_week_from_date(year, month, day)
    for event in menu_events:
        event: MenuEvent
        print(event.name)
        print(event.description)
        print("-----------")
