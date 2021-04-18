import analyze
import slides
import os
import numpy as np
import cv2
import pyautogui

def main():
    print("Welcome to NAME! Are you capturing from a live lecture or a pre-recorded video?")
    print("1: Live lecture")
    print("2: Pre-recorded video")
    lectureType = input("Enter 1 or 2: ")

    path = None
    while True:
        if(lectureType == '1'):
            print("NAME will capture from your screen.")
            break
        elif(lectureType == '2'):
            print("NAME will capture from the video file.")
            while True:
                path = input("Please enter a valid video path.")
                if os.path.isfile(path):
                    break
            break
        else:
            print("Invalid input. Try again.")
            lectureType = input("Enter 1 or 2: ")

    print("Where would you like to store your text?")
    print("1: Text file")
    print("2: Clipboard")
    outputChoice = input("Enter 1 or 2: ")
    
    while True:
        if(outputChoice == '1'):
            print("Presentation text will be writted to a result.txt.")
            break
        elif(outputChoice == '2'):
            print("Presentation text will be copied to your clipboard.")
            break
        else:
            print("Invalid input. Try again.")
            outputChoice = input("Enter 1 or 2: ")

    if lectureType == '1':
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
        cv2.imwrite("media/prelim.png", image)
        cropCoords = analyze.getCoordinates()  
        live = slides.Slides(None, cropCoords)
        live.liveFeed()

    else:
        vidObj = cv2.VideoCapture("media/test lecture.mp4")
        frame = None
        for i in range(10):
            success, frame = vidObj.read()
        # DISPLAY <frame>
        cv2.imwrite("media/prelim.png", frame)
        cropCoords = analyze.getCoordinates() 
        # vidObj.release()
        vid = slides.Slides(path, cropCoords)
        vid.videoFeed()
        analyze.analyzeImages()

    #result = slides.liveFeed() if lectureType == '1' else slides.videoFeed()
            
if __name__ == "__main__":
    main()