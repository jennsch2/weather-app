import tkinter as tk
import threading
import requests
import asyncio
import json
import os

from datetime import datetime
from zoneinfo import ZoneInfo
from winrt.windows.devices.geolocation import Geolocator

LANGUAGE_FILE = "language.json"


def choose_language():
    selected_language = None

    def set_language(language):
        nonlocal selected_language
        selected_language = language
        language_window.destroy()

    if os.path.exists(LANGUAGE_FILE):
        try:
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            language = data.get("language")

            if language in ("ru", "en"):
                return language

        except (json.JSONDecodeError, OSError):
            pass

    language_window = tk.Tk()
    language_window.title("Choose language")
    language_window.geometry("350x180")
    language_window.resizable(False, False)

    title_label = tk.Label(
        language_window,
        text="Choose language / Выберите язык",
        font=("Arial", 14, "bold")
    )
    title_label.pack(pady=25)

    buttons_frame = tk.Frame(language_window)
    buttons_frame.pack()

    russian_button = tk.Button(
        buttons_frame,
        text="🇷🇺 Русский",
        font=("Arial", 11, "bold"),
        width=12,
        command=lambda: set_language("ru")
    )
    russian_button.pack(side="left", padx=5)

    english_button = tk.Button(
        buttons_frame,
        text="🇬🇧 English",
        font=("Arial", 11, "bold"),
        width=12,
        command=lambda: set_language("en")
    )
    english_button.pack(side="left", padx=5)

    language_window.mainloop()

    with open(LANGUAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"language": selected_language},
            file,
            ensure_ascii=False,
            indent=4
        )

    return selected_language


language = choose_language()

translations = {
    "ru": {
        "app_title": "Прогноз погоды",
        "my_location": "📍 Моё местоположение",
        "search": "🔍 Поиск",
        "getting_location": "Получение местоположения...",
        "getting_weather": "Получение погоды...",
        "update": "🔄 Обновить",
        "hourly_forecast": "Почасовой прогноз",
        "daily_forecast": "Прогноз на 7 дней",
        "weather_details": "🌡️ Детали погоды",
        "sun_information": "🌅 Информация о солнце",
        "feels_like": "По ощущениям:",
        "pressure": "Давление:",
        "cloud_cover": "Облачность:",
        "precipitation": "Осадки:",
        "sunrise": "Восход:",
        "sunset": "Закат:",
        "day_length": "Длительность дня:",
        "temperature": "Температура:",
        "humidity": "Влажность:",
        "wind": "Ветер:",
        "searching": "Поиск...",
        "enter_city": "Введите город",
        "network_error": "Ошибка сети",
        "city_not_found": "Город не найден",
        "failed_location": "Не удалось получить местоположение",
        "invalid_location": "Некорректные данные местоположения",
        "failed_weather": "Не удалось получить погоду...",
        "invalid_weather": "Некорректные данные о погоде",
        "clear_sky": "Ясное небо",
        "partly_cloudy": "Переменная облачность",
        "overcast": "Пасмурно",
        "fog": "Туман",
        "drizzle": "Морось",
        "rain": "Дождь",
        "snow": "Снег",
        "rain_showers": "Ливень",
        "snow_showers": "Снегопад",
        "thunderstorm": "Гроза",
        "unknown": "Неизвестно",
        "rain_short": "Дождь",
        "uv": "UV",
        "updating": "Обновление...",
        "getting_sun_information": "Получение информации о солнце...",
        "monday": "Понедельник",
        "tuesday": "Вторник",
        "wednesday": "Среда",
        "thursday": "Четверг",
        "friday": "Пятница",
        "saturday": "Суббота",
        "sunday": "Воскресенье",
        "settings": "⚙️ Настройки",
        "language": "Язык",
        "hours": "ч",
        "minutes": "мин",
    },

    "en": {
        "app_title": "Weather App",
        "my_location": "📍 My Location",
        "search": "🔍 Search",
        "getting_location": "Getting location...",
        "getting_weather": "Getting weather...",
        "update": "🔄 Update",
        "hourly_forecast": "Hourly Forecast",
        "daily_forecast": "7-Day Forecast",
        "weather_details": "🌡️ Weather Details",
        "sun_information": "🌅 Sun Information",
        "feels_like": "Feels like:",
        "pressure": "Pressure:",
        "cloud_cover": "Cloud cover:",
        "precipitation": "Precipitation:",
        "sunrise": "Sunrise:",
        "sunset": "Sunset:",
        "day_length": "Day length:",
        "temperature": "Temperature:",
        "humidity": "Humidity:",
        "wind": "Wind:",
        "searching": "Searching...",
        "enter_city": "Enter a city",
        "network_error": "Network Error",
        "city_not_found": "City not found",
        "failed_location": "Failed to get location",
        "invalid_location": "Invalid location data",
        "failed_weather": "Failed to get weather...",
        "invalid_weather": "Invalid weather data",
        "clear_sky": "Clear sky",
        "partly_cloudy": "Partly cloudy",
        "overcast": "Overcast",
        "fog": "Fog",
        "drizzle": "Drizzle",
        "rain": "Rain",
        "snow": "Snow",
        "rain_showers": "Rain showers",
        "snow_showers": "Snow showers",
        "thunderstorm": "Thunderstorm",
        "unknown": "Unknown",
        "rain_short": "Rain",
        "uv": "UV",
        "updating": "Updating...",
        "getting_sun_information": "Getting sun information...",
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",
        "settings": "⚙️ Settings",
        "language": "Language",
        "hours": "h",
        "minutes": "min",
    }
}


