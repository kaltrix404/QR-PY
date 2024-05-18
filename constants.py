


#Error Correctin levels
ECC_L = 1
ECC_M = 0
ECC_Q = 3
ECC_H = 2

#Default ecc
DEFAULT_ECL = ECC_L

#Encoding modes
NUM_MODE = 1
ALNUM_MODE = 2
BYTE_MODE = 4

#Mode indicators
MODE_INDICATORS={
    NUM_MODE : "0001",
    ALNUM_MODE : "0010" ,
    BYTE_MODE : "0100"
}


#no of bits for each mode 
CHAR_BITS ={
    NUM_MODE : 10 ,# bits for 3                                                                   
    ALNUM_MODE : 11 ,# bits for 2 
    BYTE_MODE : 8 # bits for 1

}

#Alphanumeric character set
ALPHANUMS = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
    "A":10,"B":11,"C":12,"D":13,"E":14,"F":15,"G":16,"H":17,"I":18,"J":19,"K":20,"L":21,
    "M":22,"N":23,"O":24,"P":25,"Q":26,"R":27,"S":28,"T":29,"U":30,"V":31,"W":32,"X":33,"Y":34,
    "Z":35," ":36, "$":37,"%":38,"*":39,"+":40,"-":41,".":42,"/":43,":":44}



##############Codeword capabilities ##################
# 1 CWORD (codeword) = 8 bytes

#Format = { ECC_level : [v0 ,v1 ,v2 ...  ] ... }
#NOTE : v0 = 0 is a placeholder.(may be used for micro qr code)

BYTE_CWORD_CAP ={
    ECC_L: [0,
        19, 34, 55, 80, 108, 136, 156, 194, 232, 274,
        324, 370, 428, 461, 523, 589, 647, 721, 795, 861,
        932, 1006, 1094, 1174, 1276, 1370, 1468, 1531, 1631, 1735,
        1843, 1955, 2071, 2191, 2306, 2434, 2566, 2702, 2812, 2956
    ],
    ECC_M: [0,
        16, 28, 44, 64, 86, 108, 124, 154, 182, 216,
        254, 290, 334, 365, 415, 453, 507, 563, 627, 669,
        714, 782, 860, 914, 1000, 1062, 1128, 1193, 1267, 1373,
        1455, 1541, 1631, 1725, 1812, 1914, 1992, 2102, 2216, 2334
    ],
    ECC_Q: [0,
        13, 22, 34, 48, 62, 76, 88, 110, 132, 154,
        180, 206, 244, 261, 295, 325, 367, 397, 445, 485,
        512, 568, 614, 664, 718, 754, 808, 871, 911, 985,
        1033, 1115, 1171, 1231, 1286, 1354, 1426, 1502, 1582, 1666
    ],
    ECC_H: [0,
        9, 16, 26, 36, 46, 60, 66, 86, 100, 122,
        140, 158, 180, 197, 223, 253, 283, 313, 341, 385,
        406, 442, 464, 514, 538, 596, 628, 661, 701, 745,
        793, 845, 901, 961, 986, 1054, 1096, 1142, 1222, 1276
    ]
}


ALNUM_CWORD_CAP = {
    ECC_L: [0,
        19, 34, 55, 80, 108, 136, 156, 194, 232, 274,
        324, 370, 428, 461, 523, 589, 647, 721, 795, 861,
        932, 1006, 1094, 1174, 1276, 1370, 1468, 1531, 1631, 1735,
        1843, 1955, 2071, 2191, 2306, 2434, 2566, 2702, 2812, 2956
    ],
    ECC_M: [0,
        16, 28, 44, 64, 86, 108, 124, 154, 182, 216,
        254, 290, 334, 365, 415, 453, 507, 563, 627, 669,
        714, 782, 860, 914, 1000, 1062, 1128, 1193, 1267, 1373,
        1455, 1541, 1631, 1725, 1812, 1914, 1992, 2102, 2216, 2334
    ],
    ECC_Q: [0,
        13, 22, 34, 48, 62, 76, 88, 110, 132, 154,
        180, 206, 244, 261, 295, 325, 367, 397, 445, 485,
        512, 568, 614, 664, 718, 754, 808, 871, 911, 985,
        1033, 1115, 1171, 1231, 1286, 1354, 1426, 1502, 1582, 1666
    ],
    ECC_H: [0,
        9, 16, 26, 36, 46, 60, 66, 86, 100, 122,
        140, 158, 180, 197, 223, 253, 283, 313, 341, 385,
        406, 442, 464, 514, 538, 596, 628, 661, 701, 745,
        793, 845, 901, 961, 986, 1054, 1096, 1142, 1222, 1276
    ]
}


