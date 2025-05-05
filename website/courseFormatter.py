import pandas as pd
from datetime import datetime
import os

# get directory of this file
base_dir = os.path.dirname(__file__)

# convert time from HHMM-HHMM to HH:MM AM/PM - HH:MM AM/PM
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

# get absolute path to the CSV file
csv_path = os.path.join(base_dir, "data/nmt_courses_latest.csv")
# load csv file into pandas dataframe
df = pd.read_csv(csv_path)

# list to hold classes entries
formatted_classes = []

# iterate through dataframe rows
for _, row in df.iterrows():
    course_full = row['course_code'] if pd.notna(row['course_code']) else ''
    course_code = course_full.split('-')[0] if '-' in course_full else course_full
    crn = row['crn'] if pd.notna(row['crn']) else ''
    days = row['days'].strip().replace(' ', '') if pd.notna(row['days']) else ''
    time_range = convert_time_range(row['time'])
    title = row['title'] if pd.notna(row['title']) else ''
    credit_hours = row['credit_hours'] if pd.notna(row['credit_hours']) else ''
    seats = row['seats'] if pd.notna(row['seats']) else ''
    instructor = row['instructor'] if pd.notna(row['instructor']) else ''
    location = row['location'] if pd.notna(row['location']) else ''
    course_type = row['type'] if pd.notna(row['type']) else ''
    term = row['term'] if pd.notna(row['term']) else ''
    subject = row['subject'] if pd.notna(row['subject']) else ''
    campus = row['campus'] if pd.notna(row['campus']) else ''
    date_range = row['date_range'] if pd.notna(row['date_range']) else ''
    limit = row['limit'] if pd.notna(row['limit']) else ''
    enrolled = row['enrolled'] if pd.notna(row['enrolled']) else ''
    waitlist = row['waitlist'] if pd.notna(row['waitlist']) else ''
    fees = row['fees'] if pd.notna(row['fees']) else ''
    bookstore_link = row['bookstore_link'] if pd.notna(row['bookstore_link']) else ''

    # skip if entries are incomplete
    if not (course_code and crn and days and time_range and title and credit_hours):
        continue
    # convert day strings from MWF to M/W/F
    pretty_days = '/'.join(days)

    # construct formatted string for course
    formatted_line = (
        f"{course_code}, {crn}, {days}, {time_range}, {credit_hours}, {seats}, "
        f"{course_code} - {title} ({pretty_days} {time_range}) | "
        f"Instructor: {instructor}, Location: {location}, Type: {course_type}, "
        f"Term: {term}, Subject: {subject}, Campus: {campus}, Date Range: {date_range}, "
        f"Limit: {limit}, Enrolled: {enrolled}, Waitlist: {waitlist}, Fees: {fees}, "
        f"Bookstore: {bookstore_link}"
    )
    # add string to list
    formatted_classes.append(formatted_line)

# write file to output directory
output_path = os.path.join(base_dir, "data/classes.txt")
with open(output_path, "w") as f:
    for line in formatted_classes:
        f.write(line + "\n")
