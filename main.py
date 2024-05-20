import numpy as np
from math import floor

import utils
from data_encoder import DataEncoder, make_format_ecc
import constants


class Error(Exception):

    def mask_key_error(self, mask_no):
        print("NO masks found for mask no: %s" % mask_no)
        print("EXITING.")
        exit()


def mask_it(r, c, mask_no, bit):
    """
    Used for masking data. One bit at a time . A loop must be used to iterate ,
    the function doesn't iterate on its own.
    """
    flip = lambda x: 0 if x else 1
    MASKS = {
        0: bit if (r + c) % 2 else flip(bit),
        1: bit if r % 2 else flip(bit),
        2: bit if (c) % 3 else flip(bit),
        3: bit if (r + c) % 3 else flip(bit),
        4: bit if ((floor(r / 2) + floor(c / 3)) % 2) else flip(bit),
        5: bit if ((r * c) % 2) + ((r * c) % 3) else flip(bit),
        6: bit if (((r * c) % 2) + ((r * c) % 3)) % 2 else flip(bit),
        7: bit if (((r + c) % 2) + ((r * c) % 3)) % 2 else flip(bit),
    }
    try:
        return MASKS[mask_no]
    except KeyError:
        raise Error().mask_key_error(mask_no)


ALIGNMENT_PATTERN_POS = [
    (),
    (),
    (6, 18),
    (6, 22),
    (6, 26),
    (6, 30),
    (6, 34),
    (6, 22, 38),
    (6, 24, 42),
    (6, 26, 46),
    (6, 28, 50),
    (6, 30, 54),
    (6, 32, 58),
    (6, 34, 62),
    (6, 26, 46, 66),
    (6, 26, 48, 70),
    (6, 26, 50, 74),
    (6, 30, 54, 78),
    (6, 30, 56, 82),
    (6, 30, 58, 86),
    (6, 34, 62, 90),
    (6, 28, 50, 72, 94),
    (6, 26, 50, 74, 98),
    (6, 30, 54, 78, 102),
    (6, 28, 54, 80, 106),
    (6, 32, 58, 84, 110),
    (6, 30, 58, 86, 114),
    (6, 34, 62, 90, 118),
    (6, 26, 50, 74, 98, 122),
    (6, 30, 54, 78, 102, 126),
    (6, 26, 52, 78, 104, 130),
    (6, 30, 56, 82, 108, 134),
    (6, 34, 60, 86, 112, 138),
    (6, 30, 58, 86, 114, 142),
    (6, 34, 62, 90, 118, 146),
    (6, 30, 54, 78, 102, 126, 150),
    (6, 24, 50, 76, 102, 128, 154),
    (6, 28, 54, 80, 106, 132, 158),
    (6, 32, 58, 84, 110, 136, 162),
    (6, 26, 54, 82, 110, 138, 166),
    (6, 30, 58, 86, 114, 142, 170),
]

ALIGNMENT_PATTERN = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]


