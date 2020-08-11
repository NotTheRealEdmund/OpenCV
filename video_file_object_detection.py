# Command: py video_file_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel --video vidtest2.mp4

# Import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
ap.add_argument("-v", "--video", required=True,
	help="path to input video file")
args = vars(ap.parse_args())

# Initialize the list of class labels MobileNet SSD was trained to detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Load the serialized model from disk
print("[ INFO:0] Loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# Start the file video stream thread and allow the buffer to start to fill
print("[ INFO:0] Starting video...")
print("[ INFO:0] Press ESC key to quit...")
vs = FileVideoStream(args["video"]).start()
time.sleep(2.0)

# Start the FPS timer
fps = FPS().start()

# Loop over the frames from the video stream
while vs.more():
	# Grab the frame from the threaded video stream and resize it to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# Grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# Pass the blob through the network and obtain the detections and predictions
	net.setInput(blob)
	detections = net.forward()

	# Loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# Extract the confidence (i.e., probability) associated with the prediction
		confidence = detections[0, 0, i, 2]

		# Filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
		if confidence > args["confidence"]:
			# Extract the index of the class label from the `detections`, then compute the (x, y)-coordinates of the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# Draw the prediction on the frame
			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	# Show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# If the ESC key was pressed, break from the loop
	if key == 27:
		break

	# Update the FPS counter
	fps.update()

# Stop the timer and display FPS information
fps.stop()
print("[ INFO:0] Elapsed time: {:.2f}s".format(fps.elapsed()))
print("[ INFO:0] FPS: {:.2f}".format(fps.fps()))

# Cleanup
cv2.destroyAllWindows()
vs.stop()