import cv2
import pytesseract
from PIL import Image    

img = Image.open('bin/test.jpg')     
pytesseract.pytesseract.tesseract_cmd ='/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'   
#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
result = pytesseract.image_to_string(img)   
with open('result.txt',mode ='w') as file:     
    file.write(result)
    print(result)