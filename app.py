import image
import video

def menu():
    while True:
        print('What would you like to do?')
        print('1. Image Processing')
        print('2. Video Processing')
        print('3. Exit')
        x = input()
        if x == '1':
            image.goToImage()
        elif x == '2':
            video.goToVideo()
        else:
            print('Goodbye! Hope to see you again soon!')
            break

if __name__ == '__main__':
    print('Welcome to OpenCV!')
    menu()