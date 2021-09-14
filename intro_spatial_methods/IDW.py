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


def main():

    # filename1 = "camera_orientation_info.txt"
    # read_camera_orientation_info(filename1)
    read_laserdata()

    # filename2 = "laserdata.txt"
    # read_laserdata(filename2)


main()