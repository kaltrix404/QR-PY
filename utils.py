

import numpy as np

def alternating_arr(n,start=1):
    """
    Create array of alternating 1s and 0s
    """
    arr = np.zeros(n)
    arr[0 if start else 1::2] = 1
    return arr