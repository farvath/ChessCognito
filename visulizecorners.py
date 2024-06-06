import numpy as np
import cv2

# Load the image
img = cv2.imread("15.jpg")
image=cv2.resize(img,(720,720))      

# Define the coordinates of the box
points = np.array( [   [128 , 94], [623, 113], [665 ,668],   [ 51 ,632]], np.int32)

# Reshape the points array into the shape required by OpenCV (number of vertices, 1, 2)
points = points.reshape((-1, 1, 2))

# Draw the box on the image
cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

# Display the image with the box
cv2.imshow('Image with Box', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
