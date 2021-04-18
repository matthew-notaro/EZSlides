# EZSlides

## Inspiration
Have you ever taken a class where your professor speeds through slideshows without stopping? Do your professors ever present you with walls of text, without any time to copy them down? Taking word-for-word notes can be difficult in an online environment, especially through the lenses of accessibility. If only there were a way to automatically copy what's already there, without the hassle of filtering which information is relevant or rushing to finish typing.

## What it does
EZSlides is a program that processes either pre-recorded or live lectures and extracts the text from the video or screen for you to include in your notes! Simply crop the video to just include the text or select a region of your screen to record. You can even save the output to a text file or copy each slide directly to your clipboard to seamlessly paste into your favorite editor. As a result, online learning is made more accessible, efficient, and convenient to all.

## How we built it
To build EZSlides, we used Python 3 alongside the OpenCV, Pillow, ImageHash, PyAutoGUI, Python-tesseract, and Pyperclip libraries.
To breakdown pre-recorded video lectures, we first prompt the user to select a specific region within the video to analyze. We then extracted a frame every other Nth second (2 for the demo) to reduce computation time, cropped the frame to the desired size, hashed the frame using ImageHash, and compared the frame's hash to every other preceding frame's hash to ensure the same frame would not be outputted twice. We then wrote the remaining slides to the disk in order to perform an optical character recognition algorithm on each to convert the raw image to ASCII text which the user could then either output to a file or copy to clipboard.
To follow along live lectures, we prompt the user to select a region of her screen to analyze. We then take screenshots every other Nth second (5 for the demo) and perform similar steps as described above. However, since EZSlides regretfully cannot process future slides, the clipboard output is limited to only the current slide. If the text file output is selected, each new slide will be appended to the file in real time.

## Challenges we ran into
One of the biggest challenges on the video/live processing end was how difficult OpenCV and ImageHash were being in detecting duplicate images. A small string of bugs took at least 4 hours to sort out.
On the crop detection/OCR end, many difficulties arose with the intuitive cropping interface. We eventually decided to put the implementation on hold, instead opting for a simpler but less intuitive manual input grid display.

## Accomplishments that we're proud of
We are proud of waking up this morning and motivating each other to not only participate but also to submit a working hack! There were many speedbumps along the way with neither of us extremely comfortable even using Python but we stuck to our idea and pulled it through. Streamlined a bit more we could see ourselves using EZSlides on a fairly regular basis if a class really calls for it. 

## What we learned
We learned that OpenCV is a pain but PyTesseract is pretty nifty. 

## What's next for EZSlides
As mentioned earlier, more intuitive controls especially when cropping should be on their way maybe sometime in the future. Not only would the interface be made more appealing and be easier to follow, but it would also have positive implications on the accessibility of the program. We also talked about implementing a multithreaded approach to checking if a slide already exists which could greatly decrease processing time for long lectures but neither of us have worked with multithreading in Python before and we both agreed today was not the day to learn it. Finally, and probably most importantly, EZSlides cannot process images and diagrams every well, and by very well we mean not at all. We would have to brainstorm a bit more to determine an algorithm to detect these images or design a seamless way for the user to manually include these.