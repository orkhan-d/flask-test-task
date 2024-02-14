import asyncio
import os

import python_weather

async def get_weather_in_city(city: str):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)
        return weather.current.temperature

if __name__=='__main__':
    print(asyncio.run(get_weather_in_city('a')))