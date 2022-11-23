import cv2
import numpy as np

cap = cv2.VideoCapture(0)

area_of_non_interest = (300,500)

mask_1 = np.ones((480, 640), np.uint8)
mask_2 = np.ones(area_of_non_interest, np.uint8)
mask_hight , mask_width = mask_1.shape[0:2]
mask_center = (mask_width/2, mask_hight/2)
mask = np.concatenate((mask_1, mask_2), axis=1)

while True:
    # 프레임 읽어오기
    ret, frame = cap.read()
    if not ret:
        continue
    # 프레임을 HSV로 저장
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    
    cv2.imshow('frame', frame)
    
    # q를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()