def t(key):
    return translations[language][key]


def change_language(new_language):
    global language

    language = new_language

    with open(LANGUAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"language": language},
            file,
            ensure_ascii=False,
            indent=4
        )

    title.config(text=t("app_title"))
    settings_button.config(text=t("settings"))
    my_location_button.config(text=t("my_location"))
    search_button.config(text=t("search"))

    weather_details_title.config(
        text=t("weather_details")
    )

    feels_like_label.config(
        text=t("feels_like")
    )

    pressure_label.config(
        text=t("pressure")
    )

    cloud_cover_label.config(
        text=t("cloud_cover")
    )

    precipitation_label.config(
        text=t("precipitation")
    )

    sun_title.config(
        text=t("sun_information")
    )

    update_button.config(
        text=t("update")
    )

    hourly_title.config(
        text=t("hourly_forecast")
    )

    daily_title.config(
        text=t("daily_forecast")
    )

    if current_weather is not None:
        show_weather(
            current_weather["current"]["temperature"],
            current_weather["current"]["humidity"],
            current_weather["current"]["wind"],
            current_weather["current"]["weather_code"],
            current_weather["current"]["feels_like"],
            current_weather["current"]["pressure"],
            current_weather["current"]["cloud_cover"],
            current_weather["current"]["precipitation"]
        )

        show_hourly_weather(
            current_weather["hourly"],
            current_weather["timezone"]
        )

        show_daily_weather(
            current_weather["daily"]
        )

        show_sun_information(
            current_weather["daily"]
        )


def open_settings():
    settings_window = tk.Toplevel(window)
    settings_window.title(t("settings"))
    settings_window.geometry("300x200")
    settings_window.resizable(False, False)

    tk.Label(
        settings_window,
        text=t("language"),
        font=("Arial", 12, "bold")
    ).pack(pady=20)

    def set_and_close(new_language):
        change_language(new_language)
        settings_window.destroy()

    tk.Button(
        settings_window,
        text="🇷🇺 Русский",
        command=lambda: set_and_close("ru")
    ).pack(pady=5)

    tk.Button(
        settings_window,
        text="🇬🇧 English",
        command=lambda: set_and_close("en")
    ).pack(pady=5)


def get_day_name(date):
    day_names = {
        0: "monday",
        1: "tuesday",
        2: "wednesday",
        3: "thursday",
        4: "friday",
        5: "saturday",
        6: "sunday"
    }

    return t(day_names[date.weekday()])


