import numpy as np
from error_correction import make_format_ecc
from math import floor
import utils


# print(utils.alternating_arr(10))
# exit()


class Error(Exception):
    # def __init__(self,code):
    #     self.code
    def mask_key_error(self,mask_no):
        print("NO masks found for mask no: %s"%mask_no)
        print("EXITING.")
        exit()
    

def mask_it(r,c,mask_no,bit):
    flip = lambda x : 0 if x else 1
    MASKS = { 0 : bit if (r+c)%2 else flip(bit),
              1 : bit if r%2 else flip(bit),
              2 : bit if (c) % 3 else flip(bit),
              3 : bit if (r + c) % 3 else flip(bit),
              4 : bit if (( floor(r / 2) + floor(c / 3) ) % 2 ) else flip(bit),
              5 : bit if ((r * c) % 2) + ((r * c) % 3)  else flip(bit),
              6 : bit if ( ((r * c) % 2) + ((r * c) % 3) ) % 2  else flip(bit),
              7 : bit if ( ((r + c) % 2) + ((r * c) % 3) ) % 2  else flip(bit)}
    try :
        return MASKS[mask_no]
    except KeyError:
        raise Error().mask_key_error(mask_no)
    


class QR:

    VERSION_SIZES = {"v1":(21,21),
                      "v2":(25,25),
                      "v3":(29,29)

    }

    version_capabilities ={}

    def __init__(self,version=None,ecl=None,mask=None):
        self.version = version
        self.data = None
        self.mask = None
        self.ecl = None
        
        self.size = self.VERSION_SIZES[version]
        (self.w,self.h) = self.size

        self.template = self.create_template()
        self.qr = np.zeros(self.size)



    ##################################
    # TODO make align pattern for every version  
    def create_template(self):
            """
            Creates a template of the required size of the qr code.
            The fixed areas like finders, timing patterns,etc are represented by 0s and remaining by 1s.
            """
            qr = np.ones(self.size)
            # self.qr = qr

            fil_val = 0
            fx,fy=8,8
            finder = np.zeros([fx,fy])

            #finders with space
            qr[:fx,:fy] = finder #top_left
            qr[:fx,-fy:]  = finder #top_right
            qr[-fx:,:fy]  = finder #bottom_left

            #format info  
            #p.s.: IGNORE their placenents comments they might be wrong.
            qr[8,-8:] = [fil_val]*8 #top_right_horizontal
            qr[8,:8]  = [fil_val]*8 #top_left_horizontal
            qr[8,8] = fil_val
            qr[:8,8] = [fil_val]*8    #top_left_vertical
            qr[-8:,8] = [fil_val]*8 #botton_left vertical

            #timings
            timing_arr = [fil_val]*(self.size[0] -16)
            qr[8:-8,6] = timing_arr #vertical
            qr[6,8:-8] = timing_arr #horizontal

            #alignment pattern
            alx,aly=16,16
            qr[alx:alx+5,aly:aly+5] = np.zeros([5,5])

            return qr

    
    def place_mask(self):
        """
        Apply the specified mask to QR code.

        """
        mask_type = self.mask
        for r in range(self.w):
            for c in range(self.h):
                if self.template[r,c]:
                    self.qr[r,c]=mask_it(r,c,mask_type,self.qr[r,c])
        


    def place_finders(self):
        """
        Place finder patterns in the QR code.
        """
        finder = np.array([ [1,1,1,1,1,1,1],
                            [1,0,0,0,0,0,1],
                            [1,0,1,1,1,0,1],
                            [1,0,1,1,1,0,1],
                            [1,0,1,1,1,0,1],
                            [1,0,0,0,0,0,1],
                            [1,1,1,1,1,1,1] ])
        
        self.qr[:7,:7] = finder #top_left
        self.qr[:7,-7:]  = finder #top_right
        self.qr[-7:,:7]  = finder #bottom_left


    def place_timings(self):
        """
        Place timing patterns in the QR code.
        """
        timing_size = self.h - 16
        timing_arr = utils.alternating_arr(timing_size,self.h)
        self.qr[8:-8,6] = timing_arr #vertical
        self.qr[6,8:-8] = timing_arr #Horizontal


    #TODO dynamically place alignment patterns
    def place_alignments(self):
        """
        Place alignment patterns in the QR code
        """
        alignment_pattern = [[1,1,1,1,1],
                             [1,0,0,0,1],
                             [1,0,1,0,1],
                             [1,0,0,0,1],
                             [1,1,1,1,1]]
        x,y = 16,16
        self.qr[x:x+5,y:y+5] = alignment_pattern


    def place_format_info(self):
        """
        Place format info in the QR code.
        """
        #the masked encoded data for format info
        format_data = make_format_ecc(self.ecl,self.mask)

        #dividing data into two halves for placement
        ldat =format_data[:7]
        rdat =format_data[7:]

        # for the seperated riht and btm info
        self.qr[8,-8:] = rdat #top_right_horizontal
        self.qr[-7:,8] = ldat[::-1]#botton_left vertical

        # for the left joined one
        rdat=rdat[::-1]
        self.qr[8,:6]  = ldat[:6] 
        self.qr[:6,8] = rdat[:6]  
        self.qr[7:9,8] = rdat[-2:]
        self.qr[8,7]  = ldat[-1]  



    # def place_data(self):
    #     """
    #     Place data in QR code in snake/zigzag pattern.
    #     """
  
    #     go_left = lambda r,c: (r,c-1)
    #     go_upright = lambda r,c :(r-1, c+1)
    #     go_downright = lambda r,c :(r+1,c+1)
    #     shift_col_left = lambda r,c: (r,c-1)
    #     check = lambda r,c : self.template[r,c]

    #     timing_pos = 6
    #     dat=0
    #     r,c = self.w-1,self.h-1

    #     x,y = int((self.w-1)/2),self.h-1
        
    #     for col in range(x):
    #         # print("colllllllllll",col)
    #         if c==timing_pos:
    #             r,c=shift_col_left(r,c)

    
    #         for row in range(y):

    #             if col%2==0:       
    #                 free = check(r,c)
    #                 if free:
    #                     self.qr[r,c]=self.data[dat]
    #                     dat+=1

    #                 r,c=go_left(r,c)
                    

    #                 if check(r,c):
    #                     self.qr[r,c]=self.data[dat]
    #                     dat+=1

    #                 r,c=go_upright(r,c)
    #                 print("uppppp",r,c)

    #             else :
                    
    #                 free = check(r,c)
    #                 if free:
    #                     self.qr[r,c] = self.data[dat]
    #                     dat+=1

    #                 r,c=go_left(r,c)
    #                 if check(r,c):
    #                     self.qr[r,c] = self.data[dat]
    #                     dat+=1

    #                 r,c=go_downright(r,c)

    #                 print("downnnnnn",r,c)

    #         print(r,c)
     
    #         if check(r,c):
    #             self.qr[r,c ]= self.data[dat]
    #             dat+=1
    #         r,c=go_left(r,c)
    #         if check(r,c):
    #             self.qr[r,c] = self.data[dat]
    #             dat+=1
    #         r,c=go_left(r,c)
        
    def place_data(self):
        """
        Place data in QR code in snake/zigzag pattern.
        """
        qr= self.qr
        data = self.data

        go_left = lambda r,c: (r,c-1)
        go_upright = lambda r,c :(r-1, c+1)
        go_downright = lambda r,c :(r+1,c+1)
        shift_col_left = lambda r,c: (r,c-1)
        check = lambda r,c : self.template[r,c]
        # check = lambda r,c : not(qr[r,c])

        timing_pos = 6
        dat=0
        r,c = self.w-1,self.h-1

        x,y = int((self.w-1)/2),self.h-1
        
        #transverse columns , 2 at a time
        for col in range(x):

            #shift pointer to left if the column is the column of vertical timing data
            if c==timing_pos:
                r,c=shift_col_left(r,c)

            # transverse the qr up and down
            for row in range(y):
                
                # go up in zigzag pattern
                if col%2==0:     
                    # check if data can be placed here comparing with template  
                    # if yes place data else skip
                    if check(r,c):
                        qr[r,c]=data[dat]
                        dat+=1

                    #go left check and place data
                    r,c=go_left(r,c)
                    if check(r,c):
                        qr[r,c]= data[dat]
                        dat+=1

                    #go up and right (diagonal) ↗
                    r,c=go_upright(r,c)
                    print("uppppp",r,c)

                
                else :# go down
                    #check and place data
                    if check(r,c):
                        qr[r,c]=data[dat]
                        dat+=1

                    #go left, check and place data
                    r,c=go_left(r,c)
                    if check(r,c):
                        qr[r,c]= data[dat]
                        dat+=1

                    #go down and right (↘)
                    r,c=go_downright(r,c)

                    print("downnnnnn",r,c)

            print(r,c)
            #transverse to the next column as well as place data ( ← ← )
            for _ in range(2):
                if check(r,c):
                    qr[r,c]= data[dat]
                    dat+=1
                r,c=go_left(r,c)


            # if check(r,c):
            #     qr[r,c]= data[dat]
            #     dat+=1
            # r,c=go_left(r,c)
            # if check(r,c):
            #     qr[r,c]= data[dat]
            #     dat+=1
            # r,c=go_left(r,c)
        
        self.qr = qr


    ###################################


    def create_qr(self,data):
        """
        Create the QR code.
        """

        data = "0010000001011011000010110111100011010001011100101101110001001101010000110100000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111110000011000010111010000100110000001001101100101101001010000011000100110000110"
        self.data=data+"0"*20
  
        self.mask = 1
        self.ecl = 1

        self.place_data()
        self.place_mask()
        
        self.place_finders()
        self.place_timings()
        self.place_alignments()
        self.place_format_info()


        return self.qr
        # return self.template
    









my_qr = QR("v2")

qrm = my_qr.create_qr("HELLO WORLD")
print(qrm)

# flip = lambda x : 0 if x else 1
# qrm = [[flip(i) for i in j] for j in qrm]

levels=[0,1]

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

my_cmap = ListedColormap(["white","black"],"mcmap")
# my_cmap = ListedColormap(["black","white"],"mcmap")
plt.matshow(qrm,cmap=my_cmap)
# plt.matshow(qrm)
plt.show()


