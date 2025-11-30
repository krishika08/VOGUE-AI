# weather_module.py
import requests

def get_weather(city_name):
    """
    Fetches temperature for a city and categorizes it into 
    Hot, Moderate, Cold, or Rainy.
    """
    try:
        # 1. Get Coordinates (Latitude & Longitude) for the City
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url).json()
        
        if 'results' not in geo_response:
            print(f"❌ City '{city_name}' not found.")
            return "Moderate", 25  # Default fallback if city is wrong
            
        lat = geo_response['results'][0]['latitude']
        lon = geo_response['results'][0]['longitude']
        
        # 2. Get Weather Data using Coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url).json()
        
        # 3. Extract Temperature and Weather Code
        current_weather = weather_response['current_weather']
        temp = current_weather['temperature']
        weather_code = current_weather['weathercode'] # Codes for rain/snow etc.
        
        # 4. Categorize the Weather
        # WMO Weather Codes: 51-67, 80-82 are Rain/Drizzle
        is_rainy = weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]

        if is_rainy:
            category = "Rainy"
        elif temp >= 30:
            category = "Hot"
        elif 20 <= temp < 30:
            category = "Moderate"
        else:
            category = "Cold"
            
        return category, temp
        
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "Moderate", 25 # Fallback

# TEST BLOCK (This only runs if you run this specific file)
if __name__ == "__main__":
    city = input("Test City: ")
    cat, t = get_weather(city)
    print(f"Result: {t}°C -> {cat}")