current_latitude = None
current_longitude = None
current_weather = None

async def get_location_async():
    try:
        locator = Geolocator()

        position = await locator.get_geoposition_async()

        latitude = position.coordinate.point.position.latitude
        longitude = position.coordinate.point.position.longitude

        return latitude, longitude
    except Exception:
        window.after(
            0,
            lambda: city_label.config(
                text=t("failed_location")
            )
        )
        return None

def search_city(city_name):
    if not city_name.strip():
        return None

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": language,
        "format": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return "network_error"

    if not data.get("results"):
        return None

    result = data["results"][0]

    latitude = result["latitude"]
    longitude = result["longitude"]
    name = result["name"]

    return latitude, longitude, name

def get_city(latitude, longitude): #Вывести юзеру его город/населенный пункт
    url = "https://nominatim.openstreetmap.org/reverse"

    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "zoom": 10,
    }

    headers = {
        "User-Agent": "WeatherApp/1.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        address = data["address"]

        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or t("unknown")
        )

        return city
    except requests.RequestException:
        window.after(
            0,
            lambda: city_label.config(
                text=t("failed_location")
            )
        )
        return None

    except (KeyError, TypeError):
        window.after(
            0,
            lambda: city_label.config(
                text=t("invalid_location")
            )
        )
        return None


def get_weather_info(weather_code):
    if weather_code == 0:
        return f"☀️ {t('clear_sky')}"
    elif weather_code in (1, 2):
        return f"🌤️ {t('partly_cloudy')}"
    elif weather_code == 3:
        return f"☁️ {t('overcast')}"
    elif weather_code in (45, 48):
        return f"🌫️ {t('fog')}"
    elif weather_code in (51, 53, 55):
        return f"🌦️ {t('drizzle')}"
    elif weather_code in (61, 63, 65):
        return f"🌧️ {t('rain')}"
    elif weather_code in (71, 73, 75):
        return f"❄️ {t('snow')}"
    elif weather_code in (80, 81, 82):
        return f"🌧️ {t('rain_showers')}"
    elif weather_code in (85, 86):
        return f"🌨️ {t('snow_showers')}"
    elif weather_code in (95, 96, 99):
        return f"⛈️ {t('thunderstorm')}"
    else:
        return f"❓ {t('unknown')}"


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code,"
            "apparent_temperature,"
            "pressure_msl,"
            "cloud_cover,"
            "precipitation"
        ),
        "hourly": "temperature_2m,weather_code",
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "weather_code,"
            "sunrise,"
            "sunset,"
            "precipitation_probability_max,"
            "uv_index_max"
        ),
        "forecast_days": 7,
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        current = data["current"]
        hourly = data["hourly"]
        daily = data["daily"]

        return {
            "timezone": data["timezone"],

            "current": {
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "wind": current["wind_speed_10m"],
                "weather_code": current["weather_code"],
                "feels_like": current["apparent_temperature"],
                "pressure": current["pressure_msl"],
                "cloud_cover": current["cloud_cover"],
                "precipitation": current["precipitation"],
            },

            "hourly": {
                "time": hourly["time"],
                "temperature": hourly["temperature_2m"],
                "weather_code": hourly["weather_code"],
            },

            "daily": {
                "time": daily["time"],
                "temperature_max": daily["temperature_2m_max"],
                "temperature_min": daily["temperature_2m_min"],
                "weather_code": daily["weather_code"],
                "sunrise": daily["sunrise"],
                "sunset": daily["sunset"],
                "precipitation_probability": daily["precipitation_probability_max"],
                "uv_index": daily["uv_index_max"],
            }
        }

    except requests.RequestException:
        window.after(
            0,
            lambda: weather_label.config(
                text=t("failed_weather")
            )
        )
        return None

    except (KeyError, TypeError):
        window.after(
            0,
            lambda: weather_label.config(
                text=t("invalid_weather")
            )
        )
        return None


