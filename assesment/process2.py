
pip install requests python-dotenv
with open('.env', 'w') as f:
    f.write("TOLLGURU_API_KEY=your_api_key\n")
    f.write("TOLLGURU_API_URL=https://apis.tollguru.com\n")
from dotenv import load_dotenv
load_dotenv()
import os
print(os.getenv('TOLLGURU_API_KEY'))
print(os.getenv('TOLLGURU_API_URL'))
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# TollGuru API key and URL
TOLLGURU_API_KEY = os.getenv('TOLLGURU_API_KEY')
TOLLGURU_API_URL = os.getenv('TOLLGURU_API_URL')

# API parameters
API_PARAMETERS = {'vehicleType': '5AxlesTruck', 'mapProvider': 'osrm'}

# Function to upload a CSV file to TollGuru API
def upload_to_tollguru(file_path):
    if not TOLLGURU_API_URL:
        raise ValueError("TOLLGURU_API_URL is not defined in the environment variables.")

    url = f'{TOLLGURU_API_URL}/toll/v2/gps-tracks-csv-upload'
    headers = {'x-api-key': TOLLGURU_API_KEY, 'Content-Type': 'text/csv'}

    with open(file_path, 'rb') as file:
        response = requests.post(url, data=file, headers=headers)

    return response.json()

def main():
    # Assuming you have a list of CSV files obtained from Process1
    csv_files = [
        '/content/evaluation_data/output/1000_10.csv',
        '/content/evaluation_data/output/2000_6.csv',  # Add more file paths as needed
        # ...
    ]

    # Create a ThreadPoolExecutor for concurrent uploads
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Concurrently upload CSV files to TollGuru API
        responses = list(executor.map(upload_to_tollguru, csv_files))

    # Save JSON responses to files with the same names
    for file_path, response in zip(csv_files, responses):
        json_file_path = f'{os.path.splitext(file_path)[0]}.json'
        with open(json_file_path, 'w') as json_file:
            json_file.write(str(response))

if __name__ == "__main__":
    main()


