import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime

# URLs
INITIAL_URL = 'https://www.epfindia.gov.in/site_en/circulars.php'
POST_URL = 'https://www.epfindia.gov.in/site_en/get_cir_content.php'
BASE_URL = 'https://www.epfindia.gov.in/'

# Function to extract dropdown values from the initial page
def get_dropdown_values(soup):
    dropdown = soup.find('select', {'id': 'dd'})
    return [option['value'] for option in dropdown.find_all('option') if option['value']]

# Function to parse rows and append the year
def parse_rows(rows, year=''):
    parsed_rows = []
    for row in rows:
        cols = row.find_all('td')
        row_data = [col.text.strip() for col in cols]

        # Extract URLs from the 3rd and 4th <td> elements
        hindi_url = cols[2].find('a')['href'] if cols[2].find('a') else "NA"
        hindi_url = BASE_URL + hindi_url if hindi_url != "NA" else hindi_url

        english_url = cols[3].find('a')['href'] if cols[3].find('a') else "NA"
        english_url = BASE_URL + english_url if english_url != "NA" else english_url

        # Add URLs to the respective columns in row_data
        row_data[2] = hindi_url
        row_data[3] = english_url
        row_data.append(year)
        
        # Check if the last 10 characters of row_data[1] are in dd/mm/yyyy format
        if len(row_data[1]) >= 10 and row_data[1][-10:].count('/') == 2:
            try:
                date_str = row_data[1][-10:]
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                formatted_date = date_obj.strftime('%Y-%m-%d')
                row_data.append(formatted_date)
            except ValueError:
                row_data.append('Invalid Date')
        else:
            row_data.append('No Date')

        parsed_rows.append(row_data)

    return parsed_rows

# Function to convert JSON data to an Excel file
def json_to_excel(json_data, excel_file):
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet()

    # Write headers
    if json_data:
        headers = json_data[0].keys()
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Write data rows
        for row_num, item in enumerate(json_data, start=1):
            for col_num, (key, value) in enumerate(item.items()):
                worksheet.write(row_num, col_num, value)

    workbook.close()

# Fetch initial page
response = requests.get(INITIAL_URL)
response.raise_for_status()
soup = bs(response.text, 'html.parser')

# Extract headers and initial table rows
table = soup.find('table')
headers = [header.text.strip() for header in table.find_all('th')]
headers.append('Year')
headers.append('Date')

# Parse initial table rows
initial_rows = table.find_all('tr', class_='small_font')[1:]
all_circulars = parse_rows(initial_rows)

# Get the dropdown values for different years
dropdown_values = get_dropdown_values(soup)

# Fetch and parse rows for each year in the dropdown
for value in dropdown_values:
    post_data = {'yr': value}
    try:
        post_response = requests.post(POST_URL, data=post_data)
        post_response.raise_for_status()
        soup2 = bs(post_response.text, 'html.parser')
        year_rows = soup2.find_all('tr', class_='small_font')[1:]
        circulars = parse_rows(year_rows, year=value)
        all_circulars.extend(circulars)
    except requests.RequestException as e:
        print(f"Error fetching data for year {value}: {e}")

# Convert data to dictionary format
circulars_dicts = [{headers[i]: row[i] for i in range(len(headers))} for row in all_circulars]

# Write data to Excel
json_to_excel(circulars_dicts, 'circulars.xlsx')
