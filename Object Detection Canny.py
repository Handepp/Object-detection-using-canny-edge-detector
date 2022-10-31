import cv2  
import numpy as np  
  
frameWidth = 640
frameHeight = 480
cam = cv2.VideoCapture(0)
cam.set(3, frameWidth)
cam.set(4, frameHeight)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",23,255,empty)
cv2.createTrackbar("Threshold2","Parameters",20,255,empty)
cv2.createTrackbar("Area","Parameters",5000,30000,empty)

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt) 
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255,255,0), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)

            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)


while True:
    ret, img= cam.read()
    imgContour = img.copy()
    blurred = cv2.GaussianBlur(img, (7, 7), 1)
    gray=cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    
    canny = cv2.Canny(gray,threshold1,threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(canny, kernel, iterations=1)
    getContours(imgDil,imgContour)

    #cv2.imshow('Deteksi Objek', img)
    #cv2.imshow('Deteksi Objek', canny)
    #cv2.imshow('Deteksi Objek', imgDil)
    cv2.imshow('Deteksi Objek', imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the window   
cam.release()  
  
# De-allocate any associated memory usage   
cv2.destroyAllWindows()  