import cv2
import pytesseract
import pyperclip
import os, sys
from PIL import Image  

x1, y1, x2, y2 = 0, 0, 0, 0
toFile = True
path = 'bin/test.jpg'
dir = 'media'
slidesDir = 'media/slides'
image = cv2.imread(path,0)

# Prompts user to crop first available screenshot based on overlaid grid
def getVideoCoordinates():
    global path, image
   # for imagePath in os.listdir(slidesDir):
    imagePath = '/prelim.png'
    path = os.path.join(slidesDir, imagePath)
    isFirst = False
    print(path)
    image = cv2.imread(path,0)
    GRID_SIZE_W = 200
    GRID_SIZE_H = 150
    height, width = image.shape
    for x in range(0, width -1, GRID_SIZE_W):
        cv2.line(image, (x, 0), (x, height), (255, 0, 0), 5)
    for x in range(0, height -1, GRID_SIZE_H):
        cv2.line(image, (0, x), (width, x), (255, 0, 0), 5)
    cv2.imshow("IMAGE", image)
    k = cv2.waitKey(0) & 0xFF
    if k == ord('c'):
        x1 = input("x1? ")
        x2 = input("x2? ")
        y1 = input("y1? ")
        y2 = input("y2? ")

        x1 = int((int(x1)/(width/GRID_SIZE_W))*width)
        x2 = int((int(x2)/(width/GRID_SIZE_W))*width)
        y1 = int((int(y1)/(height/GRID_SIZE_H))*height)
        y2 = int((int(y2)/(height/GRID_SIZE_H))*height)

        coordinates = [(x1, y1), (x2, y2)]
        cv2.destroyAllWindows()

        return coordinates

def getCoordinates():
    global path, image
    # for imagePath in os.listdir(liveDir):
    path = 'media/prelim.png'
    isFirst = False
    print(path)
    image = cv2.imread(path,0)
    GRID_SIZE_W = 200
    GRID_SIZE_H = 150
    height, width = image.shape
    for x in range(0, width -1, GRID_SIZE_W):
        cv2.line(image, (x, 0), (x, height), (255, 0, 0), 5)
    for x in range(0, height -1, GRID_SIZE_H):
        cv2.line(image, (0, x), (width, x), (255, 0, 0), 5)
    cv2.imshow("IMAGE", image)

    k = cv2.waitKey(0) & 0xFF
    if k == ord('c'):
        x1 = input("x1? ")
        x2 = input("x2? ")
        y1 = input("y1? ")
        y2 = input("y2? ")

        x1 = int((int(x1)/(width/GRID_SIZE_W))*width)
        x2 = int((int(x2)/(width/GRID_SIZE_W))*width)
        y1 = int((int(y1)/(height/GRID_SIZE_H))*height)
        y2 = int((int(y2)/(height/GRID_SIZE_H))*height)

        # print(x1, y1, x2,y2)
        coordinates = [(x1, y1), (x2, y2)]
        # cv2.destroyAllWindows()
        return coordinates
    else:
        print("ERROR")

# Loops through all images in /slides
def analyzeImages():
    global path, image, imageCopy, isFirst
    for imagePath in os.listdir(slidesDir):
        path = os.path.join(slidesDir, imagePath)
        image = Image.open(path)
        analyzeImage(image) 

#Performs OCR on a single image
def analyzeImage(img):
    pytesseract.pytesseract.tesseract_cmd ='/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'   
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

    result = pytesseract.image_to_string(img)   
    if toFile:
        # with open('result.txt', mode ='w') as file:    
        with open('result.txt', 'a') as file:      
            file.write(result)      
    else:
        pyperclip.copy(result)

    print(result)
    return





# Unfinished / failed logic below -----------------------------------------------------------------------------------

isCropped, wasCropped = False, False
imageCopy = image.copy()
refPoint = [(0, 0), (1, 1)]
roi = imageCopy[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]

def selectPixels():
    global path, image, imageCopy
    imageCopy = image.copy()
    cv2.namedWindow("IMAGE")
    cv2.setMouseCallback("IMAGE", mouseCallback)
    while True:
        i = image.copy()
        if not isCropped:
            cv2.imshow("IMAGE", image)
            print("not iscropped")
        elif isCropped:
            color = (255, 0, 0)
            cv2.rectangle(i, (x1, y1), (x2, y2), color, 3)
            cv2.imshow("IMAGE", i)
            print("iscropped")
        k = cv2.waitKey(0)
    
def mouseCallback(event, x, y, flags, param):
    global x1, y1, x2, y2, isCropped, imageCopy, wasCropped, refPoint, roi
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
        roi = imageCopy[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
        cv2.imshow("CROP", roi)
    k = cv2.waitKey(0) & 0xFF
    if k == ord('s'):
        cv2.destroyWindow("Cropped")
        imgRes = Image.open(path).crop((x1, y1, x2, y2))
        analyzeImage(imgRes)
        breakLoop = True
        cv2.destroyAllWindows()
        return
    elif k == 27:
        cv2.destroyAllWindows()
        sys.exit() 

# imageCopy = image.copy()
# cv2.namedWindow("image")
# cv2.setMouseCallback("image", mouseCallback)
# while True:
#     i = image.copy()
#     if not isCropped:
#         cv2.imshow("image", image)
#         print("not iscropped")
#     elif isCropped:
#         color = (255, 0, 0)
#         cv2.rectangle(i, (x1, y1), (x2, y2), color, 3)
#         cv2.imshow("image", i)
#         print("iscropped")
#     k = cv2.waitKey(0) & 0xFF
#     if k == ord('x'):
#         cv2.destroyWindow("image")

        # cv2.namedWindow("image")
        # cv2.setMouseCallback("image", mouseCallback)
        # while True:
        #     i = image.copy()
        #     if wasCropped:
        #         #cv2.imshow("Cropped", roi)
        #         if k == ord('s'):
        #             cv2.destroyWindow("Cropped")
        #             imgRes = Image.open(path).crop((x1, y1, x2, y2))
        #             analyzeImage(imgRes)
        #             breakLoop = True
        #             cv2.destroyAllWindows()
        #             k = cv2.waitKey(0) & 0xFF
        #         return
        #     elif not isCropped:
        #         cv2.imshow("image", image)
        #         #print("not iscropped")
        #         k = cv2.waitKey(0) & 0xFF
        #     elif isCropped:
        #         color = (255, 0, 0)
        #         cv2.rectangle(i, (x1, y1), (x2, y2), color, 3)
        #         cv2.imshow("image", i)
        #         #print("iscropped")
        #         k = cv2.waitKey(0) & 0xFF
            
        #     if k == ord('s'):
        #         cv2.destroyWindow("Cropped")
        #         imgRes = Image.open(path).crop((x1, y1, x2, y2))
        #         analyzeImage(imgRes)
        #         breakLoop = True
        #         cv2.destroyAllWindows()
        #         return
        #     elif k == 27:
        #         cv2.destroyAllWindows()
        #         sys.exit()