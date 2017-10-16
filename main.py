from collections import deque
import numpy as np
import cv2
import pyautogui as pt
pt.FAILSAFE = False
handCascade = cv2.CascadeClassifier("hand.xml")

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
DEQUE_MAX_LEN =32
pts = deque(maxlen=DEQUE_MAX_LEN)
counter = 0
(dX, dY) = (0, 0)
direction = ""
camera = cv2.VideoCapture(0)
SPEED = 20

# keep looping
while True:
    ret, frame = camera.read()
    flag  = False
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hands = handCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # Draw a rectangle around the hands

    for (x, y, w, h) in hands:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center = (x+w//2, y+h//2)

        flag = True

        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        pts.appendleft(center)

    # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer

        if counter >= 10 and i == 1 and pts[-1] is not None:
            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[-1][0] - pts[i][0]
            dY = pts[-1][1] - pts[i][1]
            (dirX, dirY) = ("", "")
            # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 40:
                dirX = "Left" if np.sign(dX) == 1 else "Right"
                if flag:
                    if dX > 0:
                        s = -SPEED
                    else:
                        s = SPEED
                    pt.moveRel(s ,0)
            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 20:
                dirY = "Up" if np.sign(dY) == 1 else "Down"
                if flag:
                    if dY>0:s=-SPEED
                    else:s=SPEED
                    pt.moveRel(0, s)
            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)

            # otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(DEQUE_MAX_LEN / float(i + 1)) * 1.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        break
        # show the movement deltas and the direction of movement on
        # the frame
    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

    # show the frame to our screen and increment the frame counter
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break  # cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
