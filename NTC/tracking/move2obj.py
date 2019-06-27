import numpy as np
import cv2
# from move_servo import wire


OK_ZONE = 100

cap = cv2.VideoCapture(0)
# arduino = wire('ttyUSB0')

ret, frame = cap.read()

lbound = (np.shape(frame)[1] // 2) - (OK_ZONE // 2)
rbound = lbound + OK_ZONE
print(lbound, rbound)
window_height = np.shape(frame)[0]

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


def cp(window):
    x, y, w, h = window
    cx = x + (w / 2)
    cy = y + (h / 2)
    return (cx, cy)


def delta(point):
    px, py = point
    if px > lbound:
        print('go left')
        return
    if px < rbound:
        print('go right')
        return
    print('OK')
    return


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
        img2 = cv2.line(img2, (lbound, 0),
                        (lbound, window_height), (0, 0, 255), 5)
        img2 = cv2.line(img2, (rbound, 0),
                        (rbound, window_height), (0, 0, 255), 5)
        delta(cp(track_window))
        cv2.imshow('img2', cv2.flip(img2, 1))

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    else:
        break

cv2.destroyAllWindows()
cap.release()
