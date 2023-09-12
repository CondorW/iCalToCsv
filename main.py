from icalendar import Calendar
import csv
import os
from tkinter import filedialog
from tkinter import Tk

# Sanitize non-ASCII characters
def sanitize_string(input_str):
    return ''.join(char if ord(char) < 128 else ' ' for char in input_str)

# Initialize Tkinter root window (it won't be shown)
root = Tk()
root.withdraw()

# Step 1: Prompt user to select an iCal file
file_path = filedialog.askopenfilename(filetypes=[("iCalendar files", "*.ics")])
if not file_path:
    print("No file selected. Exiting.")
    exit()

# Step 2: Read the iCal file
with open(file_path, 'rb') as f:
    cal = Calendar.from_ical(f.read())

# Step 3: Prepare to extract relevant fields
events = []
for component in cal.walk():
    if component.name == "VEVENT":
        summary_str = sanitize_string(str(component.get('summary')))
        event['SUMMARY'] = summary_str[:30]  # Only take the first 30 characters
        event['START'] = sanitize_string(str(component.get('dtstart').dt))
        event['END'] = sanitize_string(str(component.get('dtend').dt))
        event['LOCATION'] = sanitize_string(str(component.get('location')))
        events.append(event)

# Step 4: Write to CSV
output_path = os.path.join(os.path.dirname(file_path), "events.csv")
keys = ['SUMMARY', 'START', 'END', 'LOCATION']
with open(output_path, 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys, delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(events)

print(f"CSV file has been saved at {output_path}")
