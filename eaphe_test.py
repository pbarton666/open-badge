#this code, from https://code.google.com/p/elaphe proves that the elaphe 
#   routine works - it produces a .png barcode image file

from elaphe import barcode
myBarcode = barcode('qrcode', 'Hello Barcode Writer In Pure PostScript.', 
                    options=dict(version=9, eclevel='M'),  
                    margin=10, data_mode = '8bits')

#myBarcode.show()  #you can have a look at it, if you want
myBarcode.save('test_barcode.png')
x=1