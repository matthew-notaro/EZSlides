import os
import sys
import cv2
import time
import imagehash
import numpy as np
import pyautogui

from PIL import Image
from moviepy.editor import *


# End Imports -----------------------------------------------------------------------------------


class Slides:
    def __init__(self, videoPath):

        # Sets videoPath if analyzing video file - expecting None if live feed
        self.videoPath = videoPath

        # Contains the number of unique slides
        self.slideCount = 0
        

    # Takes raw video file and outputs unique slides in order taken to ./media
    def videoFeed(self):
        
        # Make sure videoPath != None
        if self.videoPath is None:
            print("something's wrong I can feel it")
            return

        # Video stream
        vidObj = cv2.VideoCapture(self.videoPath)

        # Gets FPS of video for skipping
        fps = vidObj.get(cv2.CAP_PROP_FPS)
        
        # Delay between screenshots (in seconds)
        delay = 1

        # Counters
        slideNum = 1                # tracks unique slide number
        frameNum = fps * delay      # tracks frames read up to the fps, set to fps * delay to immediately take screenshot 

        # Frame extractor loop
        while True:
            # Reads in the next frame
            success, frame = vidObj.read()

            if success:
                # frameNum has met minimum threshold
                if frameNum >= (fps * delay):
                    # Reset frame number
                    frameNum = 0

                    # Save current frame and hash it
                    cv2.imwrite("../media/slides/slide%d.jpg" % slideNum, frame)
                    hashCurr = imagehash.average_hash(Image.open("../media/slides/slide%d.jpg" % (slideNum)))

                    # Compare current frame to previous slides to check for repeats
                    temp = slideNum - 1
                    while temp >= 1:
                        hashIter = imagehash.average_hash(Image.open("../media/slides/slide%d.jpg" % (temp)))

                        # If different slide, move onto previous slide
                        if (hashCurr - hashIter) >= 5:
                            temp -= 1

                        # If repeated slide, delete current slide and read in next one
                        else:
                            os.remove("../media/slides/slide%d.jpg" % (slideNum))
                            break
                    
                    # If current slide if unique, inc slideNum
                    if temp is 1:
                        slideNum += 1


                frameNum += 1
            
            # Reached end of file
            else:
                break
        
        print("ending video processing...")

        vidObj.release()
        cv2.destroyAllWindows()




    # Takes a screenshot of the presentation window every second
    # Upon taking a new screenshot, compares it to the previous image
    # If similar enough, discards current image
    # If different enough, saves and indexes new image 
    def liveFeed(self):

        # Make sure videoPath == None
        if self.videoPath != None:
            print("something's wrong I can feel it")
            return
        
        # Delay between screenshots (in seconds)
        delay = 1

        # Counter - tracks unique slide number
        slideNum = 1

        # Frame extractor loop
        while True:
            # Takes next screenshot and converts to writable format
            sc = pyautogui.screenshot()
            sc = cv2.cvtColor(np.array(sc), cv2.COLOR_RGB2BGR)

            # Save current sc to disk and hash it
            cv2.imwrite("../media/slides/slide%d.jpg" % slideNum, sc)
            hashCurr = imagehash.average_hash(Image.open("../media/slides/slide%d.jpg" % (slideNum)))

            # Compare current sc to previous slides to check for repeats
            temp = slideNum - 1
            while temp >= 1:
                hashIter = imagehash.average_hash(Image.open("../media/slides/slide%d.jpg" % (temp)))

                # If different slide, move onto previous slide
                if (hashCurr - hashIter) >= 5:
                    temp -= 1

                # If repeated slide, delete current slide and read in next one
                else:
                    os.remove("../media/slides/slide%d.jpg" % (slideNum))
                    break
            
            # If current slide if unique, increment slideNum
            # Catches 1st screenshot case and ensures it always gets written
            if temp <= 1:
                slideNum += 1
        
        print("ending video processing...")

        cv2.destroyAllWindows()

def main():
    vid = Slides("../media/test lecture.mp4")
    vid.videoFeed()