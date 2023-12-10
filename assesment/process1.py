from google.colab import files
uploaded = files.upload()
import pandas as pd
df = pd.read_parquet('raw_data.parquet')
print(df)
import pandas as pd
from datetime import datetime, timedelta

import pandas as pd
from datetime import timedelta

# Assuming 'df' is your DataFrame
# Convert 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Sort the DataFrame by unit and timestamp
df.sort_values(['unit', 'timestamp'], inplace=True)

# Function to determine trip number based on time difference
def get_trip_number(timestamps):
    trip_number = 0
    trip_start_time = timestamps.iloc[0]

    for timestamp in timestamps:
        if timestamp - trip_start_time > timedelta(hours=7):
            trip_start_time = timestamp
            trip_number += 1

    return trip_number
df['trip_number'] = df.groupby('unit')['timestamp'].transform(get_trip_number)

for (unit, trip), trip_data in df.groupby(['unit', 'trip_number']):
    trip_data.to_csv(f'{unit}_{trip}.csv', index=False)
!unzip MapUp-Data-Assessment-E-main.zip