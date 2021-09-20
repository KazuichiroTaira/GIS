import numpy as np


def main():
    h = [1, 2, -1]
    f = [4, 1, 2, 5]

    linear_convolution = np.convolve(h, f, mode="full")
    print(linear_convolution)


main()

"""
出来たら嬉しい！！
"""