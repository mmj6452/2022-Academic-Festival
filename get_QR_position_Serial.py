import pyzbar.pyzbar as pyzbar
import cv2
import serial
from common.function import onchange

# 비디오캡쳐 열기
cap_1 = cv2.VideoCapture(0)
cap_2 = cv2.VideoCapture(1)

# 전역변수 설정
global QR_Position

x, y, w, h = 0, 0, 0, 0

# 아두이노 시리얼통신 설정

pi_port = "COM6"
pi_serial = serial.Serial(pi_port, 115200, timeout=1)

while True:
    # 프레임 읽어오기
    ret, frame = cap_1.read()
    if not ret:
        continue
    ret_2, frame_2 = cap_2.read()
    if not ret_2:
        continue
    # 프레임 그레이스케일로 저장
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ZBar 디코드
    decoded = pyzbar.decode(gray)
    # 좌표값과 길이 높이값읽어오기
    for d in decoded:
        x, y, w, h = d.rect
        barcode_data = d.data.decode("utf-8")
        # QR코드가 있는 곳에 네모그리기
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # QRcode 위치에 QRcode 정보 띄워주기
        text = '%s' % barcode_data
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    # 이미지 띄워주기
    cv2.imshow('frame', frame)
    # q를 누르면 종료
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    # QRcode 중앙좌표 읽어오기
    QR_Position = str([x + (h / 2)]) + str([y + (w / 2)])
    print(QR_Position)  # print the center of the QR code5
    # 아두이노에서 요청이 오면 좌표값 보내주기
    change = onchange(frame)
    cv2.imshow("test", frame_2)

    if change >= 50:
        pi_serial.write("stop".encode())
        print("send to arduino")

    if pi_serial.readable():
        if pi_serial.readline().decode("utf-8") == "give me the position":
            pi_serial.write(QR_Position.encode())

cap_1.release()
cv2.destroyAllWindows()
