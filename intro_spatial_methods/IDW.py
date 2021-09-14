import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def read_camera_orientation_info(filename1):

    with open(filename1, 'r') as f:
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


def display_image(filename="test_image_gray.tif"):
    image = plt.imread(filename)
    # n_rows, n_columns = image.shape
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray', vmin=0, vmax=255)
    ax.axis('off')
    plt.show()


def read_laserdata(filename="laserdata.txt"):

    df = pd.read_csv(filename, sep=' ', header=None)
    return df.to_numpy()


def d(x, x_i):
    if isinstance(x, float) or isinstance(x, int):
        return np.sqrt((x - x_i) ** 2)

    else:
        X, Y = x
        X_i, Y_i = x_i
        return np.sqrt((X - X_i) ** 2 + (Y - Y_i) ** 2)


def w(x, x_i, p=2):
    return 1 / (d(x, x_i)**p)


def u(x, neighbours_x, neighbours_u, n=3):

    weights = []
    for i in range(n):
        x_i = neighbours_x[i]
        weight_i = w(x, x_i)
        weights.append(weight_i)

        print(f'weight {i+1}: {weight_i}')

    sum_weights = np.sum(weights)

    total = 0
    for i in range(n):
        u_i = neighbours_u[i]
        w_i = weights[i]
        to_add = w_i * u_i
        total += to_add

        print(f'w{i + 1}u{i+1}: {to_add}')

    result = total / sum_weights
    return result


def main():

    neighbours_u = [10, 4, 18]
    neighbours_x = [3, 0, 5]
    x = 2
    u_x = u(x=x, neighbours_u=neighbours_u, neighbours_x=neighbours_x)
    print(u_x)

    neighbours_u = [10, 4, 18]
    neighbours_x = [
        [10, 4],
        [2, 3],
        [3, 6]
    ]
    x = [3, 4]
    u_x = u(x=x, neighbours_u=neighbours_u, neighbours_x=neighbours_x)
    print(u_x)

    # filename1 = "camera_orientation_info.txt"
    # read_camera_orientation_info(filename1)
    # read_laserdata()

    # filename2 = "laserdata.txt"
    # read_laserdata(filename2)


main()
