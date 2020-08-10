import cv2 
import pyautogui
  


img = cv2.imread("test.png") 
orig_img = img.copy()
image_coords = pyautogui.locateOnScreen(orig_img, confidence=0.9)
#conttest = np.vstack(contours)
#conttest[:,0,:]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
  
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30)) 
  
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
im2 = img.copy()

cv2.drawContours(im2, contours, -1, (0,255,0), 3)


cv2.imshow("Wall Detection", im2)
cv2.waitKey(0)