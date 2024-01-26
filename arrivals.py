import requests
import constants

def get_station_id(station_name):
    api_key = constants.TFL_API_KEY

    endpoint = 'https://api.tfl.gov.uk/Place/Search'

    params = {
        'app_key': api_key,
        'query': station_name,
        'categories': 'Station',
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        results = response.json()

        if results and 'id' in results[0]:
            return results[0]['id']
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def get_next_departures(station_id, num_departures=10):
    api_key = constants.TFL_API_KEY

    endpoint = f'https://api.tfl.gov.uk/StopPoint/{station_id}/arrivals'

    params = {
        'app_key': api_key,
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        departures = response.json()
        return departures[:num_departures]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def main():
    station_name = 'Denmark Hill'
    station_id = '910GDENMRKH'

    if station_id:
        print(f"Station ID for {station_name}: {station_id}")
        departures = get_next_departures(station_id)
        
        if departures:
            print("Next 10 Departures:")
            for departure in departures:
                line_name = departure.get('lineName', 'N/A')
                towards = departure.get('destinationName', 'N/A')
                expected_arrival = departure.get('expectedArrival', 'N/A')

                print(f"Line: {line_name} - Towards: {towards} - Expected Arrival: {expected_arrival}")
    else:
        print(f"Unable to retrieve Station ID for {station_name}")

if __name__ == "__main__":
    main()