def show_weather(
    temperature,
    humidity,
    wind,
    weather_code,
    feels_like,
    pressure,
    cloud_cover,
    precipitation
):
    weather_info = get_weather_info(weather_code)

    window.after(
        0,
        lambda: weather_label.config(
            text=f"{weather_info}\n"
                 f"{t('temperature')} {temperature} °C\n"
                 f"{t('humidity')} {humidity} %\n"
                 f"{t('wind')} {wind} km/h"
        )
    )

    window.after(
        0,
        lambda: feels_like_value.config(
            text=f"{feels_like} °C"
        )
    )

    window.after(
        0,
        lambda: pressure_value.config(
            text=f"{pressure} hPa"
        )
    )

    window.after(
        0,
        lambda: cloud_cover_value.config(
            text=f"{cloud_cover} %"
        )
    )

    window.after(
        0,
        lambda: precipitation_value.config(
            text=f"{precipitation} mm"
        )
    )


def create_weather_card(parent, time, weather_info, temperature):
    card = tk.Frame(
        parent,
        bg="white",
        width=140,
        height=130,
        highlightthickness=1,
        highlightbackground="#D5E3EC"
    )

    card.pack_propagate(False)

    time_label = tk.Label(
        card,
        text=time,
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#34495E"
    )
    time_label.pack(pady=(10, 5))

    weather_label = tk.Label(
        card,
        text=weather_info,
        font=("Arial", 10),
        bg="white",
        fg="#5D6D7E",
        wraplength=120
    )
    weather_label.pack()

    temperature_label = tk.Label(
        card,
        text=f"{temperature} °C",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#1F2937"
    )
    temperature_label.pack(pady=5)

    return card

def show_hourly_weather(hourly, timezone):
    current_time = datetime.now(
        ZoneInfo(timezone)
    ).replace(tzinfo=None)

    def update_hourly():
        for widget in hourly_frame.winfo_children():
            widget.destroy()

        count = 0

        for time, temperature, weather_code in zip(
            hourly["time"],
            hourly["temperature"],
            hourly["weather_code"]
        ):
            forecast_time = datetime.fromisoformat(time)

            if forecast_time >= current_time:
                weather_info = get_weather_info(weather_code)

                card = create_weather_card(
                    hourly_frame,
                    forecast_time.strftime("%H:%M"),
                    weather_info,
                    temperature
                )

                card.pack(
                    side="left",
                    padx=6,
                    pady=10
                )

                count += 1

                if count >= 24:
                    break

        hourly_frame.update_idletasks()

        hourly_canvas.configure(
            scrollregion=hourly_canvas.bbox("all")
        )

    window.after(0, update_hourly)


def show_daily_weather(daily):
    def update_daily():
        for widget in daily_frame.winfo_children():
            widget.destroy()

        for date, temperature_max, temperature_min, weather_code, precipitation_probability, uv_index in zip(
            daily["time"],
            daily["temperature_max"],
            daily["temperature_min"],
            daily["weather_code"],
            daily["precipitation_probability"],
            daily["uv_index"]
        ):
            forecast_date = datetime.fromisoformat(date)

            weather_info = get_weather_info(weather_code)

            card = tk.Frame(
                daily_frame,
                bg="white",
                width=150,
                height=165,
                highlightthickness=1,
                highlightbackground="#D5E3EC"
            )

            card.pack_propagate(False)

            day_label = tk.Label(
                card,
                text=get_day_name(forecast_date),
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#34495E"
            )
            day_label.pack(pady=(12, 5))

            weather_label = tk.Label(
                card,
                text=weather_info,
                font=("Arial", 10),
                bg="white",
                fg="#5D6D7E",
                wraplength=130
            )
            weather_label.pack()

            temperature_label = tk.Label(
                card,
                text=f"{temperature_max}° / {temperature_min}°",
                font=("Arial", 17, "bold"),
                bg="white",
                fg="#1F2937"
            )
            temperature_label.pack(pady=8)

            info_label = tk.Label(
                card,
                text=f"🌧️ {t('rain_short')}: {precipitation_probability}%\n"
                     f"☀️ {t('uv')}: {uv_index}",
                font=("Arial", 9),
                bg="white",
                fg="#5D6D7E"
            )
            info_label.pack()

            card.pack(
                side="left",
                padx=6,
                pady=10
            )

        daily_frame.update_idletasks()

        daily_canvas.configure(
            scrollregion=daily_canvas.bbox("all")
        )

    window.after(0, update_daily)

