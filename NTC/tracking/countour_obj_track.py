import numpy as np
import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

# Setup initial location of window
r, c, h, w = 250, 90, 400, 125
track_window = (c, r, w, h)

# Set up ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0.0, 60.0, 32.0)),
                   np.array((180.0, 255.0, 255.0)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iterations or move by at least 1pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
    ret, frame = cap.read()

    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # Apply meanshiftto get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x, y, w, h = track_window
        img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        cv2.imshow('img2', cv2.flip(img2, 1))

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    else:
        break

cv2.destroyAllWindows()
cap.release()