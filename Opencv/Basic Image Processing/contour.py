import numpy as np
import cv2


frame = cv2.imread("brazing.jpg")


frame = cv2.resize(frame, (640,480))

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#gray=cv2.equalizeHist(gray)
gray = cv2.GaussianBlur(gray, (15, 15), 0)

#gray = cv2.medianBlur(gray,5)

#thresh = cv2.threshold(gray, 200, 255,cv2.THRESH_BINARY +  cv2.THRESH_OTSU)[1]
thresh= cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,2)
kernel = np.ones((1, 1), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,kernel, iterations=2)

closing_img = closing.copy()
contours,_ = cv2.findContours(closing_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
count=0
for cnt in contours:
	
    area = cv2.contourArea(cnt)
    
    if (area < 100) | (area> 900):
        continue
    count+=1	
    print(area) 
    ellipse = cv2.fitEllipse(cnt)
    cv2.ellipse(frame, ellipse, (0,255,0), 2)
    hull=cv2.convexHull(cnt)
    harea=cv2.contourArea(hull)
    print(harea)
    x,y,w,h=cv2.boundingRect(cnt)
   # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),lineType=8)
   # cv2.putText(frame,str(count),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
cv2.putText(frame,"Count  :"+str(count),(12,28),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
cv2.imshow("Morphological Closing", closing)
cv2.imshow("Adaptive Thresholding", thresh)
cv2.imshow('Contours', frame)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()





