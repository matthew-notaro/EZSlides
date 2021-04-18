import cv2
import pytesseract
import pyperclip
from PIL import Image   

toFile, isCropped = False, False
x1, y1, x2, y2 = 0, 0, 0, 0
path = 'bin/test.jpg'
image = cv2.imread(path,0)
imageCopy = image.copy()

def selectPixels():
    global image
    image = cv2.imread(path,0)
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouseCallback)
    i = image.copy()
    while True:
        i = image.copy()
        if not isCropped:
            cv2.imshow("image", image)
        elif isCropped:
            color = (255, 0, 0, 255)
            cv2.rectangle(i, (x1, y1), (x2, y2), color, 3)
            cv2.imshow("image", i)
        cv2.waitKey(1)
    cv2.destroyAllWindows()  

    img_res = image.crop((x1, y1, x2, y2)) 
    img_res.show() 

def mouseCallback(event, x, y, flags, param):
    global x1, y1, x2, y2, isCropped, imageCopy
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1, x2, y2 = x, y, x, y
        isCropped = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if isCropped == True:
            x2, y2 = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        isCropped = False
        refPoint = [(x1, y1), (x2, y2)]
        croppedImage = imageCopy[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
        cv2.imshow("Cropped", croppedImage)

def analyzeImage(path):
    img = Image.open(path)    
    pytesseract.pytesseract.tesseract_cmd ='/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'   
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

    result = pytesseract.image_to_string(img)   
    if toFile:
        with open('result.txt', mode ='w') as file:    
        #with open('result.txt', 'a') as file:      
            file.write(result)
            
    else:
        pyperclip.copy(result)

    print(result)

selectPixels()