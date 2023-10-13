# deaths_analysis.py
import re

def parse_gedcom(file_path):
    parsed_data = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        individuals = [entry for entry in ''.join(lines).split("0 @")[1:] if "@ INDI" in entry]
        for individual in individuals:
            indi_data = {}
            for i, line in enumerate(individual.splitlines()):
                tokens = line.split(' ')
                if len(tokens) < 3:
                    continue
                tag, data = tokens[1], ' '.join(tokens[2:])
                if tag == 'NAME':
                    indi_data['name'] = data.replace("/", "")
                elif tag == 'DATE':
                    prev_line_tag = individual.splitlines()[i-1].split(' ')[1]
                    if prev_line_tag == 'BIRT':
                        indi_data['birth_date'] = data
                    elif prev_line_tag == 'DEAT':
                        indi_data['death_date'] = data
            parsed_data.append(indi_data)
    return parsed_data

from datetime import datetime

def get_input_details():
    """Get user input details."""
    while True:
        option = input("Search by person's name or date range? (Enter '(P)erson' or '(D)ate'): ").strip().lower()
        if option == 'p':
            name = input("Enter the person's full name: ").strip()
            if not name:
                print("Please provide a valid name.")
                continue
            return {'type': 'person', 'name': name}

        elif option == 'd':
            start_date = input("Enter the start date (e.g. '12 JAN 2000'): ").strip()
            end_date = input("Enter the end date (e.g. '12 JAN 2010'): ").strip()
            if not start_date or not end_date:
                print("Both start and end dates are required.")
                continue
            return {'type': 'date', 'start_date': start_date, 'end_date': end_date}

        else:
            print("Invalid choice. Please enter either 'person' or 'date'.")
            continue

def extract_year_from_invalid_date(date_string):
    """Try to extract a year from the given invalid date string."""
    # Use regex to find a 4-digit number that looks like a year
    match = re.search(r'(\d{4})', date_string)
    return int(match.group(1)) if match else None

def convert_to_date(date_string):
    """Converts various GEDCOM date formats to a date object."""
    
    # Simplify and clean the date string
    date_string = date_string.strip().replace('.', '').replace(',', '').upper()
    
    # Map month names to their abbreviations
    month_map = {
        "JANUARY": "JAN",
        "FEBRUARY": "FEB",
        "MARCH": "MAR",
        "APRIL": "APR",
        "MAY": "MAY",
        "JUNE": "JUN",
        "JULY": "JUL",
        "AUGUST": "AUG",
        "SEPTEMBER": "SEP",
        "OCTOBER": "OCT",
        "NOVEMBER": "NOV",
        "DECEMBER": "DEC"
    }
    
    # Replace full month names with abbreviations
    for full_month, abbrev_month in month_map.items():
        date_string = date_string.replace(full_month, abbrev_month)
    
    # Define common date formats to try parsing
    date_formats = [
        "%d %b %Y",  # 14 FEB 1879
        "%b %Y",    # JAN 1983
        "%Y",       # 1904
        "%d %Y",    # 21 1995 (we'll handle it for 1970-2023)
        "%Y-%m-%d", # For standard date format, e.g. "1970-01-01"
        # Add more formats if needed
    ]
    
    # Only for years between 1970 and 2023
    current_year = datetime.now().year
    if date_string.isdigit() and 1900 <= int(date_string) <= current_year:
        return datetime.strptime(date_string, "%Y").date()
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt).date()
        except ValueError:
            continue
            
    # If none of the formats match
    potential_year = extract_year_from_invalid_date(date_string)
    if potential_year:
        return datetime(potential_year, 1, 1).date()  # Use January 1st of the extracted year

    print(f"Invalid date format: {date_string}")
    return None



def get_deaths_within_range(parsed_data, start_date, end_date):
    start_date_obj = convert_to_date(start_date)
    end_date_obj = convert_to_date(end_date)
    if not start_date_obj or not end_date_obj:
        return []

    deaths_within_range = []
    for person in parsed_data:
        death_date = person.get('death_date', None)
        if death_date:
            death_date_obj = convert_to_date(death_date)
            # Adjusted to check if death_date_obj exists before comparison
            if death_date_obj and start_date_obj <= death_date_obj <= end_date_obj:
                deaths_within_range.append(person)

    return deaths_within_range

import tkinter as tk
from tkinter import filedialog

def select_gedcom_file():
    """Open a file browser and return the selected GEDCOM file path."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select your GEDCOM file",
                                           filetypes=[("GEDCOM files", "*.ged"), ("All files", "*.*")])
    return file_path

def main():
    # gedcom_path = input("Please enter the path to your GEDCOM file: ")
    gedcom_path = select_gedcom_file()
    if not gedcom_path:  # If the user cancels the file selection
        print("No file selected. Exiting.")
        return
    
    parsed_data = parse_gedcom(gedcom_path)
    
    user_details = get_input_details()

    if user_details['type'] == 'person':
        name = user_details['name']
        person = next((p for p in parsed_data if name.lower() in p['name'].lower()), None)
        if not person:
            print("Person not found!")
            return

        start_date = person.get('birth_date')
        if not start_date:
            start_date = input(f"{name} doesn't have a birth date. Please provide a start date (e.g. '12 JAN 2000'): ")

        end_date = person.get('death_date')
        if not end_date:
            end_date = input(f"{name} doesn't have a death date. Please provide an end date (e.g. '12 JAN 2010'): ")

    else: # user_details['type'] == 'date'
        start_date = user_details['start_date']
        end_date = user_details['end_date']

    deaths = get_deaths_within_range(parsed_data, start_date, end_date)
    # Sort the deaths list chronologically by death date
    deaths_sorted = sorted(deaths, key=lambda x: convert_to_date(x.get('death_date', '')))

    if deaths_sorted:
        print(f"\nPeople who died between {start_date} and {end_date}:")
        for d in deaths_sorted:
            print(f"Name: {d['name']}, Death Date: {d.get('death_date', 'N/A')}")
    else:
        print(f"No deaths found between {start_date} and {end_date}.")

if __name__ == "__main__":
    main()
