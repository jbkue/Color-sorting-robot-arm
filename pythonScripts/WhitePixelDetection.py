import cv2
import numpy as np

vid = cv2.VideoCapture(0)
while True:
    ret, frame = vid.read()
    roi = frame[0:200, 100:300]
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    color_feed = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
    kernal = np.ones((5, 5), "uint8")
    white_mask = cv2.inRange(gray_scale, 250, 255)
    white_mask = cv2.dilate(white_mask, kernal)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    red_mask = cv2.inRange(roi, lower_red, upper_red)
    white_contours, white_hierarchy = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(gray_scale)
    gray_scale = cv2.line(gray_scale, (x // 2, y), (x // 2, 0), (0, 0, 0), 2)
    gray_scale = cv2.line(gray_scale, (x, y // 2), (0, y // 2), (0, 0, 0), 2)
    gray_scale = cv2.circle(gray_scale, (x // 2, y // 2), 4, (0, 0, 0), 4)

    for pic, contour in enumerate(white_contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            gray_scale = cv2.rectangle(gray_scale, (x, y),
                                       (x + w, y + h),
                                       (90, 55, 200), 2)
            gray_scale = cv2.circle(gray_scale, (x + w // 2, y + h // 2), 2, (0, 0, 0), 2)
            print((x + w // 2, y + h // 2))
    cv2.imshow("AAAA", gray_scale)
    cv2.imshow("roi", roi)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()
