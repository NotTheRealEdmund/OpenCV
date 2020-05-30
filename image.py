import cv2
import numpy as np
from matplotlib import pyplot as plt

def goToImage():
    print('Enter image path')
    imgPath = input()
    while True:
        print('What kind of image processing would you like to do?')
        print('Current image path: ' + imgPath)
        print('1. View the image in color')
        print('2. View the image in grayscale')
        print('3. Change the image path')
        print('4. Canny Edge Detection')
        print('5. Shi-Tomasi Corner Detector')
        print('6. Exit')
        x = input()
        if x == '1':
            img = cv2.imread(imgPath, 1)
            cv2.imshow('image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print('Would you like to save this image to a path? (y/n)')
            y = input()
            if y == 'y':
                print('Enter path to save image to')
                z = input()
                cv2.imwrite(z, img)
        elif x == '2':
            img = cv2.imread(imgPath, 0)
            cv2.imshow('image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print('Would you like to save this image to a path? (y/n)')
            y = input()
            if y == 'y':
                print('Enter path to save image to')
                z = input()
                cv2.imwrite(z, img)
        elif x == '3':
            print('Enter new image path')
            imgPath = input()
        elif x == '4':
            img = cv2.imread(imgPath, 0)
            # The most important function to carry out Canny Edge Detection
            # The arguments 100 and 200 are thresholds, minVal and maxVal
            # Any edges with intensity gradient more than maxVal are sure to be edges 
            # and those below minVal are sure to be non-edges, so discarded
            # Those who lie between these two thresholds are classified edges or non-edges based on their connectivity
            # If they are connected to “sure-edge” pixels, they are considered to be part of edges
            # Otherwise, they are also discarded
            edges = cv2.Canny(img, 100, 200)
            # Prepare the edge image to show contrast between edges and background
            plt.subplot(121), plt.imshow(img, cmap='gray')
            plt.title('Original Image'), plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(edges, cmap='gray')
            plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
            # Show the plot
            plt.show()
        elif x == '5':
            # Shi-Tomasi Corner Detector is a slightly better version of Harris Corner Detector 
            # because the scoring function used is slightly more accurate.
            # The Shi-Tomasi Corner Detector gives points which are less cluttered and 
            # are more obvious when looking at the big picture
            img = cv2.imread(imgPath)
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Shi-Tomasi corner detection function, goodFeaturesToTrack
            # We are detecting 100 best corners here, you can change the number to get desired result, leave the rest the same
            # 0.01 is the minimum quality level below which the corners are rejected
            # 10 is the minimum euclidean distance between two corners
            corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
            # Convert corners values into integers so that we will be able to draw circles on them 
            corners = np.int0(corners)
            # Draw dots on all corners 
            for i in corners:
                x,y = i.ravel()
                # (255, 0, 0) makes dots blue after conversion to grayscale
                # (0, 255, 0) makes dots green after conversion to grayscale
                # (0, 0, 255) makes dots red after conversion to grayscale
                # If the final argument is 0, it shows circles
                # If the final argument -1, it shows dots
                cv2.circle(img, (x,y), 3, (255, 0, 0), -1)
            # Show result 
            cv2.imshow('image', img)  
            # Press any key to close image
            if cv2.waitKey(0):  
                cv2.destroyAllWindows()
            # Provide option to save image
            print('Would you like to save this image to a path? (y/n)')
            y = input()
            if y == 'y':
                print('Enter path to save image to')
                z = input()
                cv2.imwrite(z, img)
        else:
            break
