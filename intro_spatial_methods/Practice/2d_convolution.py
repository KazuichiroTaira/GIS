import scipy
from scipy import signal


def main():
    f = [[2, 4, 1, 3],
         [2, 1, 4, 2],
         [4, 1, 3, 1]]

    h = [[1, 2, 3],
         [2, 3, 4],
         [3, 4, 5]]

    g = scipy.signal.convolve2d(f, h, mode='valid')

    """
    mode = valid means:
    The output consists only of those elements that 
    do not rely on the zero-padding. In ‘valid’ mode, 
    either in1 or in2 must be at least as large 
    as the other in every dimension.
    """

    # convolve2d(f, h, mode='full', boundary='fill', fillvalue=0)

    print(sum(g))


main()