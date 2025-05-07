import barcode
from barcode.writer import ImageWriter 
from IPython.display import Image, display
import time
#pip install python-barcode
#pip install ipython
#pip install pillow


barcode_format = barcode.get_barcode_class('ean13')

barcode_number = '2348166081565'

barcode_image = barcode_format(barcode_number,writer=ImageWriter())

bar_name = int(round(time.time()*1000))
bar_name = "barcode_data\\{}".format(bar_name)


barcode_image.save(bar_name)


display(Image(filename=bar_name))