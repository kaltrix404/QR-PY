

FORMAT_MASK = [i for i in "101010000010010"]


len_bin = lambda x : len(bin(x)[2:])
bin_ = lambda x,strip=True: bin(x)[2:]
str_xor = lambda x,y : "0" if x==y else "1"
xor = lambda a,b :[ str_xor(a[i],b[i])  for i in range(min(len(a),len(b))) ]


def pad_bits(dat,l,right=False):
    if (l< len(dat)):
        print("LEN is less than dat length.")
        return dat
    
    pad = "0"*(l-len(dat))
    if right:
        return dat+pad
    else:
        return pad+dat



def m2d(data,poly):
    lp=len(poly)
    s = 0
    e = lp
    for i in range(5): #TOTAL - ECC = 15 - 11 = 4
        if data[s+i]=="0" :
            continue
        else:
            data[s+i:lp+i]=xor(data[s+i:lp+i],poly)
    return data[-10:]



def make_format_ecc(ecl,mask_type):

    poly=[i for i in "10100110111"]
    mask =[i for i in "101010000010010"]

    if ecl== 0 and mask_type==0:
        return mask

    msg = pad_bits(bin_(ecl),2) + pad_bits(bin_(mask_type),3)
    msg = [ i for i in msg]
    # print("msg:",msg)

    pmsg = msg + ["0"]*10
    # print("pad:",pmsg)

    ecc = m2d(pmsg,poly)
    # print("ecc:","".join(ecc))

    codeword = msg + ecc
    print("cwd:","".join(codeword))

    masked_cword = xor(codeword,mask)
    # print("msk:","".join(masked_cword))

    return masked_cword#"".join(masked_cword)


if __name__ == "__main__":
    print("".join(make_format_ecc(1,1)))
    print(xor("111001111000100",FORMAT_MASK))
    

    for i in [0,1,2,3]:
        for j in range(7):
            print(i,j,make_format_ecc(i,j))
            # foo(i,j)