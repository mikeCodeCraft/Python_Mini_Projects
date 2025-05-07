from PIL import Image
import qrcode

data = input("Enter the data to be stored in QR code: ")

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,)
qr.add_data(data)
qr.make(fit=True)

qr_image = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

watermark = Image.open('me&pas.png')

watermark_size = (qr_image.size[0] // 4, qr_image.size[1] // 4)
watermark = watermark.resize(watermark_size, Image.Resampling.LANCZOS)

pos = ((qr_image.size[0] - watermark.size[0]) // 2, (qr_image.size[1] - watermark.size[1]) // 2)

qr_image.paste(watermark, pos, watermark)

qr_image.save('QRcode.png')

qr_image.show()