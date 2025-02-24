from pyepw.epw import EPW, WeatherData, Location
from dataclasses import dataclass
import math
import datetime
import ephem

@dataclass
class EpWeatherData:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    dry_bulb_temperature: float
    relative_humidity: float
    global_horizontal_radiation: float
    direct_normal_radiation: float
    diffuse_horizontal_radiation: float
    global_horizontal_illuminance: float
    direct_normal_illuminance: float
    diffuse_horizontal_illuminance: float
    zenith_luminance: float
    wind_speed: float
    wind_direction: float

def get_alt_az(lon, lat, height, year, month, day, hour, minute, second):
    """
    get the altitude and azimuth of sun by the longitude, latitude and time
    the time must be Greenwich time of the local
    :param lon: longitude
    :param lat: latitude
    :param height: sea level height
    :param year: year
    :param month: month
    :param day: day
    :param hour: hour
    :param minute: minute
    :param second: second
    :return: return the azimuth and latitude
    """
    date = datetime.datetime(year, month, day, hour, minute, second)
    date = date.strftime("%Y/%m/%d %H:%M:%S")
    # print(date)
    sun = ephem.Sun()
    ga_tech = ephem.Observer()
    ga_tech.lon = str(lon)
    ga_tech.lat = str(lat)
    ga_tech.elevation = height
    ga_tech.date = date
    sun.compute(ga_tech)
    # repr() 方法可以将读取到的格式字符，比如换行符、制表符，转化为其相应的转义字符
    sun_altitude = float(repr(sun.alt))/math.pi * 180.0
    sun_azimuth = float(repr(sun.az))/math.pi * 180.0
    return sun_altitude, sun_azimuth

class EpWeather:
    
    def __init__(self, file_path:str) -> None:
        """Read epw weather files.

        Args:
            file_path (str): epw file path
        """
        self.file_path = file_path
        self.epw_data = EPW()
        self.epw_data.read(self.file_path)
        self.weather_data = self.epw_data.weatherdata
        self.max_len = len(self.weather_data)
        # time interval between two weather data.
        d1, d2 = self.weather_data[0], self.weather_data[1] 
        self.interval = (d2.hour - d1.hour) * 60 + (d2.minute - d1.minute) 
        self.count = 0
        self.weather_dict = {}
        self.year = self.weather_data[0].year
        for item in self.weather_data:
            year = item.year
            month = item.month
            day = item.day
            hour = item.hour
            minute = item.minute

            year_dict = self.weather_dict.setdefault(year, {})
            month_dict = year_dict.setdefault(month, {})
            day_dict = month_dict.setdefault(day, {})
            hour_dict = day_dict.setdefault(hour, {})

            hour_dict[minute] = item
            

    @property
    def location(self) -> Location:
        """Get location data dictionary object.

        Returns:
            Object of type Location or None if not yet set

        """
        return self.epw_data.location
    
    def get_weather(self, month, day, hour, minute=0, year=None) -> EpWeatherData:
        """Get weather data by date time

        Args:
            month (int): int
            day (int): int
            hour (int): int
        """
        if year is None:
            year = self.year
        weather: WeatherData = self.weather_dict[year][month][day][hour][minute]
        # add weather by your need, it only contain a part of the whole weather data.
        data_dict = EpWeatherData(
            year = year,
            month = month,
            day = day,
            hour = hour,
            minute = minute,
            dry_bulb_temperature = weather.dry_bulb_temperature,
            relative_humidity = weather.relative_humidity,
            global_horizontal_radiation = weather.global_horizontal_radiation,
            direct_normal_radiation = weather.direct_normal_radiation,
            diffuse_horizontal_radiation =weather.diffuse_horizontal_radiation,
            global_horizontal_illuminance = weather.global_horizontal_illuminance,
            direct_normal_illuminance = weather.direct_normal_illuminance,
            diffuse_horizontal_illuminance = weather.diffuse_horizontal_illuminance,
            zenith_luminance = weather.zenith_luminance,
            wind_speed = weather.wind_speed,
            wind_direction = weather.wind_direction,
        )
        return data_dict

        