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
        

def onchange(frame):
    roi=(40,40,400,400)
    mask_1 = np.zeros((40,400),np.uint8)
    mask_2 = np.zeros((480,40),np.uint8)
    mask_3 = np.zeros((480,200),np.uint8)
    
    cv2.rectangle(frame, roi, (255, 255, 255), cv2.FILLED)# 동영상에 하얀마스크 씌우기
    bgr=cv2.split(frame)#프레임을 3개 채널로 분리
    frame_blue = bgr[0]#Blue채널
    frame_green = bgr[1]#Green채널
    frame_red = bgr[2]#Red채널
    B_histogram = cv2.calcHist([frame_blue], [0], None, [32], [0, 256])
    G_histogram = cv2.calcHist([frame_green], [0], None, [32], [0, 256])
    R_histogram = cv2.calcHist([frame_red], [0], None, [32], [0, 256])
    histo_sum = B_histogram + G_histogram + R_histogram
    B_low_sum = np.sum(B_histogram[0:15])
    G_low_sum = np.sum(G_histogram[0:15])
    R_low_sum = np.sum(R_histogram[0:15])
    histo_low_sum = B_low_sum + G_low_sum + R_low_sum
    R_histogram_img=draw_histo(histo_sum)
    R_histogram_img=cv2.resize(R_histogram_img,(400,400),interpolation=cv2.INTER_AREA)##작동확인
    
        
    sum_1 = cv2.vconcat([mask_1,R_histogram_img])
    sum_1 = cv2.vconcat([sum_1,mask_1])
    sum_1 = cv2.hconcat([sum_1,mask_3])
    sum_1 = cv2.hconcat([mask_2,sum_1])
    sum_1 = cv2.cvtColor(sum_1,cv2.COLOR_GRAY2BGR)
    frame_red = cv2.subtract(frame, sum_1)
    
    put_string(frame_red, 'minval_R', (20, 30), R_low_sum)
    cv2.imshow("change_detect",frame_red)

    return R_low_sum