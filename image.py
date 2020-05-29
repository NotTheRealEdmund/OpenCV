import cv2

def goToImage():
    print('Enter image path')
    imgPath = input()
    while True:
        print('What kind of image processing would like to do?')
        print('Current image path: ' + imgPath)
        print('1. View the image in color')
        print('2. View the image in grayscale')
        print('3. Change the image path')
        print('4. Exit')
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
        else:
            break
