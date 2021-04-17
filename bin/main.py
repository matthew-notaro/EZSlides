import analyze
import slides

def main():
    print("Welcome to NAME! Are you capturing from a live lecture or a pre-recorded video?")
    print("1: Live lecture")
    print("2: Pre-recorded video")
    lectureType = input("Enter 1 or 2: ")
    while True:
        if(lectureType == '1'):
            print("NAME will capture from your screen.")
            break
        elif(lectureType == '2'):
            print("NAME will capture from the video file.")
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

    #result = slides.liveFeed() if lectureType == '1' else slides.videoFeed()
            
if __name__ == "__main__":
    main()