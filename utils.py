import numpy as np


# def rate_masks(masks):
#     for masks in masks:




def alternating_arr(n, start=1):
    """
    Create array of alternating 1s and 0s
    """
    arr = np.zeros(n)
    arr[0 if start else 1 :: 2] = 1
    return arr


def format2(i, type, length, pad="left"):
    """
    Format int to binary string with padding to make it of specified length.
    """
    val = format(i, type)

    if len(val) > length:
        print("length less than bits required for the int, ignoring length")
        return val

    pad_bits = "0" * (length - len(val))
    res = pad_bits + val if pad == "left" else val + pad_bits

    return res


def get_version_size(v):
    """
    Returns size of QR (w,h)
    """
    s = (4 * v) + 17
    return (s, s)


def bin2x(bin, res_type="x"):
    """Binary string to list of int/hex

    Args:
        bin (str): Binary string to convert
        res_type (str, optional): output in ( x = hex | i = int). Defaults to "x".

    Raises:
        NotImplementedError: the output type isn't implemented currently.

    Returns:
        list : List of res_type converted from input binary string.
    """
    # NOTE remainder bits that dont fit into a byte are discarded
    res = []
    if res_type == "x":
        res = [hex(int(bin[i : i + 8], 2)) for i in range(0, len(bin), 8)]
    elif res_type == "i":
        res = [int(bin[i : i + 8], 2) for i in range(0, len(bin), 8)]
    else:
        raise NotImplementedError

    return res


if __name__ == "__main__":
    print(bin2x("00000000111111111111", "i"))
