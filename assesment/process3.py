import os
import json
import csv

def process_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8', errors='replace') as file:
        data = json.load(file)

    # Extract relevant data from the JSON file
    unit = data.get('unit', '')
    trip_id = os.path.splitext(os.path.basename(json_file))[0]
    toll_data = data.get('tollData', [])

    # Transform data into CSV format
    csv_data = []
    for toll_info in toll_data:
        row = {
            'unit': unit,
            'trip_id': trip_id,
            'toll_loc_id_start': toll_info.get('startToll', {}).get('tollID', ''),
            'toll_loc_id_end': toll_info.get('endToll', {}).get('tollID', ''),
            'toll_loc_name_start': toll_info.get('startToll', {}).get('tollName', ''),
            'toll_loc_name_end': toll_info.get('endToll', {}).get('tollName', ''),
            'toll_system_type': toll_info.get('tollSystemType', ''),
            'entry_time': toll_info.get('entryTime', ''),
            'exit_time': toll_info.get('exitTime', ''),
            'tag_cost': toll_info.get('tagCost', ''),
            'cash_cost': toll_info.get('cashCost', ''),
            'license_plate_cost': toll_info.get('licensePlateCost', ''),
        }
        csv_data.append(row)

    return csv_data

def process_json_files(input_dir, output_file):
    csv_header = [
        'unit', 'trip_id', 'toll_loc_id_start', 'toll_loc_id_end',
        'toll_loc_name_start', 'toll_loc_name_end', 'toll_system_type',
        'entry_time', 'exit_time', 'tag_cost', 'cash_cost', 'license_plate_cost'
    ]

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        writer.writeheader()

        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.json'):
                    json_file_path = os.path.join(root, file)
                    csv_data = process_json_file(json_file_path)
                    writer.writerows(csv_data)

if __name__ == "__main__":
    input_directory = '/content/evaluation_data/output/'
    output_csv_file = '/content/evaluation_data/output/transformed_data.csv'

    process_json_files(input_directory, output_csv_file)