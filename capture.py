# Data creation
import numpy as np # We'll be storing our data as numpy arrays
import os # For handling directories
from PIL import Image # For handling the images
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # Plotting
from keras.models import load_model
import cv2

lookup = {'Fist': 0, 'Nothing': 1, 'Palm': 2, 'Swing': 3, 'Thumb': 4, 'Yo': 5}

reverselookup = {0: 'Fist', 1: 'Nothing', 2: 'Palm', 3: 'Swing', 4: 'Thumb', 5: 'Yo'}

cap = cv2.VideoCapture(0)
flag = True
count = 1
print("Select option" + str(reverselookup))
option = int(input())
_, first_frame = cap.read()
roi = first_frame[100:400,0:300]
first_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
first_roi = cv2.GaussianBlur(first_roi, (5, 5), 0)



while True:
    _,frame = cap.read()
    
    if flag:
        if cv2.waitKey(60) & 0xFF == ord('r'):
            flag = False
        else:
            cv2.rectangle(frame,(0,100),(300,400),(0,255,0))
            roi = frame[100:400,0:300]
    
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
    
            difference = cv2.absdiff(first_roi, gray_roi)
            #_, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
            cv2.imshow("difference",difference)
            
            
    else:
        cv2.rectangle(frame,(0,100),(300,400),(0,255,0))
        roi = frame[100:400,0:300]
    
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
    
        difference = cv2.absdiff(first_roi, gray_roi)
        #_, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        cv2.imshow("difference",difference)
        cv2.imwrite('dataset/'+reverselookup[option] +'/image' + str(count) + '.png', difference)
        count += 1
        if count%100 == 0:
            print(count)     
    
    if cv2.waitKey(200) & 0xFF == 27: # you can increase delay to 2 seconds here
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()