NUM_CWORD_CAP = {
    ECC_L: [0,
        19, 34, 55, 80, 108, 136, 156, 194, 232, 274,
        324, 370, 428, 461, 523, 589, 647, 721, 795, 861,
        932, 1006, 1094, 1174, 1276, 1370, 1468, 1531, 1631, 1735,
        1843, 1955, 2071, 2191, 2306, 2434, 2566, 2702, 2812, 2956
    ],
    ECC_M: [0,
        16, 28, 44, 64, 86, 108, 124, 154, 182, 216,
        254, 290, 334, 365, 415, 453, 507, 563, 627, 669,
        714, 782, 860, 914, 1000, 1062, 1128, 1193, 1267, 1373,
        1455, 1541, 1631, 1725, 1812, 1914, 1992, 2102, 2216, 2334
    ],
    ECC_Q: [0,
        13, 22, 34, 48, 62, 76, 88, 110, 132, 154,
        180, 206, 244, 261, 295, 325, 367, 397, 445, 485,
        512, 568, 614, 664, 718, 754, 808, 871, 911, 985,
        1033, 1115, 1171, 1231, 1286, 1354, 1426, 1502, 1582, 1666
    ],
    ECC_H: [0,
        9, 16, 26, 36, 46, 60, 66, 86, 100, 122,
        140, 158, 180, 197, 223, 253, 283, 313, 341, 385,
        406, 442, 464, 514, 538, 596, 628, 661, 701, 745,
        793, 845, 901, 961, 986, 1054, 1096, 1142, 1222, 1276
    ]
}

########################################################











############ Version info module precomputed values ##########

                        # index = version - 7 ( ex: index for v8 = 8=7 = 1;  )
VERSION_INFO_STRINGS = [[0,0,0,1,1,1,1,1,0,0,1,0,0,1,0,1,0,0], #v7
                        [0,0,1,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0],
                        [0,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,0,1],
                        [0,0,1,0,1,0,0,1,0,0,1,1,0,1,0,0,1,1],
                        [0,0,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,0],
                        [0,0,1,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0],
                        [0,0,1,1,0,1,1,0,0,0,0,1,0,0,0,1,1,1],
                        [0,0,1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,1],
                        [0,0,1,1,1,1,1,0,0,1,0,0,1,0,1,0,0,0],
                        [0,1,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,0],
                        [0,1,0,0,0,1,0,1,0,0,0,1,0,1,1,1,0,1],
                        [0,1,0,0,1,0,1,0,1,0,0,0,0,1,0,1,1,1],
                        [0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,0,1,0],
                        [0,1,0,1,0,0,1,0,0,1,1,0,1,0,0,1,1,0],
                        [0,1,0,1,0,1,0,1,1,0,1,0,0,0,0,0,1,1],
                        [0,1,0,1,1,0,1,0,0,0,1,1,0,0,1,0,0,1],
                        [0,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,0,0],
                        [0,1,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,0],
                        [0,1,1,0,0,1,0,0,0,1,1,1,1,0,0,0,0,1],
                        [0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1],
                        [0,1,1,0,1,1,0,0,0,0,1,0,0,0,1,1,1,0],
                        [0,1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,1,0],
                        [0,1,1,1,0,1,0,0,1,1,0,0,1,1,1,1,1,1],
                        [0,1,1,1,1,0,1,1,0,1,0,1,1,1,0,1,0,1],
                        [0,1,1,1,1,1,0,0,1,0,0,1,0,1,0,0,0,0],
                        [1,0,0,0,0,0,1,0,0,1,1,1,0,1,0,1,0,1],
                        [1,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,0,0],
                        [1,0,0,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0],
                        [1,0,0,0,1,1,0,1,1,1,1,0,0,1,1,1,1,1],
                        [1,0,0,1,0,0,1,0,1,1,0,0,0,0,1,0,1,1],
                        [1,0,0,1,0,1,0,1,0,0,0,0,1,0,1,1,1,0],
                        [1,0,0,1,1,0,1,0,1,0,0,1,1,0,0,1,0,0],
                        [1,0,0,1,1,1,0,1,0,1,0,1,0,0,0,0,0,1],
                        [1,0,1,0,0,0,1,1,0,0,0,1,1,0,1,0,0,1]] #v40


######################################################################

##### GROUPS,BLOCKS , ECC ############

# key =  totalDC  ,  

