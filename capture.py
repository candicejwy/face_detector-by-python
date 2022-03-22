import cv2,time,pandas
from datetime import datetime


first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start","End"])
#The numbers in parentheses can be 0,1,2,3, or the video file path.
video = cv2.VideoCapture(0)

#a = 1
while True:
    #a = a+1
    check, frame = video.read()
    status =0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Blur the image
    gray = cv2.GaussianBlur(gray,(21,21),0)
   
    if first_frame is None:
        first_frame = gray
        continue  # go to the while loop and don't go down the following command

    delta_frame = cv2.absdiff(first_frame,gray)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations =2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour)<10000:
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0),3)

   # time.sleep(3)
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    status_list.append(status)

    # save the memory by keeping the last two
    status_list =status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    cv2.imshow("Gray Frame",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("THreshold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)
    # make sure you have a buton to close the window
    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break
print(status_list)
print(times)

for i in range(0,len(times),2):
    df2 = pandas.DataFrame({"Start":times[i],"End":times[i+1]},index={1})
    df = pandas.concat([df,df2],ignore_index=True)
#print(a)
video.release() 
cv2.destroyAllWindows
df.to_csv("Times.csv")