def show_sun_information(daily):
    sunrise = datetime.fromisoformat(
        daily["sunrise"][0]
    ).strftime("%H:%M")

    sunset = datetime.fromisoformat(
        daily["sunset"][0]
    ).strftime("%H:%M")

    sunrise_time = datetime.fromisoformat(
        daily["sunrise"][0]
    )

    sunset_time = datetime.fromisoformat(
        daily["sunset"][0]
    )

    day_length = sunset_time - sunrise_time

    hours = day_length.seconds // 3600
    minutes = (day_length.seconds % 3600) // 60

    window.after(
        0,
        lambda: sunrise_label.config(
            text=f"{t('sunrise')} {sunrise}"
        )
    )

    window.after(
        0,
        lambda: sunset_label.config(
            text=f"{t('sunset')} {sunset}"
        )
    )

    window.after(
        0,
        lambda: day_length_label.config(
            text=f"{t('day_length')} {hours}{t('hours')} {minutes}{t('minutes')}"
        )
    )

def load_weather(latitude, longitude):
    global current_weather

    weather = get_weather(latitude, longitude)

    if weather is None:
        return

    current_weather = weather

    current = weather["current"]
    hourly = weather["hourly"]
    daily = weather["daily"]
    timezone = weather["timezone"]

    show_weather(
        current["temperature"],
        current["humidity"],
        current["wind"],
        current["weather_code"],
        current["feels_like"],
        current["pressure"],
        current["cloud_cover"],
        current["precipitation"]
    )

    show_hourly_weather(hourly, timezone)
    show_daily_weather(daily)
    show_sun_information(daily)


def get_location():
    global current_latitude, current_longitude

    location = asyncio.run(get_location_async())

    if location is None:
        return

    latitude, longitude = location

    current_latitude = latitude
    current_longitude = longitude

    print("Latitude:", latitude)
    print("Longitude:", longitude)

    city = get_city(latitude, longitude)

    if city is None:
        return

    print("City:", city)

    window.after(
        0,
        lambda: city_label.config(text=f"📍 {city}")
    )

    window.after(
        0,
        lambda: weather_label.config(text=t("getting_weather"))
    )

    load_weather(latitude, longitude)


def my_location():
    thread = threading.Thread(target=get_location)
    thread.start()


def update_weather():
    if current_latitude is None or current_longitude is None:
        return

    window.after(
        0,
        lambda: weather_label.config(text=t("updating"))
    )

    thread = threading.Thread(
        target=update_weather_thread
    )
    thread.start()


def update_weather_thread():
    load_weather(current_latitude, current_longitude)


def start_search():
    city_name = city_entry.get().strip()

    window.after(
        0,
        lambda: city_label.config(text=t("searching"))
    )

    thread = threading.Thread(
        target=search_weather,
        args=(city_name,)
    )
    thread.start()


def search_weather(city_name):
    global current_latitude, current_longitude

    if not city_name.strip():
        window.after(
            0,
            lambda: city_label.config(text=t("enter_city"))
        )
        return
    location = search_city(city_name)

    if location == "network_error":
        window.after(
            0,
            lambda: city_label.config(text=t("network_error"))
        )
        return

    if location is None:
        window.after(
            0,
            lambda: city_label.config(text=t("city_not_found"))
        )
        return

    latitude, longitude, city_name = location

    current_latitude = latitude
    current_longitude = longitude

    window.after(
        0,
        lambda: city_label.config(text=f"📍 {city_name}")
    )

    load_weather(latitude, longitude)

window = tk.Tk()
window.title("Weather App v1")
window.geometry("850x620")
window.minsize(700, 500)
window.configure(bg="#EAF2F8")

# Основной вертикальный Canvas