BLOCKS = {
        ECC_L:[0,
            (19, 7, ((1, 19), (None, None))),
            (34, 10, ((1, 34), (None, None))),
            (55, 15, ((1, 55), (None, None))),
            (80, 20, ((1, 80), (None, None))),
            (108, 26, ((1, 108), (None, None))),
            (136, 18, ((2, 68), (None, None))),
            (156, 20, ((2, 78), (None, None))),
            (194, 24, ((2, 97), (None, None))),
            (232, 30, ((2, 116), (None, None))),
            (274, 18, ((2, 68), (2.0, 69.0))),
            (324, 20, ((4, 81), (None, None))),
            (370, 24, ((2, 92), (2.0, 93.0))),
            (428, 26, ((4, 107), (None, None))),
            (461, 30, ((3, 115), (1.0, 116.0))),
            (523, 22, ((5, 87), (1.0, 88.0))),
            (589, 24, ((5, 98), (1.0, 99.0))),
            (647, 28, ((1, 107), (5.0, 108.0))),
            (721, 30, ((5, 120), (1.0, 121.0))),
            (795, 28, ((3, 113), (4.0, 114.0))),
            (861, 28, ((3, 107), (5.0, 108.0))),
            (932, 28, ((4, 116), (4.0, 117.0))),
            (1006, 28, ((2, 111), (7.0, 112.0))),
            (1094, 30, ((4, 121), (5.0, 122.0))),
            (1174, 30, ((6, 117), (4.0, 118.0))),
            (1276, 26, ((8, 106), (4.0, 107.0))),
            (1370, 28, ((10, 114), (2.0, 115.0))),
            (1468, 30, ((8, 122), (4.0, 123.0))),
            (1531, 30, ((3, 117), (10.0, 118.0))),
            (1631, 30, ((7, 116), (7.0, 117.0))),
            (1735, 30, ((5, 115), (10.0, 116.0))),
            (1843, 30, ((13, 115), (3.0, 116.0))),
            (1955, 30, ((17, 115), (None, None))),
            (2071, 30, ((17, 115), (1.0, 116.0))),
            (2191, 30, ((13, 115), (6.0, 116.0))),
            (2306, 30, ((12, 121), (7.0, 122.0))),
            (2434, 30, ((6, 121), (14.0, 122.0))),
            (2566, 30, ((17, 122), (4.0, 123.0))),
            (2702, 30, ((4, 122), (18.0, 123.0))),
            (2812, 30, ((20, 117), (4.0, 118.0))),
            (2956, 30, ((19, 118), (6.0, 119.0)))],
    ECC_M:[0,
        (16,10,((1,16),(None,None))),
        (28,16,((1,28),(None,None))),
        (44,26,((1,44),(None,None))),
        (64,18,((2,32),(None,None))),
        (86,24,((2,43),(None,None))),
        (108,16,((4,27),(None,None))),(124,18,
                ((4,31),(None,None))),(154,22,((2,38),(2.0,39.0))),(182,22,((3,36),(2.0,37.0))),(216,26,((4,43),(1.0,44.0))),(254,30,((1,50),(4.0,51.0))),(290,22,((6,36),(2.0,37.0))),(334,22,((8,37),(1.0,38.0))),(365,24,((4,40),(5.0,41.0))),(415,24,((5,41),(5.0,42.0))),(453,28,((7,45),(3.0,46.0))),(507,28,((10,46),(1.0,47.0))),(563,26,((9,43),(4.0,44.0))),(627,26,((3,44),(11.0,45.0))),(669,26,((3,41),(13.0,42.0))),(714,26,((17,42),(None,None))),(782,28,((17,46),(None,None))),(860,28,((4,47),(14.0,48.0))),(914,28,((6,45),(14.0,46.0))),(1000,28,((8,47),(13.0,48.0))),(1062,28,((19,46),(4.0,47.0))),(1128,28,((22,45),(3.0,46.0))),(1193,
                28,((3,45),(23.0,46.0))),(1267,28,((21,45),(7.0,46.0))),(1373,28,((19,47),(10.0,48.0))),(1455,28,((2,46),(29.0,47.0))),(1541,28,((10,46),(23.0,47.0))),(1631,28,((14,46),(21.0,47.0))),(1725,28,((14,46),(23.0,47.0))),(1812,28,((12,47),(26.0,48.0))),(1914,28,((6,47),(34.0,48.0))),(1992,28,((29,46),(14.0,47.0))),(2102,28,((13,46),(32.0,47.0))),(2216,28,((40,
                47),(7.0,48.0))),(2334,28,((18,47),(31.0,48.0)))],

    ECC_Q: [0,(13,13,((1,13),(None,None))),(22,
                22,((1,22),(None,None))),(34,18,((2,17),(None,None))),(48,26,((2,24),(None,None))),(62,18,((2,15),(2.0,16.0))),(76,24,((4,19),(None,None))),(88,18,((2,14),(4.0,15.0))),(110,22,((4,18),(2.0,19.0))),(132,20,((4,16),(4.0,17.0))),(154,24,((6,19),(2.0,20.0))),(180,28,((4,22),(4.0,23.0))),(206,26,((4,20),(6.0,21.0))),(244,24,((8,20),(4.0,21.0))),(261,20,((11,16),(5.0,17.0))),(295,30,((5,24),(7.0,25.0))),(325,24,((15,19),(2.0,20.0))),(367,28,((1,22),(15.0,23.0))),(397,28,((17,22),(1.0,23.0))),(445,26,((17,21),(4.0,22.0))),(485,30,((15,
                24),(5.0,25.0))),(512,28,((17,22),(6.0,23.0))),(568,30,((7,24),(16.0,25.0))),(614,30,((11,24),(14.0,25.0))),(664,30,((11,24),(16.0,25.0))),(718,30,((7,24),(22.0,25.0))),(754,28,
                ((28,22),(6.0,23.0))),(808,30,((8,23),(26.0,24.0))),(871,30,((4,24),(31.0,25.0))),(911,30,((1,23),(37.0,24.0))),(985,30,((15,24),(25.0,25.0))),(1033,30,((42,24),(1.0,25.0))),(1115,30,((10,24),(35.0,25.0))),(1171,30,((29,24),(19.0,25.0))),(1231,30,((44,24),(7.0,25.0))),(1286,30,((39,24),(14.0,25.0))),(1354,30,((46,24),(10.0,25.0))),(1426,30,((49,24),(10.0,25.0))),(1502,30,((48,24),(14.0,25.0))),(1582,30,((43,24),(22.0,25.0))),(1666,30,((34,24),(34.0,25.0)))],

    ECC_H: [  0,
            (9, 17, ((1, 9), (None, None))),
            (16, 28, ((1, 16), (None, None))),
            (26, 22, ((2, 13), (None, None))),
            (36, 16, ((4, 9), (None, None))),
            (46, 22, ((2, 11), (2.0, 12.0))),
            (60, 28, ((4, 15), (None, None))),
            (66, 26, ((4, 13), (1.0, 14.0))),
            (86, 26, ((4, 14), (2.0, 15.0))),
            (100, 24, ((4, 12), (4.0, 13.0))),
            (122, 28, ((6, 15), (2.0, 16.0))),
            (140, 24, ((3, 12), (8.0, 13.0))),
            (158, 28, ((7, 14), (4.0, 15.0))),
            (180, 22, ((12, 11), (4.0, 12.0))),
            (197, 24, ((11, 12), (5.0, 13.0))),
            (223, 24, ((11, 12), (7.0, 13.0))),
            (253, 30, ((3, 15), (13.0, 16.0))),
            (283, 28, ((2, 14), (17.0, 15.0))),
            (313, 28, ((2, 14), (19.0, 15.0))),
            (341, 26, ((9, 13), (16.0, 14.0))),
            (385, 28, ((15, 15), (10.0, 16.0))),
            (406, 30, ((19, 16), (6.0, 17.0))),
            (442, 24, ((34, 13), (None, None))),
            (464, 30, ((16, 15), (14.0, 16.0))),
            (514, 30, ((30, 16), (2.0, 17.0))),
            (538, 30, ((22, 15), (13.0, 16.0))),
            (596, 30, ((33, 16), (4.0, 17.0))),
            (628, 30, ((12, 15), (28.0, 16.0))),
            (661, 30, ((11, 15), (31.0, 16.0))),
            (701, 30, ((19, 15), (26.0, 16.0))),
            (745, 30, ((23, 15), (25.0, 16.0))),
            (793, 30, ((23, 15), (28.0, 16.0))),
            (845, 30, ((19, 15), (35.0, 16.0))),
            (901, 30, ((11, 15), (46.0, 16.0))),
            (961, 30, ((59, 16), (1.0, 17.0))),
            (986, 30, ((22, 15), (41.0, 16.0))),
            (1054, 30, ((2, 15), (64.0, 16.0))),
            (1096, 30, ((24, 15), (46.0, 16.0))),
            (1142, 30, ((42, 15), (32.0, 16.0))),
            (1222, 30, ((10, 15), (67.0, 16.0))),
            (1276, 30, ((20, 15), (61.0, 16.0)))]
}


# Version and EC Level	Total Number of Data Codewords for this Version and EC Level	EC Codewords Per Block	Number of Blocks in Group 1	Number of Data Codewords in Each of Group 1's Blocks	Number of Blocks in Group 2	Number of Data Codewords in Each of Group 2's Blocks	Total Data Codewords