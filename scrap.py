import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_earthquake_data():
    url = 'http://www.koeri.boun.edu.tr/scripts/sondepremler.asp'

    # Make a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the only <pre> tag on the page
        pre_tag = soup.find('pre')

        if pre_tag:
            # Extract text content within the <pre> tag
            pre_text_content = pre_tag.get_text()

            # Skip the first 7 lines (header)
            lines = pre_text_content.split('\n')[7:]
            cleaned_text = '\n'.join(lines)

            # Initialize lists to store attributes
            new_events = []

            # Loop through each line and extract attributes
            for line in lines:
                attributes = line.split()

                # Check if the line has the expected number of elements
                if len(attributes) >= 10:
                    date_time_str = attributes[0] + ' ' + attributes[1]
                    date_time = datetime.strptime(date_time_str, '%Y.%m.%d %H:%M:%S')

                    # Check if the date and time already exist in the CSV
                    if not is_event_exists_in_csv(date_time):
                        latitude = float(attributes[2])
                        longitude = float(attributes[3])
                        depth = float(attributes[4])
                        magnitude = float(attributes[6])
                        location = ' '.join(attributes[8:-1])  # Include locations from index 7 to the end

                        # Append values to the new_events list
                        new_events.append((date_time_str, latitude, longitude, depth, magnitude, location))

            if new_events:
                # Print the extracted values for testing
                print("\nNew Events:")
                print(new_events)

                # Write new data to CSV file
                write_to_csv(new_events)
            else:
                print("No new events found.")
        else:
            print("No <pre> tag found on the page.")
    else:
        print(f"Failed to fetch the content. Status code: {response.status_code}")

def is_event_exists_in_csv(date_time):
    # Check if the event already exists in the CSV file
    csv_file = 'earthquake_data.csv'

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip the header
            next(reader, None)
            for row in reader:
                row_date_time = datetime.strptime(row[0], '%Y.%m.%d %H:%M:%S')
                if row_date_time == date_time:
                    return True
    except FileNotFoundError:
        pass  # File not found, indicating no existing data

    return False

# def write_to_csv(new_events):
#     # Define CSV file name
#     csv_file = 'earthquake_data.csv'

#     # Write new data to CSV file
#     with open(csv_file, 'a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)

#         # Write data
#         writer.writerows(new_events)

#     print(f"{len(new_events)} new events appended to {csv_file}.")

def write_to_csv(new_events):
    # Define CSV file name
    csv_file = 'earthquake_data.csv'

    # Read existing data from CSV file
    existing_data = []
    is_file_empty = True

    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Read existing data including the header
            existing_data = list(reader)
            if len(existing_data) > 0:
                is_file_empty = False
    except FileNotFoundError:
        pass  # File not found, indicating no existing data

    # Combine new events with existing data
    combined_data = existing_data[:1] + new_events + existing_data[1:]

    # Write combined data to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header only if the file is empty
        if is_file_empty:
            writer.writerow(['Date and Time', 'Latitude', 'Longitude', 'Depth', 'Magnitude', 'Location'])

        # Write combined data
        writer.writerows(combined_data)

    print(f"{len(new_events)} new events inserted below the header in {csv_file}.")

# Run the scraping and writing functions
scrape_earthquake_data()



# @echo off
# set script_path=C:\path\to\your\script.py
# set python_executable=C:\path\to\python\executable\python.exe

# "%python_executable%" "%script_path%"




