import utils 
from reedsolo import RSCodec
import constants



LOGS ={}
def log(tup,p=None):
    global LOGS
    LOGS[tup[0]] = tup[1]
    if p:
        print(tup[0],":",tup[1])

    


def undefined_mode(mode,*args):
    print("UNsupported mode %s"%str(mode))
    for i in args:
        print(i)
    exit()



def char_count_bits(mode,version):
    """
    Determine the number of bits required to encode len of characters for repective mode and versions. 
    """
    # numerical
    if mode == constants.NUM_MODE:
        if ( 1 <= version <= 9  ) : return 10
        elif (10 <= version <=  26) : return 12
        elif (27 <= version <= 40 ) : return 14
        else : print("Version error : %s"%version)

    # alnum
    elif mode == constants.ALconstants.NUM_MODE:
        if ( 1 <= version <= 9  ) : return 9
        elif (10 <= version <=  26) : return 11
        elif (27 <= version <= 40 ) : return 13
        else : print("Version error : %s"%version)

    #byte
    elif mode == constants.BYTE_MODE :
        if ( 1 <= version <= 9  ) : return 8
        elif (10 <= version <=  26) : return 16
        elif (27 <= version <= 40 ) : return 16
        else : print("Version error : %s"%version)

    else :
        undefined_mode(mode,"from char count bits")





class DataEncoder:

    def __init__(self,mode=None,version=None,ecl=None):
        self.mode = mode
        self.data = None
        self.version =version
        self.ecl = constants.DEFAULT_ECL if ecl == None else ecl


    def segment_data(self,data,mode,chars_len):
        print("mmmmm",mode==constants.ALNUM_MODE,chars_len)
        seg_data = ""

        if mode == constants.NUM_MODE: 
            # group 3 digits as a single value ans encode it 
            for i in range(0,chars_len-2,3):
                value = int(data[i:i+3])
                seg_data += utils.format2(value,"b",10)

            # exception when data doesnt get perfectly paired up in groups of three
            rem = chars_len % 3
            if rem :
                #7 bits long if 2 digits remaining 
                # else 4 bits long if 1 digit remainig
                f = lambda x: (3*x)+1  
                seg_data += utils.format2(int(data[-rem:]),"b",f(rem))
            

        elif mode == constants.ALconstants.NUM_MODE:
            print("here")
            #segment and encode the data :
            #Two chars are coded in an 11-bit value by this formula: Value = 45 × C1 + C2
            #This has the exception that the last character in an alphanumeric string with an odd length is read as a 6-bit value instead.
            for i in range(0,chars_len-1,2): # self-note: (-1) for a reason #
                #pair and encode 
                C1,C2 = constants.ALPHANUMS[data[i]], constants.ALPHANUMS[data[i+1]]
                value = (45 * C1) + C2
                seg_data += utils.format2(value,"b",11)
            # odd length exception
            if chars_len % 2 :
                seg_data += utils.format2(constants.ALPHANUMS[data[-1]],"b",6)

        elif mode == constants.BYTE_MODE:
            #represent every character by a 8 bit binary string
            for char in data:
                seg_data += utils.format2(bin(ord(char)),"b",8)
        else:
            undefined_mode(mode,"From segmentation")
        
        print("sesss",seg_data)
        return seg_data

    def pad_seg_data(self,mode,version,ecl,seg_data):
        """
        Pad the encoded seg_data to fill empty spaces as required with special bytes xEC and x11.
        Also adds the terminator after segmented seg_data.
        """
        total_bits = len(seg_data) #current len of seg_data

        #required len of seg_data
        if mode == constants.NUM_MODE:
            total_bits_req = constants.NUM_CWORD_CAP[ecl][version]*8
        elif mode == constants.ALconstants.NUM_MODE:
            total_bits_req = constants.ALconstants.NUM_CWORD_CAP[ecl][version]*8
        elif mode == constants.BYTE_MODE:
            total_bits_req = constants.BYTE_CWORD_CAP[ecl][version]*8
        else:
            undefined_mode(mode,"From pad_seg_data")


        #add_terminator nibble; all four 0s if there is space else only that fit
        if total_bits+4>total_bits_req:
            seg_data += "0"*(total_bits_req-total_bits)
        else:
            seg_data += "0000"

        #padding to make seg_data a multiple of bit 
        rem = len(seg_data)%8 
        if rem:
            seg_data += '0'*(8-rem)


        #add special (x11, xEC) pad bytes if there is extra left space 
        PA,PB="00010001","11101100"    #x11,xEC

        bytes_req = int((total_bits_req-len(seg_data))/8)
        for i in range(bytes_req):
            if i%2:
                seg_data+=PA
            else:
                seg_data+=PB
        
        return seg_data


    def divide_into_blocks(self,data,ecl,mode):
        v_index  = self.version
        blk_specs = constants.BLOCKS[mode][v_index]
        print(blk_specs)

    def calculate_ecc(self,enc_data):
        """
        Calculates the ecc for data
        """
        #convert data from string of bits to array on bytes represented as ints
        enc_data = [int(enc_data[i:i+8],2) for i in range(0,len(enc_data),8)]
        print(enc_data)

        #TODO dynamcially generate
        nsym = 10 #no_of symbols
        
        rsc = RSCodec(10)

        ecc_data = rsc.encode(enc_data)

        print(f"ecc raw ({len(ecc_data)})>>",ecc_data)

        # covert ecc bytearray to sting of bits
        res = "".join([utils.format2(byte,"b",8) for byte in ecc_data ])

        print("kkk",ecc_data[0])


        return res



    def encode_data(self,data):
        self.data =  data

        #analyze input data 
        recommended_params = self.analyze_input_data(self.data,ecl=self.ecl,version=self.version,mode=self.mode)


        #update the undefined params with params received by analyzing input
        self.version = recommended_params['version']
        self.mode = recommended_params['mode']
        self.ecl = recommended_params['ecl']



        log(('Data : ',self.data),p=1)
        log(('Mode : ',self.mode),p=1)
        log(('Version : ',self.version),p=1)
        log((' ECL : ',self.ecl),p=1)

        #no of characteras in data
        chars_len = len(data)

        #segment the data 
        seg_data = self.segment_data(data,self.mode,chars_len)
        log((f"Seg data ({len(seg_data)})",seg_data),p=1)

        # add mode and char count info
        mode_indicator = constants.MODE_INDICATORS[self.mode] 
        no_of_chars    = utils.format2(chars_len,"b",char_count_bits(self.mode,self.version))
        seg_data =  mode_indicator + no_of_chars + seg_data

        #add terminator + pad the data if necessary
        padded_data = self.pad_seg_data(self.mode,self.version,self.ecl,seg_data)
        log((f"Pad data ({len(padded_data)})",padded_data),p=1)

        self.divide_into_blocks(padded_data,self.ecl,self.mode)

        # add the ecc
        eccd_data = self.calculate_ecc(padded_data)
        log((f"ECCd({len(eccd_data)}):",eccd_data),p=1)

 
        return (recommended_params,eccd_data)


        


        # no segmentation currently
        #TODO one an specifytheir own func to analyze data than this default one
    def analyze_input_data(self,inp,ecl=None,mode=None,version=None):
        """
        Analyze the input data and select the best params for encoding data.
        Is independent from the params given while initializing the class.
        Automatically used to generate params not given while initializing the class.
        May or may not be used independently to analyse input data.
        """
        
        def choose_mode(inp_str):
            # data only contains nums
            if inp_str.isnumeric():
                return constants.NUM_MODE
            
            # if data not in constants.alphanums set resort to byte mode()
            for i in inp_str:
                if i not in constants.ALPHANUMS.keys():
                    return constants.BYTE_MODE
            return constants.ALconstants.NUM_MODE

        # left to figure out on what basis to choose ecl #TODO
        def chooose_ecl():
            return constants.ECC_L

        def choose_version(mode,data_len,ecl):
            #get the req. capabilities table dat for specified ecl.
            if mode == constants.NUM_MODE :
                cap = constants.NUM_CWORD_CAP[ecl]
            elif mode == constants.ALconstants.NUM_MODE: 
                cap = constants.ALconstants.NUM_CWORD_CAP[ecl]
            elif mode == constants.BYTE_MODE:
                cap = constants.BYTE_CWORD_CAP[ecl]
            else:
                print("UNKNOWN MODE : %s"%str(mode))
                exit()

            #return the version which has len just greater than data_len
            for ver in range(len(cap)): # 40 versions
                chars = cap[ver]
                if chars > data_len:
                    return ver

            #data len greater than max
            print("too much data %s"%data_len)
            exit()       

        #if data cant be fit into the mode 

        #analyze input data 
        if mode == None:
            mode = choose_mode(inp)
            log(("(A)MODE",mode),p=1)
            # print("MODE :%s"%str(mode))
        if ecl == None:
            ecl = chooose_ecl()
            log(("(A)ECL",ecl),p=1)
        if version == None:
            version = choose_version(mode,len(inp),ecl)
            log(("(A)Version",version),p=1)
        
        return {'ecl':ecl,'mode':mode,'version':version}
    







