import os
import numpy as np
import pandas as pd
import pyepw
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import axes
from mpl_toolkits.mplot3d import Axes3D


def dc_timestep(view, transmission, daylight, sky, save_path, option="", if_print=True):
    """
    compute annual simulation time-step(s) via matrix multiplication
    :param view:  view matrix, relating outgoing directions on window to desired results at interior
    :param transmission: transmission matrix, relating incident window directions to exiting directions (BSDF)
    :param daylight: daylight matrix, relating sky patches to incident directions on window
    :param sky: sky vector/matrix, assigning luminance values to patches representing sky directions
    :param save_path: the path to save the RGB data
    :param option: "-n 8760" when do manual simulation
    :param if_print: if print the command
    :return: the RGB values of each photo cells
    """

    command = "dctimestep -h " + option + " " + view + " " + transmission + " " + daylight + " " + sky + " > " \
              + save_path
    if if_print:
        print(command)
    os.system(command)


def view_matrix(octree, photocells, window_material):
    """
    compute the view matrix by the view file.
    There may be some wrongs in native-windows.
    :param octree: the window must be replaced by a glazing material
    :param photocells: points in time illuminance or luminance result
    :param window_material: the glazing materials of the window
    :return: view_matrix
    """
    command = "rcontrib -f klems_full.cal -b kbinS -bn Nkbins -m "+window_material + " -I+ \
    -ab 12 -ad 50000 -lw 2e-5 " + octree + " < " + photocells
    print(command)
    matrix = os.system(command)
    return matrix


def gen_skv_p(altitude, azimuth, epsilon, delta, path_save_skv):
    """
    gen sky vector by Perez parameters
    Deriving the epsilon and delta parameters for use with the -P invocation is quite complicated, and you are unlikely
    to need this.
    :param altitude: the altitude is measured in degrees above the horizon
    :param azimuth: the azimuth is measured in degrees west of South
    :param epsilon: Epsilon variations express the transition from a totally overcast sky (epsilon=1) to a low turbidity
     clear sky (epsilon>6)
    :param delta:  Delta can vary from 0.05 representing a dark sky to 0.5 for a very bright sky.
    :param path_save_skv: the path to save the sky vector
    :return: return the sky vector
    """

    command = "gendaylit -ang " + str(altitude) + " " + str(azimuth) + " -P " + " " + str(epsilon) + " " + str(delta) +\
              " " + " |genskyvec -m 4 -c 1 1 1 > " + path_save_skv
    print(command)
    os.system(command)


def gen_skv_W(altitude, azimuth, direct_normal_irradiance, diffuse_horizontal_irradiance, path_save_skv):
    """
    gen sky vector by irradiance
    :param altitude: the altitude is measured in degrees above the horizon
    :param azimuth: the azimuth is measured in degrees west of South
    :param direct_normal_irradiance: the radiant flux coming from the sun and an area of approximately 3 degrees
    round the sun
    :param diffuse_horizontal_irradiance:
    :param path_save_skv: the path to save the sky vector
    :return: sky vec
    """
    command = "gendaylit -ang " + str(altitude) + " " + str(azimuth) + " -W " + " " + str(direct_normal_irradiance) + \
              " " + str(diffuse_horizontal_irradiance) + " " + " |genskyvec -m 4 -c 1 1 1 > " + path_save_skv
    print(command)
    os.system(command)


def rgb2lux(rgb_path):
    """
    :param rgb_path: the address of the rgb data, which were split by space
    :return: the illumination list
    """
    rgb_read = open(rgb_path, "r")
    lux_list = []
    for rgb_line in rgb_read.readlines():
        rgb_data = rgb_line.split()
        lux_num = 179.0*(float(rgb_data[0])*0.265+float(rgb_data[1])*0.670+float(rgb_data[2])*0.065)
        lux_list.append(lux_num)
    return lux_list


def drawHotMap3D(lux_t, height, weight, add='0', bias=1):
    # 绘制热图
    y = np.arange(0, weight, 1)
    x = np.arange(0, height-bias, 1)
    X, Y = np.meshgrid(x, y)
    lux_len = len(lux_t)
    temp = []
    for i in range(0, lux_len, height):
        temp.append(lux_t[i:i + height-bias])
    # plt.imshow(temp, cmap='hot_r', vmin=0, vmax=1600)
    # 增加右侧的颜色刻度条
    Z = np.array(temp)
    sort_temp = Z.flatten()
    sort_temp.sort()
    temp_mean = np.mean(sort_temp)
    print(temp_mean)
    min_list = sort_temp[0:100]
    temp_min = np.mean(min_list)
    print(temp_min)
    average_degree = temp_min/temp_mean
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none', vmax=2000)
    ax.set_zlim(0, 2000)
    ax.set_title('average degree: %.3f, mean=%.2f, min=%.2f' % (average_degree, temp_mean, temp_min))
    if add != '0':
        plt.savefig(add)
        plt.clf()
    else:
        plt.show()


def date_draw():
    # 查找某时间对应的气候数据，并计算照度分布
    original_data = "data/angle_null.xlsx"
    all_data = pd.read_excel(original_data)
    date_list = all_data["Date/Time"]

    vmx_d = "rad_files/vmx/room_s_photocells_7.vmx"
    dmx_d = "rad_files/dmx/room_S.dmx"
    skv_d = "rad_files/skv/radiance_temp.skv"
    path_d = "rad_files/results/room_s_radiance_temp.dat"

    date = input("date:")
    save_root = input("add:")
    first_item = " %s:00" % date
    first_index = 0

    for i, item in enumerate(date_list):
        if item == first_item:
            first_index = i
            print("find")
            break
    input_data = all_data.iloc[first_index]
    diffuse_rate = input_data[3]
    direct_rate = input_data[4]
    azimuth_d = input_data[5]
    altitude_d = input_data[6]
    gen_skv_W(altitude_d, azimuth_d, direct_rate, diffuse_rate, skv_d)
    for i in range(5, 180, 5):
        xml_d = "rad_files/xml/type25_angle%s.xml" % str(i)
        dc_timestep(vmx_d, xml_d, dmx_d, skv_d, path_d)
        lux = rgb2lux(path_d)
        save_add = save_root + "%s.jpg" % i
        drawHotMap3D(lux, 81, 35, add=save_add, bias=0)


def radiance_test():
    ang = '75'
    vmx = "rad_files/vmx/room_s_photocells_7.vmx"
    xml = "rad_files/xml/type25_angle%s.xml" % ang
    dmx = "rad_files/dmx/room_S.dmx"
    skv = "rad_files/skv/temp.skv"
    path = "rad_files/results/room_s_d063014_p7_a%s.dat" % ang

    dc_timestep(vmx, xml, dmx, skv, path)
    print("****")

    lux = rgb2lux(path)
    print(len(lux))
    # drawHotMap3D(lux, 16, 31, 0)
    drawHotMap3D(lux, 81, 35, bias=0)
    # gen_skv_p(60, 0, 3.2, 0.24, "rad_files/skv/test_60_0.skv")
    # print(lux)
    # gen_skv_W(61.68, 260, 758, 89.5, "./rad_files/skv/6_30_14.skv")


if __name__ == "__main__":
    date_draw()