main_canvas = tk.Canvas(
    window,
    bg="#EAF2F8",
    highlightthickness=0
)
main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

main_scrollbar = tk.Scrollbar(
    window,
    orient="vertical",
    command=main_canvas.yview
)
main_scrollbar.pack(
    side="right",
    fill="y"
)

main_canvas.configure(
    yscrollcommand=main_scrollbar.set
)


# Главный Frame внутри Canvas
main_frame = tk.Frame(
    main_canvas,
    bg="#EAF2F8"
)

main_canvas_window = main_canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


# Обновляем область прокрутки
def update_scrollregion(event=None):
    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )


main_frame.bind(
    "<Configure>",
    update_scrollregion
)


# Растягиваем main_frame по ширине Canvas
def resize_main_frame(event):
    main_canvas.itemconfig(
        main_canvas_window,
        width=event.width
    )


def on_mousewheel(event):
    if event.state & 0x0001:
        widget = main_canvas.winfo_containing(
            event.x_root,
            event.y_root
        )

        while widget is not None:
            if widget == hourly_frame:
                hourly_canvas.xview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
                return "break"

            if widget == daily_frame:
                daily_canvas.xview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )
                return "break"

            widget = widget.master

        return

    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


main_canvas.bind_all(
    "<MouseWheel>",
    on_mousewheel
)

main_canvas.bind(
    "<Configure>",
    resize_main_frame
)

# Верхняя панель

top_frame = tk.Frame(
    main_frame,
    bg="#EAF2F8"
)
top_frame.pack(
    fill="x",
    padx=20,
    pady=(10, 5)
)


title = tk.Label(
    top_frame,
    text=t("app_title"),
    font=("Arial", 24, "bold"),
    bg="#EAF2F8",
    fg="#1F2937"
)
title.pack(
    side="left"
)

settings_button = tk.Button(
    top_frame,
    text=t("settings"),
    command=open_settings,
    font=("Arial", 10, "bold"),
    bg="#3498DB",
    fg="white",
    relief="flat",
    padx=12,
    pady=5,
    cursor="hand2"
)
settings_button.pack(
    side="right",
    padx=(5, 0)
)

my_location_button = tk.Button(
    top_frame,
    text=t("my_location"),
    command=my_location,
    font=("Arial", 10, "bold"),
    bg="#3498DB",
    fg="white",
    relief="flat",
    padx=12,
    pady=5,
    cursor="hand2"
)
my_location_button.pack(
    side="right"
)

# Поиск города

search_frame = tk.Frame(
    main_frame,
    bg="#EAF2F8"
)
search_frame.pack(
    pady=5
)


city_entry = tk.Entry(
    search_frame,
    font=("Arial", 13),
    width=25,
    relief="flat"
)
city_entry.pack(
    side="left",
    padx=(0, 5),
    ipady=5
)


search_button = tk.Button(
    search_frame,
    text=t("search"),
    command=start_search,
    font=("Arial", 10, "bold"),
    bg="#3498DB",
    fg="white",
    relief="flat",
    padx=14,
    pady=5,
    cursor="hand2"
)
search_button.pack(
    side="left"
)

# Название города

city_label = tk.Label(
    main_frame,
    text=t("getting_location"),
    font=("Arial", 17, "bold"),
    bg="#EAF2F8",
    fg="#1F2937"
)
city_label.pack(
    pady=(5, 3)
)

# Текущая погода

weather_card = tk.Frame(
    main_frame,
    bg="white",
    highlightthickness=1,
    highlightbackground="#D5E3EC"
)
weather_card.pack(
    padx=20,
    pady=3
)


weather_label = tk.Label(
    weather_card,
    text=t("getting_weather"),
    font=("Arial", 16),
    bg="white",
    fg="#1F2937",
    padx=30,
    pady=10
)
weather_label.pack()

weather_details_card = tk.Frame(
    main_frame,
    bg="white",
    highlightthickness=1,
    highlightbackground="#D5E3EC"
)
weather_details_card.pack(
    padx=20,
    pady=5
)

