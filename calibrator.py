import numpy as np
import cv2 as cv
import time

# Number of inside corners on your checkerboard
# ex: A 8x6 checkerboard should have values of (7, 5)
chessboardSize = (7, 5)

# Should be same as in recorder.py
frameSize = (1280, 720)

# Size of checkerboard squares in meters
sizeOfBoardSquaresm = 0.03

# Name of recording file
cap = cv.VideoCapture("cam3.avi")

framesProcessed = 190 # Good rule of thumb: ~20 for a quick calibration, ~200 for compeition-ready calibration. Consider adding more if alot of frames have no checkerboard

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)


objp = objp * sizeOfBoardSquaresm

objpoints = []
imgpoints = []

totalFrames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print(f"Total frames: {totalFrames}")
frameSkips = totalFrames // framesProcessed

count = 0

startTime = time.time()

print("Note: this program will take a while, especially on the calibration step. Let it run.")

print("Reading frames...")

while cap.isOpened():
    _, img = cap.read()

    if not count == frameSkips:
        count += 1
        print(count)
        continue

    if _:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            count = 0
        else:
            print(f"WARN: No chessboard detected in frame.")
    else:
        break

print(f"Frame reading complete. It took {round((time.time() - startTime) / 60, 2)} minutes.")
print(f"{len(objpoints)} frames were read.")

print("Starting Calibration, this will take a WHILE depending on number of frames")

startTime = time.time()

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

print(f"Calibration complete. It took {round((time.time() - startTime) / 60, 2)} minutes.")

print("\n Reprojection error:")
print(ret)
print("This should be between 0.1 and 1. If it is outside of that, gather new data")

print (
    f"""
    Camera Matrix:
    {cameraMatrix}

    In the order of:
    fx 0 cx
    0 fy cy
    0 0 1
        
    
    
    Distortion Coefficients:
    {dist}

    In the order of:
    k1 k2 p1 p2 k3
    """
)

input("Hit enter to close the window. Outputs have been written to outputs.txt. Make sure you record them before running again, new values WILL overwrite old ones.")

f = open("output.txt", "w")
f.write(
    f"""
    Camera Matrix:
    {cameraMatrix}

    In the order of:
    fx 0 cx
    0 fy cy
    0 0 1
        
    
    
    Distortion Coefficients:
    {dist}

    In the order of:
    k1 k2 p1 p2 k3
    """
)

f.close()