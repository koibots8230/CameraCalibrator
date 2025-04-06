import numpy as np
import cv2 as cv

# Change to zero if no other camera is on your computer (this includes laptop cameras)
# If there is another camera on your computer, keep at 1
vid = cv.VideoCapture(0, cv.CAP_DSHOW)

# Configure this to your camera frame size
# If this and the size entered in cameras.json differ, pose estimation WILL be innaccurate
frame_width = 1280
frame_height = 720

# Name of recording file
recordingName = "filename.avi"

vid.set(cv.CAP_PROP_FRAME_WIDTH, frame_width)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, frame_height)
   
size = (frame_width, frame_height) 

result = cv.VideoWriter(recordingName,  
                         cv.VideoWriter_fourcc(*'MJPG'), 
                         50, size) 

print("Press S to stop recording")

while(True): 
    ret, frame = vid.read() 
  
    if ret == True:  
        result.write(frame) 

        resize = cv.resize(frame, (1200, 900))
        cv.imshow('Frame', resize) 
  
        # Press S on keyboard  
        # to stop the process 
        if cv.waitKey(1) & 0xFF == ord('s'): 
            break
  
    else: 
        break

vid.release() 
result.release() 

cv.destroyAllWindows() 
   
print("The video was successfully saved") 