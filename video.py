import cv2

def goToVideo():
    while True:
        print('What kind of video processing would you like to do?')
        print('1. Capture live stream video with camera')
        print('2. Play a video from file')
        print('3. Exit')
        x = input()
        if x == '1':
            cap = cv2.VideoCapture(0)
            print('Press ESC key to stop recording')
            while(True):
                # Capture frame-by-frame
                ret, frame = cap.read()
                # Carry out operations on the frame, make the frames turn gray
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Display the resulting frame
                cv2.imshow('frame', gray)
                if cv2.waitKey(1) & 0xFF == ord('\x1B'):
                    break
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
        elif x == '2':
            print('Enter the video path')
            vidPath = input()
            cap = cv2.VideoCapture(vidPath)
            print('Press ESC key to stop the video')
            while(cap.isOpened()):
                ret, frame = cap.read()
                cv2.imshow('frame', frame)
                # Slow the video down by limiting the display frame rate
                if cv2.waitKey(50) & 0xFF == ord('\x1B'):
                    break
            cap.release()
            cv2.destroyAllWindows()    
        else:
            break