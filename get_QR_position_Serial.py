import cv2
import serial
from common.function import onchange
from common.function import find_coordinate


# 변수설정
motion_threshold = 50
x, y, w, h = 0, 0, 0, 0
# 아두이노 시리얼통신 설정
pi_port = "COM6"
pi_serial = serial.Serial(pi_port, 115200, timeout=1)

# 비디오캡쳐 열기
cap_QR = cv2.VideoCapture(0)
cap_motion = cv2.VideoCapture(1)

# 전역변수 설정
global QR_Position

while True:
    # 프레임 읽어오기
    ret, frame_QR = cap_QR.read()
    if not ret:
        continue
    ret_2, frame_motion = cap_motion.read()
    if not ret_2:
        continue
    # 프레임 그레이스케일로 저장
    gray_QR_frame = cv2.cvtColor(frame_QR, cv2.COLOR_BGR2GRAY)
    # 관심영역의 변화를 측정
    change = onchange(frame_motion)
    # 관심영역의 변화가 특정값이상이면 시리얼로 stop 보냄
    if change >= motion_threshold:
        pi_serial.write("stop".encode())
        print("send to arduino")
    # 라즈베리파이에서 요청이 오면 좌표값 보내주기
    if pi_serial.readable():
        if pi_serial.readline().decode("utf-8") == "give me the position":
            QR_Position = find_coordinate(gray_QR_frame)
            pi_serial.write(QR_Position.encode())
        # q를 누르면 종료
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cap_QR.release()
cap_motion.release()
cv2.destroyAllWindows()