class QR:

    def __init__(self, version=None, ecl=None, mask=None, mode=None):
        self.version = version
        self.mask = mask
        self.ecl = ecl
        self.data = None  # raw binary data
        self.mode = None
        self.size = None  # get_version_size(version) if version else None
        self.qr = None
        self.inp_data = None

    ##################################
    # - TODO make align pattern for every version
    def create_template(self):
        """
        Creates a template of the required size of the qr code.
        The fixed areas like finders, timing patterns,etc are represented by 0s and remaining by 1s.
        """
        qr = np.ones(self.size)
        # self.qr = qr

        fil_val = 0
        fx, fy = 8, 8
        finder = np.zeros([fx, fy])

        # finders with space
        qr[:fx, :fy] = finder  # top_left
        qr[:fx, -fy:] = finder  # top_right
        qr[-fx:, :fy] = finder  # bottom_left

        # format info
        # p.s.: IGNORE their placenents comments they might be wrong.
        qr[8, -8:] = [fil_val] * 8  # top_right_horizontal
        qr[8, :8] = [fil_val] * 8  # top_left_horizontal
        qr[8, 8] = fil_val
        qr[:8, 8] = [fil_val] * 8  # top_left_vertical
        qr[-8:, 8] = [fil_val] * 8  # botton_left vertical

        # timings
        timing_arr = [fil_val] * (self.size[0] - 16)
        qr[8:-8, 6] = timing_arr  # vertical
        qr[6, 8:-8] = timing_arr  # horizontal

        qr = self.place_alignments(qr, np.zeros((5, 5)))

        if self.version >= 7:
            qr = self.place_version_info(self.version, is_template=True, template=qr)

        return qr

    def place_mask(self):
        """
        Apply the specified mask to QR code.
        """
        mask_type = self.mask
        for r in range(self.w):
            for c in range(self.h):
                if self.template[r, c]:
                    self.qr[r, c] = mask_it(r, c, mask_type, self.qr[r, c])

    def place_finders(self):
        """
        Place finder patterns in the QR code.
        """
        finder = np.array(
            [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
        )

        self.qr[:7, :7] = finder  # top_left
        self.qr[:7, -7:] = finder  # top_right
        self.qr[-7:, :7] = finder  # bottom_left

    def place_timings(self):
        """
        Place timing patterns in the QR code.
        """
        timing_size = self.h - 16
        timing_arr = utils.alternating_arr(timing_size, self.h)
        self.qr[8:-8, 6] = timing_arr  # vertical
        self.qr[6, 8:-8] = timing_arr  # Horizontal

    # -TODO dynamically place alignment patterns
    def place_alignments(self, qr, pattern):
        """
        Place specified alignment patterns in the QR code / Template .
        """
        if not self.version == 1:
            from itertools import product

            # Generate combinations
            positions = list(product(ALIGNMENT_PATTERN_POS[self.version], repeat=2))

            for r, c in positions:
                # avoid finder patterns
                if (r, c) == (6, 6):
                    continue
                if r > (self.w - 8) and c == 6:
                    continue
                if r == 6 and c > (self.h - 8):
                    continue

                # place template/pattern in their respective positions
                qr[r - 2 : r + 3, c - 2 : c + 3] = pattern

        return qr

    def place_version_info(self, version, is_template=False, template=None):
        """
        Place version info in the qr
        """
        if is_template:
            vstring = np.zeros((6, 3))
            template[:6, -11:-8] = vstring  # top right
            template[-11:-8, :6] = vstring.T  # bottom left
            return template

        v_index = version - 7
        version_string = constants.VERSION_INFO_STRINGS[v_index][
            ::-1
        ]  # reverse FTM until changing constant
        vstring = [version_string[i : i + 3] for i in range(0, len(version_string), 3)]

        vstring = np.array(vstring)

        self.qr[:6, -11:-8] = vstring  # top right
        self.qr[-11:-8, :6] = vstring.T  # bottom left

        # return qr

    def place_format_info(self):
        """
        Place format info in the QR code.
        """
        # the masked encoded data for format info
        format_data = make_format_ecc(self.ecl, self.mask)

        # dividing data into two halves for placement
        ldat = format_data[:7]
        rdat = format_data[7:]

        # for the seperated riht and btm info
        self.qr[8, -8:] = rdat  # top_right_horizontal
        self.qr[-7:, 8] = ldat[::-1]  # botton_left vertical

        # for the left joined one
        rdat = rdat[::-1]
        self.qr[8, :6] = ldat[:6]
        self.qr[:6, 8] = rdat[:6]
        self.qr[7:9, 8] = rdat[-2:]
        self.qr[8, 7] = ldat[-1]

    def place_data(self):
        """
        Place data in QR code in snake/zigzag pattern.
        """
        qr = self.qr
        data = self.data

        go_left = lambda r, c: (r, c - 1)
        go_upright = lambda r, c: (r - 1, c + 1)
        go_downright = lambda r, c: (r + 1, c + 1)
        shift_col_left = lambda r, c: (r, c - 1)
        check = lambda r, c: self.template[r, c]
        # check = lambda r,c : not(qr[r,c])

        timing_pos = 6
        dat = 0
        r, c = self.w - 1, self.h - 1

        x, y = int((self.w - 1) / 2), self.h - 1

        # transverse columns , 2 at a time
        for col in range(x):

            # shift pointer to left if the column is the column of vertical timing data
            if c == timing_pos:
                r, c = shift_col_left(r, c)

            # transverse the qr up and down
            for row in range(y):

                # go up in zigzag pattern
                if col % 2 == 0:
                    # check if data can be placed here comparing with template
                    # if yes place data else skip
                    if check(r, c):
                        qr[r, c] = data[dat]
                        dat += 1

                    # go left check and place data
                    r, c = go_left(r, c)
                    if check(r, c):
                        qr[r, c] = data[dat]
                        dat += 1

                    # go up and right (diagonal) ↗
                    r, c = go_upright(r, c)
                    # print("uppppp",r,c)

                else:  # go down
                    # check and place data
                    if check(r, c):
                        qr[r, c] = data[dat]
                        dat += 1

                    # go left, check and place data
                    r, c = go_left(r, c)
                    if check(r, c):
                        qr[r, c] = data[dat]
                        dat += 1

                    # go down and right (↘)
                    r, c = go_downright(r, c)

                    # print("downnnnnn",r,c)

            # print(r,c)
            # transverse to the next column as well as place data ( ← ← )
            for _ in range(2):
                if check(r, c):
                    qr[r, c] = data[dat]
                    dat += 1
                r, c = go_left(r, c)

        self.qr = qr

    ###################################

    def create_qr(self, inp_data):
        """
        Create the QR code.
        """

        # analyze the input and determine params for qr.
        encoder = DataEncoder(mode=self.mode, version=self.version, ecl=self.ecl)
        (enc_data_params, enc_data) = encoder.encode_data(inp_data)

        # update attributes
        self.inp_data = inp_data
        self.version = enc_data_params["version"]
        self.mode = enc_data_params["mode"]
        self.ecl = enc_data_params["ecl"]
        self.size = utils.get_version_size(self.version)
        (self.w, self.h) = self.size

        # format encoded data from bytearray to bitstring

        self.data = "".join([utils.format2(i, "b", 8) for i in enc_data])
        self.data = (
            self.data + "0" * 8
        )  # NOTE : there are remainder bits specified in the standard ranging form (0-7)

        self.mask = 1  # for now

        # create template and initialize an empty qr
        self.template = self.create_template()
        self.qr = np.zeros(self.size)

        # create the QR
        self.place_data()
        self.place_mask()
        self.place_finders()
        self.place_timings()
        self.qr = self.place_alignments(self.qr, ALIGNMENT_PATTERN)
        self.place_version_info(self.version)
        self.place_format_info()

        return self.qr
        # return self.template

    # currently using matplotlib for testing out
    def show(self):
        levels = [0, 1]
        qrm = self.template
        qrm = self.qr

        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap

        fig, ax = plt.subplots(1, 1)

        my_cmap = ListedColormap(["white", "black"], "mcmap")
        # my_cmap = ListedColormap(["black","white"],"mcmap")

        ax.matshow(qrm, cmap=my_cmap)
        ax.set_title(f"QR CODE v{self.version}, ECL: {self.ecl}, MODE: {self.mode}")

        # plt.matshow(qrm)
        plt.show()

    def _adv_show(self, data=None, force=False, version=None, mode=None, ecl=None):
        levels = [0, 1]
        # temp = self.template
        # qrm = self.qr

        # update attributes
        self.version = version
        self.mode = mode
        self.ecl = ecl
        self.data = data

        print("version:", self.version)
        print("mode:", self.mode)
        print("ecl:", self.ecl)

        # self.mode=constants.NUM_MODE
        self.size = utils.get_version_size(self.version)
        (self.w, self.h) = self.size

        print("QR ATTRIBUTES", self.__getattribute__("version"))
        # create template and initialize an empty qr
        self.template = self.create_template()
        self.qr = np.zeros(self.size)

        self.mask = 1  # for now
        # create the QR
        self.place_data()
        self.place_mask()
        self.place_finders()
        self.place_timings()
        self.qr = self.place_alignments(self.qr, ALIGNMENT_PATTERN)
        self.place_version_info(self.version)
        self.place_format_info()

        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap

        # plt.title("Version:%i"%self.version)
        fig, axis = plt.subplots(1, 2)

        # p.mat

        my_cmap = ListedColormap(["white", "black"], "mcmap")

        axis[0].matshow(self.template)
        axis[0].set_title("Template")

        # For Cosine Function
        axis[1].matshow(self.qr, cmap=my_cmap)
        axis[1].set_title("QR CODE v%i" % self.version)

        plt.show()


if __name__ == "__main__":

    my_qr = QR()

    # qrm = my_qr.create_qr("ABCDEFGHIJKLMNOPQRSTUVWXYZ; "*20)
    # qrm = my_qr.create_qr("1234567890"*200)
    qrm = my_qr.create_qr("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    print(qrm)

    # my_qr._adv_show()
    my_qr.show()

    ################
    # NOTE: Workings and Implementation
    # How i want to implement usage:

    # 1
    # create instance of QR
    # adv .:  can give it mode,ecl,ver
    # qr = QR()

    # 2
    # create a qr code
    # qr.create_qr("input data")

    # automatically determines params that are not given by user (ecl,mode,version)
    # creates a qr code
    # NOTES / INFO :
    # calls DataEncoder
    # outputs qr data /alt./ show it like the ex. below  (qr saved in self.qr)

    # 3
    # show the qr / save it
    # qr.show()

    # NOTES / INFO
    # - TODO version to size, v/
    # - TODO total cwords,ecc syms
    # - TODO alignment  pattern
    # TODO mask rating and choosing
    # - TODO version info module placement for version>7
