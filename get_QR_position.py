import pyzbar.pyzbar as pyzbar
import cv2
import serial

# 비디오캡쳐 열기
cap = cv2.VideoCapture(0)

# 전역변수 설정
global QR_Position


x, y, w, h = 0, 0, 0, 0

# 아두이노 시리얼통신 설정
arduino_port = "COM6"
arduino_serial = serial.Serial(arduino_port, 115200, timeout=1)

while True:
    # 프레임 읽어오기
    ret, frame = cap.read()
    if not ret:
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
    QR_Position = str([x + (h / 2)])+str([y + (w / 2)])
    print(QR_Position)  # print the center of the QR code
    # 아두이노에서 요청이 오면 좌표값 보내주기
    if arduino_serial.readable():
        if arduino_serial.readline().decode("utf-8"):
            arduino_serial.write(QR_Position.encode())
cap.release()
cv2.destroyAllWindows()
