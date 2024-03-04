import requests
import pandas as pd

district_coordinates='district_abcd.csv'

def get_soil_properties(latitude, longitude):
    url = f"http://soil.narc.gov.np/soil/api/soildata?lat={latitude}&lon={longitude}"

    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soil_data = response.json()
            return soil_data
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


#latitude = 28.746
#longitude = 80.695
#result = get_soil_data(latitude, longitude)
#print(result)

def generate_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('soil_properties.csv', index=False)

def main():
    district_data =pd.read_csv(district_coordinates)

    soil_properties_data = []

    for index, row in district_data.iterrows():
         properties = get_soil_properties(row['lat'], row['lon'])
         if properties:
            data = {
                'location_name': row['DISTRICT'],
                'latitude': row['lat'],
                'longitude': row['lon'],
                'totalNitrogen': properties['totalNitrogen'],
                'p2o5': properties['p2o5'],
                'ph': properties['ph'],
                #'parentsoil': properties['parentsoil'],
                #'sand': properties['sand'],
                #'boron': properties['boron'],
                #'clay': properties['clay'],
                'organicMatter': properties['organicMatter'],
        
            }
            soil_properties_data.append(data)

    generate_csv(soil_properties_data)

if __name__ == '__main__':
    main()
    





