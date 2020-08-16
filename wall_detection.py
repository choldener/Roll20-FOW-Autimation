import cv2 
import pyautogui
import numpy as np
import time
import fire
import scipy.spatial.distance

pyautogui.FAILSAFE = True

def wall_detection(IMAGE, approx = True, kernel = (15,15),epsilon_value= 0.005):
    
    img = cv2.imread(IMAGE) 
    
    ####################
    #IMAGE RECOG
    #
    box = pyautogui.locateOnScreen(img, confidence=0.9)
    if box is None:
        raise RuntimeError("Could not detect iamge on screen")
    #
    ####################
    
    ####################
    #Computer Vision
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel) 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    im2 = img.copy()
    cv2.drawContours(im2, contours, -1, (0,255,0), 3)
    #
    ####################

    ####################
    # Testing
    # 
    # for array in contours:
    #     conttest = np.vstack(array)
    #     #print(conttest)
    #     print("SPACE")
    #     # global distance
    #     # for c in conttest:
    #     #     #calculate distance
    #     #     pass
    #     # if distance > 10:
    #     for index, c in enumerate(conttest):
    #         print(c)
    #         print(index)
    #         if index > 0:
    #             print(array[index - 1])
    #             d = scipy.spatial.distance.cdist(array[index-1],array[index])
    #             print('distance: '+ str(d))
    #         x = c[0] #+ box[0]
    #         y = c[1] #+ box[1]
            #print('x:' + str(x))
            #print('y:'+str(y))
            #d = scipy.spatial.distance.cdist(x,y)
            #print(d)
        #print(conttest)
        #print('x_first: ' + str(conttest[0][0] ))#+ box[0]))
        #print('y_first:'+ str(conttest[0][1] ))#+ box[1]))
    #
    ####################
    #Contour testing
    # 
    cv2.imshow("Wall Detection", im2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #
    ####################
    
    ####################
    #Clicking Script
    #
    time.sleep(3)
    if approx == True:
        print('approx')
        for array in contours:
            #print(array)
            epsilon = epsilon_value*cv2.arcLength(array,True)
            approx = cv2.approxPolyDP(array,epsilon,True)
            approx = np.vstack(approx)
            time.sleep(1)
            for c in approx:
                x = c[0] + box[0]
                y = c[1] + box[1]
                pyautogui.click(x, y)
            pyautogui.click(approx[0][0] + box[0] , approx[0][1]+box[1])
            pyautogui.click(approx[0][0] + box[0] , approx[0][1]+box[1], button='right')
    else: 
        print("not approx")
        for array in contours:
            conttest = np.vstack(array)
            for index, c in enumerate(conttest):
                if index == 1:
                    d = scipy.spatial.distance.cdist(array[index-1],array[index])
                    if  d < 2.5:
                        continue
                x = c[0] + box[0]
                y = c[1] + box[1]
                pyautogui.click(x, y)   
            pyautogui.click(conttest[0][0] + box[0] , conttest[0][1]+box[1])
            pyautogui.click(conttest[0][0] + box[0] , conttest[0][1]+box[1], button='right')
    #
    ####################
    
# if __name__ == "__main__":
#     fire.Fire(wall_detection)
    