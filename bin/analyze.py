import cv2
import pytesseract
import pyperclip
from PIL import Image   

spam = pyperclip.paste() 

toFile = False

img = Image.open('bin/test2.jpg')    
pytesseract.pytesseract.tesseract_cmd ='/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'   
#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
result = pytesseract.image_to_string(img)   

if toFile:
    with open('result.txt', mode ='w') as file:    
    #with open('result.txt', 'a') as file:      
        file.write(result)
        print(result)
else:
    pyperclip.copy(result)