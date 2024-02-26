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
