from datetime import datetime

current_data = datetime.strptime('2024-08-14 00:00', '%Y-%m-%d %H:%M')
year = current_data.year
month = current_data.month
day = current_data.day
hours = current_data.minute

print(hours)