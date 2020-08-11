import cv2 
import pyautogui
import numpy as np
import time
import fire

def wall_detection(IMAGE):
    
    img = cv2.imread(IMAGE) 
    orig_img = img.copy()
    
    ####################
    #IMAGE RECOG
    #
    box = pyautogui.locateOnScreen(orig_img, confidence=0.9)
    if box is None:
        raise RuntimeError("Could not detect iamge on screen")
    #
    ####################
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1)) 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    im2 = img.copy()
    cv2.drawContours(im2, contours, -1, (0,255,0), 3)
    
    #############
    #Contour testing
    #
    # cv2.imshow("Wall Detection", im2)
    # cv2.waitKey(0)
    #
    #############
    
    #############
    #Clicking Script
    #working(for the most part)
    #bug, if coords are to close to eachother roll2 may click twice in same spot
    conttest = np.vstack(contours)
    time.sleep(5)
    for c in conttest[:,0,:]:
        x = c[0] + box[0]
        y = c[1] + box[1]
        pyautogui.click(x, y)   
    pyautogui.click(conttest[:,0,:][0,0] + box[0] , conttest[:,0,:][0,1]+box[1])
    #
    ##############

if __name__ == "__main__":
    fire.Fire(wall_detection)
    