import cv2
import numpy as np

def goToVideo():
    while True:
        print('What kind of video processing would you like to do?')
        print('1. Capture live stream video with camera')
        print('2. Play a video from file')
        print('3. Optical flow')
        print('4. Exit')
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
        elif x == '3':
            # Optical flow is the pattern of apparent motion of image objects between two consecutive frames caused 
            # by the movemement of object or camera
            # It is 2D vector field where each vector is a displacement vector 
            # showing the movement of points from first frame to second
            print('Enter the video path')
            vidPath = input()
            cap = cv2.VideoCapture(vidPath)
            # Parameters for Shi-Tomasi corner detection
            feature_params = dict(maxCorners = 100,
                                qualityLevel = 0.01,
                                minDistance = 10,
                                blockSize = 7)
            # Parameters for lucas kanade optical flow
            lk_params = dict(winSize  = (15, 15),
                            maxLevel = 2,
                            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
            # Create some random colors
            color = np.random.randint(0, 255, (100, 3))
            # Take first frame and find corners in it using Shi-Tomasi corner detection
            ret, old_frame = cap.read()
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
            p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
            # Create a mask image for drawing purposes
            mask = np.zeros_like(old_frame)
            print('Press ESC key to stop the video')
            # Repeatedly compare corner points between old frame and new frame for the entire video
            # to get the vectors which make up optical flow
            while(1):
                ret,frame = cap.read()
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Calculate optical flow
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
                # Select good points
                good_new = p1[st == 1]
                good_old = p0[st == 1]
                # Draw the tracks
                for i, (new, old) in enumerate(zip(good_new, good_old)):
                    a,b = new.ravel()
                    c,d = old.ravel()
                    mask = cv2.line(mask, (a,b), (c,d), color[i].tolist(), 2)
                    frame = cv2.circle(frame, (a,b), 5, color[i].tolist(), -1)
                img = cv2.add(frame, mask)
                # Show the frame
                cv2.imshow('frame', img)
                if cv2.waitKey(50) & 0xFF == ord('\x1B'):
                    break
                # Now update the previous frame and previous points, the new frame/points will become old frame/points 
                # and the next loop, the captured frame/points will be the new frame/points
                old_gray = frame_gray.copy()
                p0 = good_new.reshape(-1, 1, 2)
            cv2.destroyAllWindows()
            cap.release()
        else:
            break