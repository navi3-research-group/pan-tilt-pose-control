import cv2
import numpy as np
import dlib  
import os 
import pandas as pd
import math
from time import time
import serial



def moveServos(positionServo):
    dictComm = {'Center': 's90,90\n',
                'Right': 's70,90\n',
                'Left': 's120,90\n',
                'Up': 's90,120\n',
                'Down': 's90,70\n',
                'Up-right': 's70,120\n',
                'Up-left': 's120,120\n',
                'Down-right': 's70,70\n',
                'Down-left': 's120,70\n'}
    print(dictComm[positionServo])
    ser.write(bytes(dictComm[positionServo].encode('utf8')))


ser = serial.Serial('com6',9600)

ser.write(b'hhhhh')
#textRead = ser.readline()  


pan = 90
tilt = 90





from keras.models import load_model
modelLoad = load_model('model\\model_9_positions.h5')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video-test-NN.avi',fourcc, 10, (320,240))


    
#capture source video
cap = cv2.VideoCapture(0)





detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  


font = cv2.FONT_HERSHEY_SIMPLEX







while True:
    start = time()

#    frame_num += 1
    ret, frameOrig = cap.read()
    height = frameOrig.shape[0]
    width = frameOrig.shape[1]
    frame = cv2.resize(frameOrig, (int(width/2), int(height/2))) 
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
#    cv2.imshow("Gray", gray)  
     
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    claheImg = clahe.apply(gray)
    cv2.imshow("CLAHE", claheImg)
     
     
    faces = detector(claheImg, 0)  
    print("Found {0} faces!".format(len(faces)))  
      
    # Draw a rectangle around the face 
    if len(faces) >= 1:
        maxArea = 0
        for rect in faces: 
            #print(rect.area())
            if rect.area() >= maxArea:
                rectFace = rect
                maxArea = rect.area()
    #            print(maxArea)
        
          
        landmarks = np.matrix([[p.x, p.y]  
                      for p in predictor(frame, rectFace).parts()])  
          
        landmarks_display = landmarks[:60]  
        x, y, w, h = cv2.boundingRect(landmarks_display)
          
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
          
        centerX = int(x + round(w/2))
        centerY = int(y + round(h/2))
        cv2.circle(frame,(centerX,centerY), 2, (0,0,255), 2)
          
        for idx, point in enumerate(landmarks_display):
            pos = (point[0, 0], point[0, 1])  
            cv2.circle(frame, pos, 2, color=(0, 255, 255), thickness=-1)  
        
        d = []
        for ppoints in landmarks_display:
            d.append(math.sqrt((centerX-ppoints[0,0])**2+(centerY-ppoints[0,1])**2))
        
           
        
        dnp = np.array([d])
        dd = dnp/max(max(dnp))
        pred = modelLoad.predict(dd)
        
        
        positionLabel = np.argmax(pred)
        dictPos = {
                0: 'Center',
                1: 'Right',
                2: 'Left',
                3: 'Up',
                4: 'Down',
                5: 'Up-right',
                6: 'Up-left',
                7: 'Down-right',
                8: 'Down-left'
                }
        
        if max(pred[0,:])>.8:
            positionServo = dictPos[positionLabel]
            moveServos(positionServo)
            text = dictPos[positionLabel]+', conf: '+str(max(pred[0,:]))
        else:
            text = 'Not sure'
        cv2.putText(frame,text,(10,30), font, 0.8,(0,0,255),2)
        
    cv2.imshow("Landmarks found", frame) 
#    out.write(frame)
    stop = time()
    print(1/(stop-start))
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
    
#    stop = time()
#    print(1/(stop-start))
cv2.destroyAllWindows()
out.release()
cap.release()
ser.close()  
