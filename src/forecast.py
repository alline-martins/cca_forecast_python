from datetime import datetime
from collections import defaultdict


def summarize_forecast(weather_data):
    summaries = {}

    # Group entries by day
    group_day = group_daily_entries(weather_data)

    # Process each day
    for day, entries in group_day.items():
        morning_temperature, morning_rain, afternoon_temperature, afternoon_rain, all_temperature = split_entries_into_groups(entries)

        summary = {
            "morning_average_temperature": "Insufficient forecast data" if not morning_temperature else round(
                sum(morning_temperature) / len(morning_temperature)),
            "morning_chance_of_rain": "Insufficient forecast data" if not morning_rain else round(
                sum(morning_rain) / len(morning_rain), 2),
            "afternoon_average_temperature": "Insufficient forecast data" if not afternoon_temperature else round(
                sum(afternoon_temperature) / len(afternoon_temperature)),
            "afternoon_chance_of_rain": "Insufficient forecast data" if not afternoon_rain else round(
                sum(afternoon_rain) / len(afternoon_rain), 2),
            "high_temperature": max(all_temperature),
            "low_temperature": min(all_temperature)
        }

        # format reader-friendly date
        day_name = day.strftime("%A %B %d").replace(" 0", " ")

        summaries[day_name] = summary

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