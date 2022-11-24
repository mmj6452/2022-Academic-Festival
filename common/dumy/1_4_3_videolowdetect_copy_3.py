import cv2
import numpy as np

#카메라 480*640
#마스크 40~440
#화면에 

def put_string(frame,text,pt,value,color=(120,200,90)):
    text +=str(value)
    shade=(pt[0]+2, pt[1]+2)
    font= cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,text,shade,font,0.7,(0,0,0),2)
    cv2.putText(frame, text, pt, font, 0.7,color, 2)

def calc_histo(image,histSize,ranges=[0,256]):
    hist=np.zeros((histSize,1),np.float32)
    gap=ranges[1]/histSize
    for row in image:
        for pix in row:
            idx=int(pix/gap)
            hist[idx]+=1
        return hist

def draw_histo(hist,shape=(200,256)):
    hist_img=np.full(shape,255,np.uint8)
    cv2.normalize(hist,hist,0,shape[0],cv2.NORM_MINMAX)
    gap=hist_img.shape[1]/hist.shape[0]
    
    for i,h in enumerate(hist):
        x=int(round(i*gap))
        w=int(round(gap))
        cv2.rectangle(hist_img,(x,0,w,int(h)),0,cv2.FILLED)
    
    return cv2.flip(hist_img,0)\
        
mask_1 = np.zeros((40,400),np.uint8)
mask_2 = np.zeros((480,40),np.uint8)
mask_3 = np.zeros((480,200),np.uint8)



        
        
capture = cv2.VideoCapture(0)
if capture.isOpened()==False:raise Exception("no camera from 1_4_")

#capture.set(cv2.CAP_PROP_FRAME_WIDTH,480)
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

title="video_BGR"
cv2.namedWindow(title)
roi=(40,40,400,400)

def on_change(frame):
    ret,frame=capture.read()
    cv2.rectangle(frame, roi, (255, 255, 255), cv2.FILLED)# 동영상에 하얀마스크 씌우기
    bgr=cv2.split(frame)#프레임을 3개 채널로 분리
    frame3 = bgr[2]#Red채널

    minvalue_R, maxvalue_R, min_loc_R, max_loc_R = cv2.minMaxLoc(frame3)
        
    R_histogram = cv2.calcHist([frame3], [0], None, [32], [0, 256])
        
    R_histogram_img=draw_histo(R_histogram)
        
    R_low_sum = np.sum(R_histogram[0:15])
        
    h_R_histo, w_R_histo=frame3.shape[:2]
        
        
    R_histogram_img=cv2.resize(R_histogram_img,(400,400),interpolation=cv2.INTER_AREA)##작동확인
        
    sum_1 = cv2.vconcat([mask_1,R_histogram_img])
    sum_1 = cv2.vconcat([sum_1,mask_1])
    sum_1 = cv2.hconcat([sum_1,mask_3])
    sum_1 = cv2.hconcat([mask_2,sum_1])
        
        ##crop_R_histo = R_histogram_img[0:h_R_histo, 0:w_R_histo]
        
        
    h,w=R_histogram_img.shape[:2]
        
    put_string(frame3, 'minval_R', (20, 30), minvalue_R)
        
    frame3 = cv2.subtract(frame3, sum_1)
        
        
        
    cv2.imshow(title,frame3)
    

    capture.release()
    return R_low_sum