import numpy as np
import cv2
import time
import face_recognition
from datetime import datetime
import os
from tele_notification import send_message


#import the cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

def TakeSnapshotAndSave():
    # access the webcam (every webcam has a number, the default is 0)
    cap = cv2.VideoCapture(0)

    num = 0 
    while num<1:
        # Capture frame-by-frame
        time.sleep(1)
        ret, frame = cap.read()fa

        # to detect faces in video
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

        x = 0
        y = 20
        text_color = (0,255,0)

        
        current_time = datetime.now().strftime("%m-%d-%Y,%H:%M:%S") # current date and time
        path = "captured_faces"

        cv2.imwrite("captured_faces/" + current_time+'.jpg',frame)
        num = num+1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return current_time


def Face_Recognition(captured_file_name):

    # Load the jpg files into numpy arrays
    known_image = face_recognition.load_image_file("known_faces/barack.jpg")
    detected_image = face_recognition.load_image_file("captured_faces/" + captured_file_name + '.jpg')


    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
    no_of_faces = face_recognition.face_locations(detected_image)
    if len(no_of_faces)==0:
        os.remove("captured_faces/" + captured_file_name + '.jpg')
        return "There are no face detected!"
    else:
        try:
            detected_face_encoding = face_recognition.face_encodings(detected_image)
            known_face_encoding = face_recognition.face_encodings(known_image)[0]

        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            quit()

        known_faces = [
            known_face_encoding
        ]


        # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
        final_file_name = "captured_faces/" + captured_file_name + '.jpg'
        for one_detected_face_encoding in detected_face_encoding:
            result = face_recognition.compare_faces(known_faces,one_detected_face_encoding)
            if result[0] == False:
                send_message('Stranger detected', final_file_name)
                return False
        send_message('Elderly came back', final_file_name)
        return True

if __name__ == "__main__":
    file_name_created = TakeSnapshotAndSave()
    print(Face_Recognition(file_name_created))