def make_format_ecc(ecl,mask_type):
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

    def foo(ecl,mask_type):

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
    
    return foo(ecl,mask_type)



if __name__ == "__main__":
    v = 2
    de = DataEncoder()
    # data = de.analyze_input_data("HELLO WORLD")
    # 
    (_,data) = de.encode_data("12345678902345767845634737467")
    print(data,len(data))



    # exit()

    # data = "0010000001011001110111011000010001100000101111000101100111111011100110100100000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000100000101110111010100001110111111011100101111101000001101110011101011100001010011"
    data=data+"0"*30
    # print(len(data))
    # exit()

    from main import QR
    my_qr = QR(v)



#TODO /NOTES
#
# Byte mode err
# data len err if more data then v2
# 



# ECC Level	Mask Pattern	Type Information Bits
# L	0	111011111000100
# L	1	111001011110011
# L	2	111110110101010
# L	3	111100010011101
# L	4	110011000101111
# L	5	110001100011000
# L	6	110110001000001
# L	7	110100101110110
# M	0	101010000010010
# M	1	101000100100101
# M	2	101111001111100
# M	3	101101101001011
# M	4	100010111111001
# M	5	100000011001110
# M	6	100111110010111
# M	7	100101010100000
# Q	0	011010101011111
# Q	1	011000001101000
# Q	2	011111100110001
# Q	3	011101000000110
# Q	4	010010010110100
# Q	5	010000110000011
# Q	6	010111011011010
# Q	7	010101111101101
# H	0	001011010001001
# H	1	001001110111110
# H	2	001110011100111
# H	3	001100111010000
# H	4	000011101100010
# H	5	000001001010101
# H	6	000110100001100
# H	7	000100000111011
# About Version Information Strings