weather_details_title = tk.Label(
    weather_details_card,
    text=t("weather_details"),
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#1F2937"
)
weather_details_title.pack(
    pady=(10, 5)
)

weather_details_frame = tk.Frame(
    weather_details_card,
    bg="white"
)
weather_details_frame.pack(
    padx=25,
    pady=(5, 12)
)


# Feels like

feels_like_icon = tk.Label(
    weather_details_frame,
    text="🌡️",
    font=("Arial", 12),
    bg="white",
    fg="#E67E22",
    width=3
)
feels_like_icon.grid(
    row=0,
    column=0,
    padx=(0, 8),
    pady=4
)

feels_like_label = tk.Label(
    weather_details_frame,
    text=t("feels_like"),
    font=("Arial", 11),
    bg="white",
    fg="#5D6D7E",
    width=14,
    anchor="w"
)
feels_like_label.grid(
    row=0,
    column=1,
    pady=4
)

feels_like_value = tk.Label(
    weather_details_frame,
    text="-- °C",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1F2937",
    width=10,
    anchor="w"
)
feels_like_value.grid(
    row=0,
    column=2,
    pady=4
)


# Pressure

pressure_icon = tk.Label(
    weather_details_frame,
    text="📊",
    font=("Arial", 12),
    bg="white",
    fg="#8E44AD",
    width=3
)
pressure_icon.grid(
    row=1,
    column=0,
    padx=(0, 8),
    pady=4
)

pressure_label = tk.Label(
    weather_details_frame,
    text=t("pressure"),
    font=("Arial", 11),
    bg="white",
    fg="#5D6D7E",
    width=14,
    anchor="w"
)
pressure_label.grid(
    row=1,
    column=1,
    pady=4
)

pressure_value = tk.Label(
    weather_details_frame,
    text="-- hPa",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1F2937",
    width=10,
    anchor="w"
)
pressure_value.grid(
    row=1,
    column=2,
    pady=4
)


# Cloud cover

cloud_cover_icon = tk.Label(
    weather_details_frame,
    text="☁️",
    font=("Arial", 12),
    bg="white",
    fg="#3498DB",
    width=3
)
cloud_cover_icon.grid(
    row=2,
    column=0,
    padx=(0, 8),
    pady=4
)

cloud_cover_label = tk.Label(
    weather_details_frame,
    text=t("cloud_cover"),
    font=("Arial", 11),
    bg="white",
    fg="#5D6D7E",
    width=14,
    anchor="w"
)
cloud_cover_label.grid(
    row=2,
    column=1,
    pady=4
)

cloud_cover_value = tk.Label(
    weather_details_frame,
    text="-- %",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1F2937",
    width=10,
    anchor="w"
)
cloud_cover_value.grid(
    row=2,
    column=2,
    pady=4
)


# Precipitation

precipitation_icon = tk.Label(
    weather_details_frame,
    text="🌧️",
    font=("Arial", 12),
    bg="white",
    fg="#2980B9",
    width=3
)
precipitation_icon.grid(
    row=3,
    column=0,
    padx=(0, 8),
    pady=4
)

precipitation_label = tk.Label(
    weather_details_frame,
    text=t("precipitation"),
    font=("Arial", 11),
    bg="white",
    fg="#5D6D7E",
    width=14,
    anchor="w"
)
precipitation_label.grid(
    row=3,
    column=1,
    pady=4
)

precipitation_value = tk.Label(
    weather_details_frame,
    text="-- mm",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1F2937",
    width=10,
    anchor="w"
)
precipitation_value.grid(
    row=3,
    column=2,
    pady=4
)

sun_card = tk.Frame(
    main_frame,
    bg="white",
    highlightthickness=1,
    highlightbackground="#D5E3EC"
)
sun_card.pack(padx=20, pady=5)

sun_title = tk.Label(
    sun_card,
    text=t("sun_information"),
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#1F2937"
)
sun_title.pack(pady=(10, 5))

sun_info_frame = tk.Frame(
    sun_card,
    bg="white"
)
sun_info_frame.pack(
    pady=10,
    padx=10
)

