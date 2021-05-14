import cv2
import pyautogui
import numpy as np
import time
import fire
import scipy.spatial.distance
import os

pyautogui.FAILSAFE = True


def wall_detection(
        approx=True,
        contour_test=True,
        kernel=(15, 15),
        epsilon_value=0.005
):
    ####################
    # Image Section
    #
    global down
    down = False

    def event_handle(event, x, y, flags, params):
        global down, point_1, point_2, sub_img
        if event == cv2.EVENT_LBUTTONDOWN:
            down = True
            point_1 = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and down:
            img_copy = img.copy()
            cv2.rectangle(img_copy, point_1, (x, y), (0, 0, 255), 2)
            cv2.imshow("Image", img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            down = False
            sub_img = img[point_1[1]:y, point_1[0]:x]
            point_2 = (x, y)
            cv2.destroyAllWindows()
            cv2.imshow("Press 0 to close", sub_img)

    img = pyautogui.screenshot("straight_to_disk.png")
    img = cv2.imread("straight_to_disk.png", 1)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', event_handle)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img = sub_img
    box = point_1
    #
    ####################

    ####################
    # Computer Vision
    #
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    im2 = img.copy()
    cv2.drawContours(im2, contours, -1, (0, 255, 0), 3)
    #
    ####################

    ####################
    # Contour testing
    # 
    if contour_test:
        cv2.imshow("Wall Detection", im2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    #
    ####################

    ####################
    # Clicking Script
    #
    time.sleep(3)
    print(box[0], box[1])
    if approx:
        print('approx')
        for array in contours:
            # print(array)
            epsilon = epsilon_value * cv2.arcLength(array, True)
            approx = cv2.approxPolyDP(array, epsilon, True)
            approx = np.vstack(approx)
            # time.sleep(1)
            for c in approx:
                x = c[0] + box[0]
                y = c[1] + box[1]
                pyautogui.click(x, y)
            pyautogui.click(approx[0][0] + box[0], approx[0][1] + box[1])
            pyautogui.click(approx[0][0] + box[0], approx[0][1] + box[1], button='right')
    else:
        print("not approx")
        for array in contours:
            conttest = np.vstack(array)
            for index, c in enumerate(conttest):
                if index == 1:
                    d = scipy.spatial.distance.cdist(array[index - 1], array[index])
                    if d < 2.5:
                        continue
                x = c[0] + box[0]
                y = c[1] + box[1]
                pyautogui.click(x, y)
            pyautogui.click(conttest[0][0] + box[0], conttest[0][1] + box[1])
            pyautogui.click(conttest[0][0] + box[0], conttest[0][1] + box[1], button='right')
    os.remove("straight_to_disk.png")
    #
    ####################


if __name__ == "__main__":
    fire.Fire(wall_detection)
