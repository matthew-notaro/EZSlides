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
    while True:
        i = image.copy()
        if not isCropped:
            cv2.imshow("image", image)
        elif isCropped:
            color = (255, 0, 0)
            cv2.rectangle(i, (x1, y1), (x2, y2), color, 3)
            cv2.imshow("image", i)
    print("here2")
    img_res = image.crop((x1, y1, x2, y2)) 
    img_res.show() 
    
def mouseCallback(event, x, y, flags, param):
    global x1, y1, x2, y2, isCropped, imageCopy, image
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
    k = cv2.waitKey(0) & 0xFF
    if k == 27: # wait for ESC key to exit
        cv2.destroyAllWindows()
    # print("here")
    # img_res = Image.open(path).crop((x1, y1, x2, y2))
    # img_res.show() 

def analyzeImage(img):
    #img = Image.open(path)    
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

# cropping = False
# x_start, y_start, x_end, y_end = 0, 0, 0, 0
# image = cv2.imread('bin/test.jpg')
# oriImage = image.copy()
# def mouse_crop(event, x, y, flags, param):
#     # grab references to the global variables
#     global x_start, y_start, x_end, y_end, cropping
#     # if the left mouse button was DOWN, start RECORDING
#     # (x, y) coordinates and indicate that cropping is being
#     if event == cv2.EVENT_LBUTTONDOWN:
#         x_start, y_start, x_end, y_end = x, y, x, y
#         cropping = True
#     # Mouse is Moving
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if cropping == True:
#             x_end, y_end = x, y
#     # if the left mouse button was released
#     elif event == cv2.EVENT_LBUTTONUP:
#         # record the ending (x, y) coordinates
#         x_end, y_end = x, y
#         cropping = False # cropping is finished
#         refPoint = [(x_start, y_start), (x_end, y_end)]
#         if len(refPoint) == 2: #when two points were found
#             roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
#             cv2.imshow("Cropped", roi)
# cv2.namedWindow("image")
# cv2.setMouseCallback("image", mouse_crop)
# while True:
   
#     i = image.copy()
#     if not cropping:
#         cv2.imshow("image", image)
#         cv2.waitKey(0)
#     elif cropping:
#         cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
#         cv2.imshow("image", i)
#         cv2.waitKey(0)
# # close all open windows
# cv2.destroyAllWindows()