import requests
import sensetive_info

API_KEY = sensetive_info.WEATHER_API_KEY

def get_weather():
    location = "Athens"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        
        # Extract weather details
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        wind_direction = data['wind'].get('deg', 'N/A')  # Some responses might not include wind direction

        # Format the weather information
        weather_info = (
            f"The weather in {location} is currently {weather_description} with a temperature of {temperature}°C. "
            f"It feels like {feels_like}°C. The humidity is {humidity}%, pressure is {pressure} hPa, "
            f"and the wind is blowing at {wind_speed} m/s from {wind_direction} degrees."
        )
        return weather_info
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return "Sorry, I couldn't retrieve the weather information at this time due to an HTTP error."
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return "Sorry, I couldn't retrieve the weather information at this time due to a request error."
    except KeyError as key_err:
        print(f"Key error: {key_err} - The location may not be valid or the API response format might have changed.")
        return "Sorry, I couldn't retrieve the weather information at this time due to a data parsing error."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Sorry, I couldn't retrieve the weather information at this time due to an unexpected error."

if __name__ == "__main__":
    print(get_weather())
