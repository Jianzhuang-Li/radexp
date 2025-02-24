import radfiles.skv
from weather import EpWeather, get_alt_az
from pyepw.epw import Location
from radiance import gen_skv_W,dc_timestep
from radiance import drawHotMap3D
from radfiles import xml_angle_null, skv_063010, skv_063014, skv_063018
from radfiles import dmx_north, dmx_east, dmx_south, dmx_west
from radfiles import vmx_east, vmx_north, vmx_south, vmx_west
from radiance import IlluData, SkyData
from radiance import dc_timestep_pipe, dc_timestep_group
import radfiles
import os
import sys

# 

# current_dir = os.path.dirname(os.path.abspath(__file__))
# radiance_path = os.path.join(current_dir, "radiance\\bin")
# print(radiance_path)
# os.environ["PATH"] += radiance_path

weather_data = EpWeather(file_path=radfiles.CHN_ShanghaiCSWD)
location = weather_data.location

longitude = location.longitude
latitude = location.latitude
height = 2.19

weather_d = weather_data.get_weather(month=2, day=24, hour=12)

year = 2025
# year = weather_d.year
month = weather_d.month
day = weather_d.day
hour = weather_d.hour
minute = weather_d.minute
second = 0

print(longitude, latitude)
print(month, day, hour, minute, second)
alt, az = get_alt_az(lon=longitude, lat=latitude, height=height, year=year, month=month, day=day, hour=hour, minute=minute, second=second)
print(alt, az)

direct_normal_irradiance = weather_d.direct_normal_radiation
diffuse_horizontal_irradiance = weather_d.diffuse_horizontal_radiation
direct_normal_illuminance = weather_d.direct_normal_illuminance
diffuse_horizontal_illuminance = weather_d.diffuse_horizontal_illuminance

path_save_skv = os.path.join(radfiles.radfiles_skv, f"skv_{year}_{month}_{day}_{hour}.skv")

# gen_skv_W(altitude=alt, azimuth=az, direct_normal_irradiance=direct_normal_irradiance, diffuse_horizontal_irradiance=diffuse_horizontal_irradiance, path_save_skv=path_save_skv)
xml_angle = xml_angle_null
skv = skv_063018

skv_data = SkyData(altitude=alt, azimuth=az, \
                direct_normal_irradiance=direct_normal_irradiance, \
                diffusion_horizonttal_irradiance=diffuse_horizontal_irradiance, \
                direct_normal_illuminance=direct_normal_illuminance, \
                diffusion_horizonttal_illumiance=diffuse_horizontal_illuminance)
print(skv_data)
illu_data_south = IlluData(dmx=dmx_south, xml=xml_angle, vmx=vmx_south)
illu_data_west = IlluData(dmx=dmx_west, xml=xml_angle, vmx=vmx_west)
illu_data_east = IlluData(dmx=dmx_east, xml=xml_angle, vmx=vmx_east)
illu_data_north = IlluData(dmx=dmx_north, xml=xml_angle, vmx=vmx_south)

# illu_group = [illu_data_south, illu_data_north, illu_data_east, illu_data_west]
# result = dc_timestep_group(skv_data, illu_group)
# result_south = result[0]
# result_north = result[1]
# result_east = result[2]
# result_west = result[3]

result_south = dc_timestep_pipe(sky_data=skv_data, illu_data=illu_data_south)
result_north = dc_timestep_pipe(sky_data=skv_data, illu_data=illu_data_north)
result_east = dc_timestep_pipe(sky_data=skv_data, illu_data=illu_data_east)
result_west = dc_timestep_pipe(sky_data=skv_data, illu_data=illu_data_west)

"""
result_south = dc_timestep(vmx_south, xml_angle, dmx_south, skv, "")
result_north = dc_timestep(vmx_north, xml_angle, dmx_north, skv, "")
result_west = dc_timestep(vmx_west, xml_angle, dmx_west, skv, "")
result_east = dc_timestep(vmx_east, xml_angle, dmx_east, skv, "")
"""
points_num = len(result_east)
point_ill = []
for i in range(points_num):
    sou = result_south[i]
    nor = result_north[i]
    eas = result_east[i]
    wes = result_west[i]
    illu = 179.0 * (sou[0] + nor[0] + eas[0] + wes[0]) * 0.25 + \
        (sou[1] + nor[1] + eas[1] + wes[1]) * 0.670 + (sou[2] + nor[2] + eas[2] + wes[2]) * 0.065
    point_ill.append(illu)

drawHotMap3D(point_ill, height=31 , weight=60)

