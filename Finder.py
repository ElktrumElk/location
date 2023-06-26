import requests
import folium
from socket import gethostbyname
from time import sleep

def get_location(ip_address):
    access_key = "88408889e294331ceefa9c879ed51159"  # Replace with your own access key
    url = f"http://api.ipstack.com/{ip_address}?access_key={access_key}"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")
        return None

def show_loading_animation():
    animation = "|/-\\"
    for _ in range(5):
        for char in animation:
            print(f"\033[96mProcessing... {char}\033[0m", end="\r")
            sleep(0.1)

# Prompt for user choice
choice = input("Choose an option:\n1. Search by domain or URL\n2. Search by IP address\nEnter your choice: ")

if choice == "1":
    domain = input("Enter the domain or URL to search for IP address information: ")
    try:
        ip_address = gethostbyname(domain)
    except Exception as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")
        ip_address = None
elif choice == "2":
    ip_address = input("Enter the IP address to search for information: ")
else:
    print("\033[91mInvalid choice. Exiting...\033[0m")
    exit()

if ip_address is not None:
    show_loading_animation()
    location_data = get_location(ip_address)

    if location_data is not None:
        # Extract relevant information
        country = location_data["country_name"]
        region = location_data["region_name"]
        city = location_data["city"]
        postal = location_data["zip"]
        latitude = location_data["latitude"]
        longitude = location_data["longitude"]

        # Print the information with color
        print("\033[92m--- IP Address Information ---\033[0m")
        print(f"\033[96mDomain/URL: {domain}\033[0m" if choice == "1" else f"\033[96mIP Address: {ip_address}\033[0m")
        print(f"\033[92mCountry: {country}")
        print(f"Region: {region}")
        print(f"City: {city}")
        print(f"Postal Code: {postal}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}\033[0m")

        # Create a map centered around the location
        location_map = folium.Map(location=[latitude, longitude], zoom_start=10)
        folium.Marker([latitude, longitude], popup=city).add_to(location_map)

        # Save the map to an HTML file
        location_map.save("location_map.html")
        print("\033[92mLocation map saved as location_map.html\033[0m")
