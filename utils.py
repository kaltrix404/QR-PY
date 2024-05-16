import numpy as np

def alternating_arr(n,start=1):
    """
    Create array of alternating 1s and 0s
    """
    arr = np.zeros(n)
    arr[0 if start else 1::2] = 1
    return arr

def format2(i,type,length,pad="left"):
    """
    Format int to binary string with padding to make it of specified length. 
    """
    val = format(i,type)

    if len(val) > length : print("length less than bits required for the int, ignoring length");return val 
    
    pad_bits = "0"*(length -len(val))
    res = pad_bits + val if pad=="left" else val + pad_bits

    return res
