import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KDTree

from IDW import read_laserdata, read_image, read_camera_orientation_info


def main():
    laser_data = read_laserdata()
    laser_x = laser_data[:, 0]
    laser_y = laser_data[:, 1]
    laser_z = laser_data[:, 2]
    laser_xy = laser_data[:, :2]
    print("from Laser data")
    print(f'x-coordinate: min={laser_x.min()}, max={laser_x.max()}')
    print(f'y-coordinate: min={laser_y.min()}, max={laser_y.max()}')
    orthophoto = read_image()

    print("read camera orientation")
    pp_x, pp_y, c, r, x_0, y_0, z_0 = read_camera_orientation_info()
    print(f'pp_x = {pp_x}, pp_y = {pp_y}, c = {c}, r = {r}, x_0 = {x_0}, y_0 = {y_0}, z_0 = {z_0}')
    print("*" * 30)
    tree = KDTree(laser_xy)

    n_pixel_rows, n_pixel_columns = orthophoto.shape

    x_start = 6111.4
    y_start = 5267.0
    grid_size = 0.2

    pixel_x_start = x_start
    pixel_y_start = y_start - n_pixel_rows*grid_size

    pixel_x_stop = x_start + n_pixel_columns*grid_size
    pixel_y_stop = y_start

    laser_x_start = laser_x.min()  # 6088.331
    laser_y_start = laser_y.min()

    laser_x_stop = laser_x.max()
    laser_y_stop = laser_y.max()

    print(
        f"pixel_x_start = {pixel_x_start}\n"
        f"pixel_y_start = {pixel_y_start}\n\n"
        f"pixel_x_stop = {pixel_x_stop}\n"
        f"pixel_y_stop = {pixel_y_stop}\n\n"
        f"laser_x_start = {laser_x_start}\n"
        f"laser_y_start = {laser_y_start}\n\n"
        f"laser_x_stop = {laser_x_stop}\n"
        f"laser_y_stop = {laser_y_stop}\n\n"
    )


main()
