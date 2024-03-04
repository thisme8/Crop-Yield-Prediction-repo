

import os
import requests
import csv

locations = [(29.0396, 81.2519), (5, 10)]

output = r""
combined_data = []

base_url = r"https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=T2M,RH2M,WS10M,PRECTOTCORR&community=SB&longitude={longitude}&latitude={latitude}&format=CSV&start=2020&end=2022"

for latitude, longitude in locations:
    api_request_url = base_url.format(longitude=longitude, latitude=latitude)

    response = requests.get(url=api_request_url, verify=True, timeout=30.00)

    filename = f"data_{latitude}_{longitude}.csv"

    filepath = os.path.join(output, filename)
    with open(filepath, 'wb') as file_object:
        file_object.write(response.content)

    # Extract data lines skipping header lines
    data_lines = response.content.decode('utf-8').splitlines()
    for idx, line in enumerate(data_lines):
        if line.strip() == "-END HEADER-":
            data = data_lines[idx + 1:]  # Skip header lines
            data = [[latitude, longitude] + line.split(",") for line in data]
            combined_data.extend(data)
            break

filename = "combined_data.csv"
filepath = os.path.join(output, filename)
with open(filepath, 'w', newline='') as combined_file:
    writer = csv.writer(combined_file)
    writer.writerow(["Latitude", "Longitude", "Month", "T2M", "RH2M", "WS10M", "PRECTOTCORR"])
    writer.writerows(combined_data)

print("Data downloaded and combined successfully.")
