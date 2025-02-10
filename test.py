import requests

url = "https://sport-highlights-api.p.rapidapi.com/football/highlights/8780"

headers = {
    "x-rapidapi-host": "sport-highlights-api.p.rapidapi.com",
    "x-rapidapi-key": "2111b15adcmsh11ffa193ecdd7b8p10ece2jsn0b1449c39037"
}

try:
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print("Successfully retrieved data:")
        print(data)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
