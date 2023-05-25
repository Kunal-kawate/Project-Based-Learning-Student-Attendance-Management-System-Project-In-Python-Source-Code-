import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
#------------------------------Whats App message Code Librarys----------------------------------

import pyautogui as pg
import webbrowser as web
import time
import pandas as pd
import pywhatkit
# -----------------------------------End of code -----------------------------------------------
video_capture = cv2.VideoCapture(0)


# ----------------------------Data of students-------------------------------------------------
no_list={"Kunal kawate":"91_8788654516","Kunal Paithane":"91_8788654516","shreyas":"91_8788654516","Ritesh":"91_8788654516"}
# ----------------------------End----------------------------------------------------------------


jobs_image = face_recognition.load_image_file("photos/kunya.jpg")
jobs_encoding = face_recognition.face_encodings(jobs_image)[0]
 
ratan_tata_image = face_recognition.load_image_file("photos/kunalp.jpg")
ratan_tata_encoding = face_recognition.face_encodings(ratan_tata_image)[0]
 
sadmona_image = face_recognition.load_image_file("photos/rcbsamrthak.jpg")
sadmona_encoding = face_recognition.face_encodings(sadmona_image)[0]

s_image = face_recognition.load_image_file("photos/shreyas.jpg")
s_encoding = face_recognition.face_encodings(s_image)[0]
 
known_face_encoding = [
jobs_encoding,
ratan_tata_encoding,
sadmona_encoding,
s_encoding
]
 
known_faces_names = [
"Kunal kawate",
"Kunal Paithane",
"Ritesh",
"shreyas"
]
 
students = known_faces_names.copy()
 
face_locations = []
face_encodings = []
face_names = []
s=True
 
 
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
 
 
 
f = open(current_date+'.csv','w+',newline = '')
lnwriter = csv.writer(f)
lnwriter.writerow(["Name of Students","Phone No.","Log","Message"])
 
while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name=""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]
 
            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10,100)
                fontScale              = 1.5
                fontColor              = (255,0,0)
                thickness              = 3
                lineType               = 2
 
                cv2.putText(frame,name+' Present', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
 
                if name in students:
                    students.remove(name)
                    name1=no_list[name]
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,name1,"Present","-"])

    cv2.imshow("attendence system",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# -------------------change---------------------------
for item in students:
    item1=no_list[item]
    lnwriter.writerow([item,item1,"Absent","Dear Parent "+item+" is absent from college today, if you are unaware of this, please contact the office on 01-12345-789 , Thank You!; Mail From: *Dr. D. Y. Patil Institute Of Technology, Pimpari Pune* "])
# ---------------------------------------------------

video_capture.release()
cv2.destroyAllWindows()
f.close()

# ------------------------------whats code-----------------------------

data = pd.read_csv(current_date+'.csv')
data_dict = data.to_dict('list')
student_name_list=data_dict["Name of Students"]
leads = data_dict["Phone No."]
messages = data_dict["Message"]
d_log=data_dict["Log"]
combo = zip(leads,messages,d_log,student_name_list)
first = True
time.sleep(6)
for lead,message,log,stu_name in combo:
    if(log == "Absent"):
        pywhatkit.sendwhatmsg_instantly(lead, message,10,True,10)
        print("\nMessage has been sent Successfully to "+stu_name)
# --------------------end code----------------------------------------------------------

print("\n-----------------------------Exit----------------------------\nThank You for using this program.......\n")