sunrise_icon = tk.Label(
    sun_info_frame,
    text="🌅",
    font=("Segoe UI Emoji", 11),
    bg="white"
)
sunrise_icon.grid(
    row=0,
    column=0,
    padx=(0, 8),
    pady=2
)

sunrise_label = tk.Label(
    sun_info_frame,
    text="",
    font=("Arial", 11),
    bg="white",
    fg="#5D6D7E",
    anchor="w",
)
sunrise_label.grid(
    row=0,
    column=1,
    sticky="w",
    pady=2
)


sunset_icon = tk.Label(
    sun_info_frame,
    text="🌇",
    font=("Segoe UI Emoji", 11),
    bg="white"
)
sunset_icon.grid(
    row=1,
    column=0,
    padx=(0, 8),
    pady=2
)

sunset_label = tk.Label(
    sun_info_frame,
    text="",
    font=("Arial", 11),
    bg="white",
    fg="#5D6D7E",
    anchor="w",
)
sunset_label.grid(
    row=1,
    column=1,
    sticky="w",
    pady=2
)


day_length_icon = tk.Label(
    sun_info_frame,
    text="☀️",
    font=("Segoe UI Emoji", 11),
    bg="white"
)
day_length_icon.grid(
    row=2,
    column=0,
    padx=(0, 8),
    pady=2
)

day_length_label = tk.Label(
    sun_info_frame,
    text="",
    font=("Arial", 11),
    bg="white",
    fg="#5D6D7E",
    anchor="w",
)
day_length_label.grid(
    row=2,
    column=1,
    sticky="w",
    pady=2
)

# Кнопка обновления

update_button = tk.Button(
    main_frame,
    text=t("update"),
    command=update_weather,
    font=("Arial", 10, "bold"),
    bg="#3498DB",
    fg="white",
    relief="flat",
    padx=16,
    pady=5,
    cursor="hand2"
)
update_button.pack(
    pady=(3, 6)
)

# Почасовой прогноз

hourly_title = tk.Label(
    main_frame,
    text=t("hourly_forecast"),
    font=("Arial", 15, "bold"),
    bg="#EAF2F8",
    fg="#1F2937"
)
hourly_title.pack(
    pady=(5, 3)
)


hourly_canvas = tk.Canvas(
    main_frame,
    height=155,
    bg="#EAF2F8",
    highlightthickness=0
)

hourly_canvas.pack(
    fill="x",
    padx=20
)


hourly_scrollbar = tk.Scrollbar(
    main_frame,
    orient="horizontal",
    command=hourly_canvas.xview
)
hourly_scrollbar.pack(
    fill="x",
    padx=20
)


hourly_canvas.configure(
    xscrollcommand=hourly_scrollbar.set
)


hourly_frame = tk.Frame(
    hourly_canvas,
    bg="#EAF2F8"
)


hourly_canvas.create_window(
    (0, 0),
    window=hourly_frame,
    anchor="nw"
)

# 7-дневный прогноз

daily_title = tk.Label(
    main_frame,
    text=t("daily_forecast"),
    font=("Arial", 15, "bold"),
    bg="#EAF2F8",
    fg="#1F2937"
)
daily_title.pack(
    pady=(15, 5)
)


daily_canvas = tk.Canvas(
    main_frame,
    height=165,
    bg="#EAF2F8",
    highlightthickness=0
)
daily_canvas.pack(
    fill="x",
    padx=20
)


daily_scrollbar = tk.Scrollbar(
    main_frame,
    orient="horizontal",
    command=daily_canvas.xview
)
daily_scrollbar.pack(
    fill="x",
    padx=20
)


daily_canvas.configure(
    xscrollcommand=daily_scrollbar.set
)


daily_frame = tk.Frame(
    daily_canvas,
    bg="#EAF2F8"
)


daily_canvas.create_window(
    (0, 0),
    window=daily_frame,
    anchor="nw"
)

# Запуск получения локации

thread = threading.Thread(
    target=get_location
)
thread.start()


window.mainloop()

