import cv2
import numpy as np
#화면에 
def put_string(frame,text,pt,value,color=(120,200,90)):
    text +=str(value)
    shade=(pt[0]+2, pt[1]+2)
    font= cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,text,shade,font,0.7,(0,0,0),2)
    cv2.putText(frame, text, pt, font, 0.7,color, 2)

capture = cv2.VideoCapture(0)
if capture.isOpened()==False:raise Exception("no camera from 1_4_")

#capture.set(cv2.CAP_PROP_FRAME_WIDTH,480)
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

title="video_BGR"
cv2.namedWindow(title)
roi=(40,40,400,400)


while True:
    ret,frame=capture.read()
    if not ret:break
    if cv2.waitKey(30)>=0:break
    #bgr 자료형은 list고 원소의 단일채널 자료형은 numpy.ndarray라서 호환이 안됨
    #단일 채널로 분할해서 최소값을 구하고 세개의 값중 가장 낮은 값을 찾거나 평균내서 최소값 확인해도됨
    #평균을 낼경우 하얀색 a4에서 120이 나온다면 이물질이 들어와 그림자가 생길경우 바로 10이하의 값이 나오고
    #그림자가 생기지 않을경우에도 하얀색 이물질이 아니라면 수치가 매우 떨어짐(=검출이 잘됨)
    cv2.rectangle(frame, roi, (255, 255, 255), cv2.FILLED)# 동영상에 하얀마스크 씌우기
    #cv2.rectangle(frame, roi, (0, 0, 0), cv2.FILLED)  # 동영상에 까만마스크 씌우기
    bgr=cv2.split(frame)#프레임을 3개 채널로 분리
    frame1 = bgr[0]#Blue채널
    frame2 = bgr[1]#Green채널
    frame3 = bgr[2]#Red채널

    minvalue_B, maxvalue_B, min_loc_B, max_loc_B = cv2.minMaxLoc(frame1)
    minvalue_G, maxvalue_G, min_loc_G, max_loc_G = cv2.minMaxLoc(frame2)
    minvalue_R, maxvalue_R, min_loc_R, max_loc_R = cv2.minMaxLoc(frame3)
    
    R_histogram = cv2.calcHist([frame3], [0], None, [256], [0, 256])
    G_histogram = cv2.calcHist([frame2], [0], None, [256], [0, 256])
    B_histogram = cv2.calcHist([frame1], [0], None, [256], [0, 256])
    
    R_low_sum = np.sum(R_histogram[0:50])
    G_low_sum = np.sum(G_histogram[0:50])
    B_low_sum = np.sum(B_histogram[0:50])
    
    low_sum = int((R_low_sum + G_low_sum + B_low_sum)/3)
    
    print("R_histogram = ",R_low_sum)

    
    #minvalue_BGR=(minvalue_B+minvalue_G+minvalue_R)/3 # 평균으로 구하고 싶은 경우

    '''
    if minvalue_R<=minvalue_B and minvalue_R<=minvalue_G:
        minvalue_BGR=minvalue_R
    elif minvalue_B<=minvalue_R and minvalue_B<=minvalue_G:
        minvalue_BGR=minvalue_B
    elif minvalue_G<=minvalue_B and minvalue_G<=minvalue_R:
        minvalue_BGR=minvalue_G
        '''
    #maxvalue_BGR = (maxvalue_B + maxvalue_G + maxvalue_R) / 3
    #minvalue=cv2.min(frame,(255,255,255))#mask가 포함된 이미지의 값을 확인하는건 맞음 그러나 frame을 바로 넣으면 파일 형식이 list형이되어 cv.min이 정상적으로 작동하지 않음
    #maxvalue=cv2.max(frame,(0,0,0))#mask가 포함된 이미지의 값을 확인하는건 맞음
    #minval로 해야 밝은곳(255,255,255)에 어두운게(0,0,0) 침입했을떄 확인가능
    

    put_string(frame, 'minval', (20, 30), low_sum)
    put_string(frame1, 'minval_B', (20, 30), minvalue_B)
    put_string(frame2, 'minval_G', (20, 30), minvalue_G)
    put_string(frame3, 'minval_R', (20, 30), minvalue_R)
    
    cv2.imshow('f1_B',bgr[0])
    cv2.imshow('f2_G',bgr[1])
    cv2.imshow('f3_R',bgr[2])
    #put_string(frame,'maxval',(10,30),maxvalue_BGR)
    cv2.imshow(title,frame)

capture.release()