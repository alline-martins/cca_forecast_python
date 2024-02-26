from datetime import datetime
from collections import defaultdict

def summarize_forecast(weather_data):
    summaries = {}

    # Group entries by day
    group_day = group_daily_entries(weather_data)

    # Process each day
    for day, entries in group_day.items():
        morning_temperature, morning_rain, afternoon_temperature, afternoon_rain, all_temperature = split_entries_into_groups(entries)

        summary = Summary(
            morning_temperature=morning_temperature,
            morning_rain=morning_rain,
            afternoon_temperature=afternoon_temperature,
            afternoon_rain=afternoon_rain,
            all_temperature=all_temperature
        )
        # format reader-friendly date
        day_name = day.strftime("%A %B %d").replace(" 0", " ")

        summaries[day_name] = summary.get_summary()

    return summaries

def split_entries_into_groups(entries):
    morning_temperature, morning_rain, afternoon_temperature, afternoon_rain = [], [], [], []
    all_temperature = [entry["average_temperature"] for entry in entries]

    for entry in entries:
        entry_time = datetime.fromisoformat(entry["date_time"].replace('Z', '+00:00'))
            # collect morning period entries
        if 6 <= entry_time.hour < 12:
            morning_temperature.append(entry["average_temperature"])
            morning_rain.append(entry["probability_of_rain"])
            # collection afternoon period entries
        elif 12 <= entry_time.hour < 18:
            afternoon_temperature.append(entry["average_temperature"])
            afternoon_rain.append(entry["probability_of_rain"])
    return morning_temperature,morning_rain,afternoon_temperature,afternoon_rain,all_temperature

def group_daily_entries(weather_data):
    group_day = defaultdict(list)

    for row in weather_data:
        entry_time = datetime.fromisoformat(row["date_time"].replace('Z', '+00:00'))
        group_day[entry_time.date()].append(row)

    return group_day



class Summary():
    def __init__(self, morning_temperature, morning_rain, afternoon_temperature, afternoon_rain, all_temperature):
        self.morning_temperature = morning_temperature
        self.morning_rain = morning_rain
        self.afternoon_temperature = afternoon_temperature
        self.afternoon_rain = afternoon_rain
        self.all_temperature = all_temperature

    def get_summary(self):
        
        summary = {
            "morning_average_temperature": create_message(self.morning_temperature),
            "morning_chance_of_rain": create_message(self.morning_rain, 2),
            "afternoon_average_temperature": create_message(self.afternoon_temperature),
            "afternoon_chance_of_rain": create_message(self.afternoon_rain, 2),
            "high_temperature": max(self.all_temperature),
            "low_temperature": min(self.all_temperature)
        }

        return summary



def create_message(weather_list, decimals=0):
    return "Insufficient forecast data" if not weather_list else calculate_mean(weather_list, decimals)

def calculate_mean(a_list, decimals):
    return round(
                sum(a_list) / len(a_list), decimals)
