print('Please Wait...')

import face_recognition
import cv2
import numpy as np
import firebase as firebase
import glob
import os
from datetime import datetime
import serial as serial
import pandas as pd



class Arc:
    def __init__(self):
        self.dirname = '.\\images'
        self.temp = []
        self.info = []
        if not os.path.exists(os.path.abspath(self.dirname)):
            os.mkdir(os.path.abspath(self.dirname))

            
            #self.storage = firebase.screening() 



    def extract_info(self,response):
        print('nothing')



    def upload(self):
        print('')


    def face_recognition(self,file_name):
        
        try:
            
       

            
            print("file name-"+file_name)
         
            #video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)





            # Initialize some variables
            face_locations = []
            face_encodings = []
            face_names = []
            process_this_frame = True
            i = 0
            face_detect = True
            while face_detect:
                # Grab a single frame of video
                ret, frame = video_capture.read()

                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Only process every other frame of video to save time
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        face_detect=False
                        name = "Unknown"
                        cv2.imwrite(os.path.abspath(os.path.join(self.dirname,(datetime.today().strftime('%Y-%m-%d')+'-'+file_name+'-'+str(++i)+'.png'))),frame)
                        self.storage.upload(self.dirname,(datetime.today().strftime('%Y-%m-%d')+'-'+file_name+'-'+str(i)+'.png'))


                        i = i+1
                        

                        print("I see someone named {}!".format(name))
                        # # If a match was found in known_face_encodings, just use the first one.
                        # if True in matches:
                        #     first_match_index = matches.index(True)
                        #     name = known_face_names[first_match_index]

                        # Or instead, use the known face with the smallest distance to the new face
                        

                process_this_frame = not process_this_frame


                # Display the results
                #for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                #    top *= 4
                #   right *= 4
                    #  bottom *= 4
                    #  left *= 4

                    # Draw a box around the face
                    #  cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    #  cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    #  font = cv2.FONT_HERSHEY_DUPLEX
                    #  cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                # Display the resulting image
                # cv2.imshow('Video', frame)

                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release handle to the webcam
            
        except Exception as ex:
                    template = "Camera exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message)
        finally:
                    video_capture.release()
                    cv2.destroyAllWindows()


        

    def read_temperature(self):
        #self.ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1)
        temp = []
        while True:
            #ser.write(b'0x55,0xAA,5,1,4')
            #response = ser.readline()
            response = b''''====================================\r\n'
b'T Ambience = 31.130 C\r\n'
b'1234.623\r\n'
b'1259.302\r\n'
b'vs = 24.680\r\n'
b'vs = 45.240, calibrate modify\r\n'
b'vs = 46.192, emissivity compensate\r\n'
b'to1 = 33.592\r\n'
b'to2 = 34.569\r\n'
b'T Object = 33.709 C\r\n'
b'T body = 34.128 C, ambience compensate\r\n'
b'T body = 36.353 C, weak low\r\n'
b'cfg.mode = 1\r\n'
b'Vbat = 3270.365\r\n' '''
            if 'body' in str(response):
                temp.append(str(response))
        
            elif 'Vbat' in str(response):
                if len(temp)!=0:
                    self.info = temp 
                    print(self.info)
                    self.face_recognition('demo')

                    temp = []
            
        


if __name__ == '__main__':
    print('Device Ready.')
    #arc = Arc()
    #arc.read_temperature()