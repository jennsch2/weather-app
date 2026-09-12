# Weather App

A desktop weather application built with Python and Tkinter.

## Features

* 🌤️ Current weather information
* 📍 Automatic location detection
* 🔍 Search weather by city
* 🌡️ Temperature and feels-like temperature
* 💧 Humidity
* 💨 Wind speed
* 🌧️ Precipitation
* ☁️ Cloud cover
* 🌅 Sunrise and sunset information
* 🕐 24-hour forecast
* 📅 7-day forecast
* 🌍 Automatic timezone detection
* 🇷🇺 Russian and 🇬🇧 English languages
* ⚙️ Language switching in settings

## Technologies

* Python
* Tkinter
* Requests
* Open-Meteo API
* OpenStreetMap Nominatim
* Windows Geolocation API

## Installation

Clone the repository:

```bash
git clone https://github.com/jennsch2/weather-app.git
```

Open the project folder and install the required libraries:

```bash
pip install requests winrt-runtime winrt-Windows.Devices.Geolocation
```

Run the application:

```bash
python main.py
```

## API

Weather data is provided by the Open-Meteo API.

Location data is provided by OpenStreetMap Nominatim.

## About

This is one of my first Python desktop applications.

The project was created to practice Python, Tkinter, APIs, JSON, threading, and working with external services.
