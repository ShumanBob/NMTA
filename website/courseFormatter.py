import pandas as pd
from datetime import datetime
import os

# Get directory where this script is located
base_dir = os.path.dirname(__file__)

# Convert "HHMM-HHMM" format to "HH:MM AM/PM - HH:MM AM/PM"
def convert_time_range(time_str):
    if pd.isna(time_str) or '-' not in str(time_str):
        return ''
    try:
        start, end = time_str.split('-')
        start_time = datetime.strptime(start.strip(), "%H%M").strftime("%I:%M %p")
        end_time = datetime.strptime(end.strip(), "%H%M").strftime("%I:%M %p")
        return f"{start_time} - {end_time}"
    except ValueError:
        return ''

# Load the CSV (absolute path)
csv_path = os.path.join(base_dir, "nmt_courses_latest.csv")
df = pd.read_csv(csv_path)

# Collect formatted lines
formatted_classes = []

for _, row in df.iterrows():
    course_full = row['course_code'] if pd.notna(row['course_code']) else ''
    course_code = course_full.split('-')[0] if '-' in course_full else course_full
    dept = row['crn'] if pd.notna(row['crn']) else ''
    days = row['days'].strip().replace(' ', '') if pd.notna(row['days']) else ''
    time_range = convert_time_range(row['time'])
    title = row['title'] if pd.notna(row['title']) else ''
    credit_hours = row['credit_hours'] if 'credit_hours' in row and pd.notna(row['credit_hours']) else ''

    if not (course_code and dept and days and time_range and title and credit_hours):
        continue

    pretty_days = '/'.join(days)
    formatted_line = f"{course_code}, {dept}, {days}, {time_range}, {credit_hours}, {course_code} - {title} ({pretty_days} {time_range})"
    formatted_classes.append(formatted_line)

# Write to output file (absolute path)
output_path = os.path.join(base_dir, "classes.txt")
with open(output_path, "w") as f:
    for line in formatted_classes:
        f.write(line + "\n")

print("classes.txt has been created.")
