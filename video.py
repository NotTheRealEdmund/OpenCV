import cv2
import numpy as np

def goToVideo():
    while True:
        print('What kind of video processing would you like to do?')
        print('1. Capture live stream video with camera')
        print('2. Play a video from file')
        print('3. Optical flow')
        print('4. Dense optical flow')
        print('5. Background subtraction')
        print('6. Exit')
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
                if cv2.waitKey(30) & 0xFF == ord('\x1B'):
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
                if cv2.waitKey(30) & 0xFF == ord('\x1B'):
                    break
                # Now update the previous frame and previous points, the new frame/points will become old frame/points 
                # and the next loop, the captured frame/points will be the new frame/points
                old_gray = frame_gray.copy()
                p0 = good_new.reshape(-1, 1, 2)
            cv2.destroyAllWindows()
            cap.release()
        elif x == '4':
            # Dense optical flow basically computes the optical flow for all the points in the frame instead of just corner points.
            print('Enter the video path')
            vidPath = input()
            cap = cv2.VideoCapture(vidPath)

            # First frame
            ret, frame = cap.read()
            old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hsv = np.zeros_like(frame)
            hsv[...,1] = 255

            print('Press ESC key to stop the video')
            # Repeatedly compare between old frame and new frame for the entire video
            while(1):
                ret, frame = cap.read()
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                flow = cv2.calcOpticalFlowFarneback(old_gray, frame_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

                mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                hsv[...,0] = ang*180/np.pi/2
                hsv[...,2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
                img = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

                # Show the frame
                cv2.imshow('frame', img)
                if cv2.waitKey(30) & 0xFF == ord('\x1B'):
                    break
                # Now update the previous frame and previous points, the new frame/points will become old frame/points 
                # and the next loop, the captured frame/points will be the new frame/points
                old_gray = frame_gray
            cap.release()
            cv2.destroyAllWindows()
        elif x == '5':
            # Background subtraction is a major preprocessing step in many vision based applications
            # Technically, we are extracting the moving foreground from static background
            print('Enter the video path')
            vidPath = input()
            cap = cv2.VideoCapture(vidPath)
            print('Press ESC key to stop the video')
            
            # Before the loop, we need to use cv2.createBackgroundSubtractorMOG2()
            # to create a background object using the function
            background = cv2.createBackgroundSubtractorMOG2()

            while(1):
                ret, frame = cap.read()

                # This kernel allows morphological opening to use the first few (120 by default) frames for background modelling.
                # It employs probabilistic foreground segmentation algorithm that identifies 
                # possible foreground objects using Bayesian inference. 
                # The estimates are adaptive; newer observations are more heavily weighted 
                # than old observations to accommodate variable illumination. 
                # Several morphological filtering operations like closing and opening are done to remove unwanted noise. 
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

                # Use backgroundsubtractor.apply() method to get the foreground mask.
                mask = background.apply(frame)

                # Apply morphological opening to the resulting mask to remove the noises
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

                # Show the frame
                cv2.imshow('frame', mask)
                if cv2.waitKey(30) & 0xFF == ord('\x1B'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        else:
            break