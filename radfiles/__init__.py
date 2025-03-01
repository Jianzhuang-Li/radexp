import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# the path where save the diffusion model weights.
radfiles_dmx = os.path.join(current_dir, "dmx")
radfiles_xml = os.path.join(current_dir, "xml")
radfiles_vmx = os.path.join(current_dir, "vmx")
radfiles_skv = os.path.join(current_dir, "skv")
weather_data = os.path.join(current_dir, "weather")

# the available weather
CHN_ShanghaiCSWD = os.path.join(weather_data, "CHN_ShanghaiCSWD.epw")

# the available vmx
vmx_south = os.path.join(radfiles_vmx, "south.vmx")
vmx_north = os.path.join(radfiles_vmx, "north.vmx")
vmx_west = os.path.join(radfiles_vmx, "west.vmx")
vmx_east = os.path.join(radfiles_vmx, "east.vmx")

# the available dmx
dmx_south = os.path.join(radfiles_dmx, "south.dmx")
dmx_north = os.path.join(radfiles_dmx, "north.dmx")
dmx_west = os.path.join(radfiles_dmx, "west.dmx")
dmx_east = os.path.join(radfiles_dmx, "east.dmx")

# the avaiable xml
xml_angle_null = os.path.join(radfiles_xml, "type25_anglenull.xml")
xml_angle_45 = os.path.join(radfiles_xml, "type25_angle45.xml")

def get_type25_xml(angle=None):
    if angle == None:
        return xml_angle_null
    else:
        return os.path.join(radfiles_xml, f"type25_angle{angle}.xml")

# skv for testing
skv_063010 = os.path.join(radfiles_skv, "6_30_10.skv")
skv_063014 = os.path.join(radfiles_skv, "6_30_14.skv")
skv_063018 = os.path.join(radfiles_skv, "6_30_18.skv")