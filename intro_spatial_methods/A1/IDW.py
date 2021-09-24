import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KDTree

"""
loading data
"""


def read_camera_orientation_info(filename="camera_orientation_info.txt"):

    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    pp_x = float(lines[1])
    pp_y = float(lines[2])
    c = float(lines[4])

    x_0 = float(lines[9])
    y_0 = float(lines[10])
    z_0 = float(lines[11])

    r = np.zeros((3, 3))

    for i in range(3):
        str_row = lines[13 + i].split("\t")
        r[i] = [float(x) for x in str_row]

    return pp_x, pp_y, c, r, x_0, y_0, z_0


def read_laserdata(filename="laserdata.txt"):
    df = pd.read_csv(filename, sep=' ', header=None)
    laser_data = df.to_numpy()
    return laser_data


def read_image(filename="test_image_gray.tif"):
    image = plt.imread(filename)
    return image


def display_image(filename="test_image_gray.tif"):
    image = plt.imread(filename)
    # n_rows, n_columns = image.shape
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray', vmin=0, vmax=255)
    ax.set_axis_off()

    fig.tight_layout(pad=0, h_pad=0, w_pad=0)
    plt.savefig('image.png', bbox_inches='tight', pad_inches=0)
    plt.show()


"""
Computation 
"""


def d(x, x_i):

    try:
        X, Y = x
        X_i, Y_i = x_i
        return np.sqrt((X - X_i) ** 2 + (Y - Y_i) ** 2)
    except:
        print('was it testing with 1D?')
        return np.sqrt((x - x_i) ** 2)


def w(d_i, p=2):
    return 1 / d_i**p


def u(neighbours_u, neighbours_d):

    n = len(neighbours_d)

    weights = []
    for i in range(n):
        d_i = neighbours_d[i]
        weight_i = w(d_i)
        weights.append(weight_i)

        # print(f'weight {i+1}: {weight_i}')

    sum_weights = np.sum(weights)

    total = 0
    for i in range(n):
        u_i = neighbours_u[i]
        w_i = weights[i]
        to_add = w_i * u_i
        total += to_add

        # print(f'w{i + 1}u{i+1}: {to_add}')

    result = total / sum_weights
    return result


def main():

    laser_data = read_laserdata()
    laser_x = laser_data[:, 0]
    laser_y = laser_data[:, 1]
    laser_z = laser_data[:, 2]
    laser_xy = laser_data[:, :2]
    print(f'x-coordinate: min={laser_x.min()}, max={laser_x.max()}')
    print(f'y-coordinate: min={laser_y.min()}, max={laser_y.max()}')

    orthophoto = read_image()

    print("read camera orientation")
    pp_x, pp_y, c, r, x_0, y_0, z_0 = read_camera_orientation_info()
    print(f'pp_x = {pp_x}, pp_y = {pp_y}, c = {c}, r = {r}, x_0 = {x_0}, y_0 = {y_0}, z_0 = {z_0}')
    print("*" * 30)

    tree = KDTree(laser_xy)

    pixels_rows, pixels_columns = 1, 3         # orthophoto.shape
    DEM = np.zeros((pixels_rows, pixels_columns))

    x_start = 6111.4
    y_start = 5267
    grid_size = 0.2

    for i in range(pixels_rows):
        for j in range(pixels_columns):

            X = x_start + j*grid_size
            Y = y_start - i*grid_size

            dist, ind = tree.query(np.array([[X, Y], ]), k=5)
            # ind/dist shape: 1 x k
            neighbours_u = laser_z[ind[0]]
            neighbours_d = dist[0]

            interpolated_height = u(neighbours_d=neighbours_d,
                                    neighbours_u=neighbours_u)
            DEM[i, j] = interpolated_height

    print(DEM)


    # neighbours_u = [10, 4, 18]
    # neighbours_x = [3, 0, 5]
    # x = 2
    # u_x = u(x=x, neighbours_u=neighbours_u, neighbours_x=neighbours_x)
    # print(u_x)

    # neighbours_u = [10, 4, 18]
    # neighbours_x = [
    #     [10, 4],
    #     [2, 3],
    #     [3, 6]
    # ]
    # x = [3, 4]
    # u_x = u(x=x, neighbours_u=neighbours_u, neighbours_x=neighbours_x)
    # print(u_x)

    # display_image()

if __name__ == "__main__":
    main()
