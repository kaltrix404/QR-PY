import utils 
from reedsolo import RSCodec
from constants import *


PRINT_LOG = True
TEMP_P = 1

LOGS ={}
def log(tup,print_only=False,p=False):
    if print_only:
        print(tup)
        return 0

    global LOGS
    LOGS[tup[0]] = tup[1]

    if p:
        print(tup[0],":",tup[1])

def char_count_bits(mode,version):
    """
    Determine the number of bits required to encode len of characters for repective mode and versions. 
    """
    # numerical
    if mode == NUM_MODE:
        if ( 1 <= version <= 9  ) : return 10
        elif (10 <= version <=  26) : return 12
        elif (27 <= version <= 40 ) : return 14
        else : print("Version error : %s"%version)

    # alnum
    elif mode == ALNUM_MODE:
        if ( 1 <= version <= 9  ) : return 9
        elif (10 <= version <=  26) : return 11
        elif (27 <= version <= 40 ) : return 13
        else : print("Version error : %s"%version)

    #byte
    elif mode == BYTE_MODE :
        if ( 1 <= version <= 9  ) : return 8
        elif (10 <= version <=  26) : return 16
        elif (27 <= version <= 40 ) : return 16
        else : print("Version error : %s"%version)

    else :
        undefined_mode(mode,"from char count bits")
   


def undefined_mode(mode,*args):
    print("UNsupported mode %s"%str(mode))
    for i in args:
        print(i)
    exit()


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



