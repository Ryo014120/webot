import os
import discord
import requests
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('OPENWEATHER_API_KEY')

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!weather'):
        city = message.content.split(' ', 1)[1]
        weather_data = get_weather(city)
        await message.channel.send(weather_data)

def get_weather(city):
    url = 'https://home.openweathermap.org/api_keys'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    weather_json = response.json()

    if response.status_code == 200:
        temperature = weather_json['main']['temp']
        description = weather_json['weather'][0]['description']
        return f'The current temperature in {city} is {temperature}°C with {description}.'
    else:
        return 'Failed to fetch weather data.'

client.run(TOKEN)