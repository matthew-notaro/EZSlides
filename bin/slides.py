import os
import sys
import cv2
import time
import imagehash
import numpy as np

# import pyautogui

import analyze
from PIL import Image
from moviepy.editor import *


# End Imports -----------------------------------------------------------------------------------


class Slides:
    def __init__(self, videoPath, cropDims):

        # Sets videoPath if analyzing video file - expecting None if live feed
        self.videoPath = videoPath

        # Contains the number of unique slides
        self.slideCount = 0

        # Sets crop boundaries
        self.x1 = cropDims[0][0]
        self.y1 = cropDims[0][1]
        self.x2 = cropDims[1][0]
        self.y2 = cropDims[1][1]
        

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
        delay = 2

        # Counters
        slideNum = 0                # tracks unique slide number
        frameNum = fps * delay      # tracks frames read up to the fps, set to fps * delay to immediately take screenshot
        totalFrames = 0             # track total number of frames read for debugging

        success, frame = vidObj.read()
        totalFrames += 1

        # Reads in and appends all slides as images to frame_list
        frame_list = []
        while (success):
            if (totalFrames % (frameNum) <= 1):
                frame_list.append(frame)
                # cv2.imwrite("../media/slides/all/slide%d.png" % slideNum, frame)
                # slideNum += 1
            success, frame = vidObj.read()
            totalFrames += 1

        # Crop all frames to desired dimensions
        for i in range(len(frame_list)):
            frame_list[i] = frame_list[i].crop((self.x1, self.y1, self.x2, self.y2))

        # Writes all frames to calculate each frame's image hash and appends to hash
        hash = []
        for i in range(len(frame_list)):
            cv2.imwrite("../media/slides/temp.png", frame_list[i])
            curr_hash = imagehash.average_hash(Image.open("../media/slides/temp.png"))
            hash.append(curr_hash)

        # Store frames with enough change from previous frame in selected_frames
        # Start with frame_list[0] - append the next, not the current
        selected_frames = [frame_list[0]]
        selected_hashes = [hash[0]]

        for i in range(len(hash) - 1):
            curr_hash = hash[i]
            next_hash = hash[i + 1]

            # If different from previous, appends to selected_frame
            if (abs(curr_hash - next_hash) != 0):
                print("i = %d, diff = %d" % (i, abs(curr_hash - next_hash)))
                selected_frames.append(frame_list[i+1])
                selected_hashes.append(hash[i+1])

        # for i, frame in enumerate(selected_frames):
        #     cv2.imwrite("../media/slides/{}.png".format(i), frame)
        

        # Ensured selected frames are not repeated
        selected_frames2 = []
        for i in range(len(selected_frames)):
            uniqueSlide = True
            curr_hash = selected_hashes[i]
            
            for j in range(i-1, -1, -1):
                prev_hash = selected_hashes[j]
                print(abs(curr_hash - next_hash), i, j)
                if abs(curr_hash - next_hash) == 0:
                    uniqueSlide = False
                    print("repeat found: ", i, j)
                    break

            if uniqueSlide:
                print("unique found: ", i)
                selected_frames2.append(selected_frames[i])

        for i, frame in enumerate(selected_frames2):
            cv2.imwrite("../media/slides/select2{}.png".format(i), frame)

        # Set slideCount to easy iteration through the slides
        self.slideCount = len(selected_frames2)

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

        # Lists to keep track of seen frames and respective hashes
        frame_list = []
        hash = []

        # 






        # # Frame extractor loop
        # while True:
        #     # Takes next screenshot and converts to writable format
        #     #sc = pyautogui.screenshot()
        #     #sc = cv2.cvtColor(np.array(sc), cv2.COLOR_RGB2BGR)

        #     # Save current sc to disk and hash it
        #     cv2.imwrite("../media/slides/slide%d.jpg" % slideNum, sc)
        #     hashCurr = imagehash.average_hash(Image.open("../media/slides/slide%d.jpg" % (slideNum)))

        #     # Compare current sc to previous slides to check for repeats
        #     temp = slideNum - 1
        #     while temp >= 1:
        #         hashIter = imagehash.average_hash(Image.open("../media/slides/slide%d.jpg" % (temp)))

        #         # If different slide, move onto previous slide
        #         if (hashCurr - hashIter) >= 5:
        #             temp -= 1

        #         # If repeated slide, delete current slide and read in next one
        #         else:
        #             os.remove("../media/slides/slide%d.jpg" % (slideNum))
        #             break
            
        #     # If current slide if unique, increment slideNum
        #     # Catches 1st screenshot case and ensures it always gets written
        #     if temp <= 1:
        #         slideNum += 1
        
        # print("ending video processing...")

        cv2.destroyAllWindows()

# vid = Slides("../media/test lecture.mp4")
# vid.videoFeed()
# analyze.analyzeImages()