class DataEncoder:

    def __init__(self,mode=None,version=None,ecl=None):
        self.mode = mode
        self.data = None
        self.version =version
        self.ecl = DEFAULT_ECL if ecl == None else ecl


    def segment_data(self,data,mode,chars_len):
        """
        Segment data according to QR specifications
        """
        
        log(f"Segmenting input : ",print_only=TEMP_P)

        seg_data = ""
        if mode == NUM_MODE: 
            # group 3 digits as a single value ans encode it 
            for i in range(0,chars_len-2,3):
                value = int(data[i:i+3])
                seg_data += utils.format2(value,"b",10)

                log(f"{i}. {value} -> {utils.format2(value,"b",10)}",print_only=TEMP_P)

            # exception when data doesnt get perfectly paired up in groups of three
            rem = chars_len % 3
            if rem :
                #7 bits long if 2 digits remaining 
                # else 4 bits long if 1 digit remainig
                f = lambda x: (3*x)+1  
                seg_data += utils.format2(int(data[-rem:]),"b",f(rem))

                log(f"rem. {data[-rem:]} -> {utils.format2(int(data[-rem:]),"b",f(rem))}",print_only=TEMP_P)
            

        elif mode == ALNUM_MODE:
            #segment and encode the data :
            #Two chars are coded in an 11-bit value by this formula: Value = 45 × C1 + C2
            #This has the exception that the last character in an alphanumeric string with an odd length is read as a 6-bit value instead.
            for i in range(0,chars_len-1,2): # self-note: (-1) for a reason #
                #pair and encode 
                C1,C2 = ALPHANUMS[data[i]], ALPHANUMS[data[i+1]]
                value = (45 * C1) + C2
                seg_data += utils.format2(value,"b",11)

                log(f"{i}. {value} -> {utils.format2(value,"b",11)}",print_only=TEMP_P)

            # odd length exception
            if chars_len % 2 :
                seg_data += utils.format2(ALPHANUMS[data[-1]],"b",6)

                log(f"rem. {data[-1]} -> {utils.format2(ALPHANUMS[data[-1]],"b",6)}",print_only=TEMP_P)



        elif mode == BYTE_MODE:
            #represent every character by a 8 bit binary string
            i=0
            for char in data:
                seg_data += utils.format2(ord(char),"b",8)

                i+=1
                log(f"{i}. {char} -> {utils.format2(ord(char),"b",8)}",print_only=TEMP_P)
        else:
            undefined_mode(mode,"ERROR : From segmentation")
        

        return seg_data




    def divide_into_blocks(self,data,ecl,mode):
        log(f"Dividing and interleaving data :",print_only=TEMP_P)

        def interleave(data):
            res = []
            total_blocks = len(data)
            for i in range(max([len(blk) for blk in data])):
                for b in range(total_blocks):
                    try:
                        cword=data[b][i]
                        res.append(cword)
                    except IndexError:
                        pass

            return res


        #determine the blocks and groups of respected version
        blk_specs = BLOCKS[ecl][self.version]

        #
        total_cwords = blk_specs[0]
        ec_cwords_per_block = blk_specs[1]
        
        groups = blk_specs[2]
        G1_blk_spec = groups[0]
        G2_blk_spec = groups[1]

        log(f"Block specs : {blk_specs}",print_only=TEMP_P)
        log(f"Total cword : {total_cwords}",print_only=TEMP_P)
        log(f"EC per block : {ec_cwords_per_block}",print_only=TEMP_P)
        log(f"Groups : {groups}",print_only=TEMP_P)
        print()
        

        DC=[]
        ECC=[]
        s = 0
        for group in groups:
            no_of_blks =  group[0] or 0
            DC_in_each_blk = group[1] or 0 

            for i in range(no_of_blks):
                dc = data[s:s+DC_in_each_blk]
                ecc = self.calculate_ecc(dc,ec_cwords_per_block,only_ecc=1)

                DC.append(dc)
                ECC.append(ecc)

                s+=DC_in_each_blk

                # log(f"Group {} ({len(seg_data)}) : {seg_data}",print_only=TEMP_P)



        #interleave data
        interleaved_DC =interleave(DC)
        interleaved_ECC =interleave(ECC)
        res = interleaved_DC + interleaved_ECC

        log(f"DC data ({len(interleaved_DC)}) : {interleaved_DC}",print_only=TEMP_P)
        print()
        log(f"ECC data ({len(interleaved_ECC)}) : {interleaved_ECC}",print_only=TEMP_P)
        print()

        return res

    
    def calculate_ecc(self,enc_data,nsym,only_ecc=False,):
        """
        Calculates the ecc for data
        """

        # enc_data = [int(enc_data[i:i+8],2) for i in range(0,len(enc_data),8)]
        # print(enc_data)


        nsym = 1 if nsym is None else nsym  #no_of symbols
        
        rsc = RSCodec(nsym)
        ecc_data = rsc.encode(enc_data)

        if only_ecc:
            return ecc_data[-nsym:]

        return ecc_data





    def pad_seg_data(self,mode,version,ecl,seg_data):
        """
        Pad the encoded seg_data to fill empty spaces as required with special bytes xEC and x11.
        Also adds the terminator after segmented seg_data.
        """
        total_bits = len(seg_data) #current len of seg_data

        #required len
        total_bytes_req = BLOCKS[ecl][version][0] #bytes

        #add_terminator nibble; all four 0s if there is space , else only that fit
        if total_bits + 4 > total_bytes_req*8 :
            seg_data += "0"*(total_bytes_req-total_bits)
        else:
            seg_data += "0000"


        #padding bit to make seg_data a multiple 8 
        rem = len(seg_data)%8 
        if rem:
            seg_data += '0'*(8-rem)

        #TODO use  bytearray in all  operations 
        #turn the data into byte array
        seg_data = utils.bin2x(seg_data,"i")#[ seg_data[i:i+8] for i in range(0,len(seg_data),8) ]
        
        
        #add special (xEC ,x11) pad bytes if there is extra left spa  
        pad_bytes_req = total_bytes_req - len(seg_data)
        for i in range(pad_bytes_req):
            if i%2:
                seg_data.append(17)    #x11       #second
            else:
                seg_data.append(236)   #xEC       #first

        
        return seg_data


    
    def encode_data(self,data):
        self.data =  data
        #analyze input data 
        recommended_params = self.analyze_input_data(self.data,ecl=self.ecl,version=self.version,mode=self.mode)


        #update the undefined params with params received by analyzing input
        self.version = recommended_params['version']
        self.mode = recommended_params['mode']
        self.ecl = recommended_params['ecl']

        log(f"Finalized params for QR generation : ",print_only=TEMP_P)
        log(('Data : ',self.data),p=1)
        log(('Mode : ',self.mode),p=1)
        log(('Version : ',self.version),p=1)
        log(('ECL : ',self.ecl),p=1)
        print()

        #no of characteras in data
        chars_len = len(data)

        #segment the data 
        seg_data = self.segment_data(data,self.mode,chars_len)
        log((f"Seg data ({len(seg_data)})",seg_data),print_only=1)
        print()

 
        # add mode and char count info
        mode_indicator = MODE_INDICATORS[self.mode] 
        no_of_chars    = utils.format2(chars_len,"b",char_count_bits(self.mode,self.version))
        seg_data =  mode_indicator + no_of_chars + seg_data

        log(f"Adding mode indication and char count: ",print_only=TEMP_P)
        log(f"MODE indicator  : {mode_indicator}",print_only=TEMP_P)
        log(f"Char count : {no_of_chars}",print_only=TEMP_P)
        log(f"Resulting data ({len(seg_data)}) : {seg_data}",print_only=TEMP_P)
        print()
        
        
        #add terminator + pad the data if necessary
        padded_data = self.pad_seg_data(self.mode,self.version,self.ecl,seg_data)
        log((f"Pad data ({len(padded_data)})",padded_data),p=1)
        print()

     
        eccd_data = self.divide_into_blocks(padded_data,self.ecl,self.mode)
        log(f"Final data ({len(eccd_data)}) : {eccd_data}",print_only=TEMP_P)
        print()

        

        return (recommended_params,eccd_data)




        # no segmentation currently
        #TODO one an specify their own func to analyze data than this default one
        #TODO notify user if given params are incompatible
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
                return NUM_MODE
            
            # if data not in alphanums set resort to byte mode()
            for i in inp_str:
                if i not in ALPHANUMS.keys():
                    return BYTE_MODE
            
            return ALNUM_MODE

        # left to figure out on what basis to choose ecl #TODO
        def chooose_ecl():
            return ECC_L

        def choose_version(mode,data_len,ecl):
            #get the req. capabilities table dat for specified ecl.
            if mode == NUM_MODE :
                cap = NUM_CWORD_CAP[ecl]
            elif mode == ALNUM_MODE: 
                cap = ALNUM_CWORD_CAP[ecl]
            elif mode == BYTE_MODE:
                cap = BYTE_CWORD_CAP[ecl]
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

        #TODO if data cant be fit into the mode 

        log(f"Analyzing input : {inp}",print_only=TEMP_P)
        #analyze input data 
        if mode == None:
            mode = choose_mode(inp)
            log(("(A)MODE",mode),p=1)

        if ecl == None:
            ecl = chooose_ecl()
            log(("(A)ECL",ecl),p=1)

        if version == None:
            version = choose_version(mode,len(inp),ecl)
            log(("(A)Version",version),p=1)

        print()
        
        return {'ecl':ecl,'mode':mode,'version':version}



from main import QR

if __name__ == "__main__":

    #tests
    v = 5
    de = DataEncoder()#version=v)
    # data = de.analyze_input_data("HELLO WORLD")
    # 
    (_,data) = de.encode_data("ABCDEFGHIJKLMNOPQRSTUVWXZ; "*4)
    data = "".join([utils.format2(i,"b",8) for i in data]) +  "0"*8

    print("DONE ENCODING DATA .NOW PLACING DATA")

    myqr=QR()._adv_show(data,version=_['version'],ecl=_['ecl'],mode=_['mode'],force=1)







