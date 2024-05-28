# QR-PY 
QRPY, your friendly python QR code generator.

## Usage
Just run the main.py (see bottom of main.py for more info.)

Alternatively:
```python
from main import QR

# create instance of QR
qr = QR()

#optionally you could also specify params for qr generation
# qr = QR(version=3,ecl=1)

# create a qr code
qr.create_qr("Hello from qrpy.")

# show the qr / save it
qr.show()
```


# Parameters
## Modes
Currently supported modes.

| Mode id  |       Name     |       Allowed Chars    |            Note                 |
|----------|----------------|------------------------|---------------------------------|
|    `1`   | Numeric        | [0-9]                  | Number 0 to 9                   |
|    `2`   | Alphanumeric   | [A-Z]+[$%*+-./:]+Space | Uppercase + some special chars. |
|    `4`   | Byte           | ISO/IEC 8859-1         |All ISO specified.     |                                 |


## Error Correction Level (ECL)
|ECL id   | Name          |           Descripton                      |
|---------|---------------|-------------------------------------------|
| `ECC_L` | Low	     (L)  | 7% of data bytes can be restored.         |
| `ECC_M` | Medium   (M)  | 15% of data bytes can be restored.        |            
| `ECC_Q` | Quartile (Q)  | 25% of data bytes can be restored.        |        
| `ECC_H` | High     (H)  | 30% of data bytes can be restored.        |    

## Others

|  | Params   |  Allowed values  |          Description             |
|--|----------|------|-----------------------------------------------|
|1.| `version`| 1-40 | Specify version to encode the data.           |   
|2.| `mask`   | 0-7  | Specify mask to apply as per QRcode standard. |            





