import requests
import pandas as pd

def get_data():
    '''
    Scrapes the SpaceX API and returns the launch and ship information for the latest launch.
    '''
    latest_url = 'https://api.spacexdata.com/v4/launches/latest'
    latest_response = requests.get(latest_url)
    latest_json = latest_response.json()
    launch_name = latest_json['name']
    launch_date = latest_json['date_utc']
    #removing the time, to leave just the date
    launch_date = launch_date.split('T')[0]
    launch_details = latest_json['details']
    ships = latest_json['ships']
    ship_name = []
    ship_type = []
    ship_port = []
    for i in range(len(ships)):
        ship_url = 'https://api.spacexdata.com/v4/ships/' + ships[i]
        ship_response = requests.get(ship_url)
        ship_json = ship_response.json()
        ship_name.append(ship_json['name'])
        ship_type.append(ship_json['type'])
        ship_port.append(ship_json['home_port'])
    #launch data specified as lists for formatting the dataframe, as they are always single entries
    launch_data = {'Name': [launch_name], 'Date': [launch_date], 'Details': [launch_details]}
    ship_data = {'Name': ship_name, 'Type': ship_type, 'Home Port': ship_port}
    return launch_data, ship_data

def main():
    '''
    Uses the data from the get_data() function and prints it as two dataframes.
    '''
    launch_data, ship_data = get_data()
    launch_df = pd.DataFrame(data = launch_data)
    ship_df = pd.DataFrame(data = ship_data)
    print(f'Launch information:\n{launch_df.to_string(index=False)}\n')
    print(f'Ship information:\n{ship_df.to_string(index=False)}')

if __name__ == "__main__":
    main()
