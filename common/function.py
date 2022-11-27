import numpy as np
import pyzbar.pyzbar as pyzbar
import cv2


# 카메라 480*640
# 마스크 40~440
# 화면에

# 화면에 글자 만들어주는 함수
def put_string(frame, text, pt, value, color=(120, 200, 90)):
    text += str(value)
    shade = (pt[0] + 2, pt[1] + 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, shade, font, 0.7, (0, 0, 0), 2)
    cv2.putText(frame, text, pt, font, 0.7, color, 2)


def draw_histo(hist, shape=(200, 256)):
    hist_img = np.full(shape, 255, np.uint8)
    cv2.normalize(hist, hist, 0, shape[0], cv2.NORM_MINMAX)
    gap = hist_img.shape[1] / hist.shape[0]

    for i, h in enumerate(hist):
        x = int(round(i * gap))
        w = int(round(gap))
        cv2.rectangle(hist_img, (x, 0, w, int(h)), 0, cv2.FILLED)

    return cv2.flip(hist_img, 0)


# 프레임에서 무관심영역에서 움직이는 객채가 있는지 확인후 있다면 해당 변화를 수치화해서 반환
def onchange(frame):
    area_of_non_interest = [40, 40, 400, 400]
    mask = np.zeros((480, 640), np.uint8)

    cv2.rectangle(frame, area_of_non_interest, (255, 255, 255), cv2.FILLED)  # 동영상에 하얀마스크 씌우기
    b, g, r = cv2.split(frame)  # 프레임을 3개 채널로 분리
    B_histogram = cv2.calcHist([b], [0], None, [32], [0, 256])
    G_histogram = cv2.calcHist([g], [0], None, [32], [0, 256])
    R_histogram = cv2.calcHist([r], [0], None, [32], [0, 256])
    histo_sum = B_histogram + G_histogram + R_histogram
    histo_low_sum = np.sum(B_histogram[0:15]) + np.sum(G_histogram[0:15]) + np.sum(R_histogram[0:15])
    histogram_img = draw_histo(histo_sum)
    histogram_img = cv2.resize(histogram_img, (400, 400), interpolation=cv2.INTER_AREA)  # 작동확인

    # 마스크 만드는 부분 좀더 깔끔하게 수정함 이거 작동안되면 기존거로 변경바람
    mask[40:440, 40:440] = histogram_img
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    frame = cv2.subtract(frame, mask)

    put_string(frame, 'histo_low_sum', (20, 30), histo_low_sum)
    cv2.imshow("change_detect", frame)

    return histo_low_sum


# 프레임에서 QR을 찾아 해당 좌표값을 반환해주는 함수
def detect_qr(frame , pos):
    x, y, w, h = 0, 0, 0, 0
    # 그리드 원하는 그리드로 변경해주세요
    decoded = pyzbar.decode(frame)
    # 좌표값과 길이 높이값읽어오기
    print(decoded)
    for d in decoded:
        x, y, w, h = d.rect
        barcode_data = d.data.decode("utf-8")
        # QR코드가 있는 곳에 네모그리기
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # QRcode 위치에 QRcode 정보 띄워주기
        text = '%s' % barcode_data
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("test %s"%pos, frame)
    # QRcode 중앙좌표 읽어오기
    QR_Position = str([x + (h / 2)]) + str([y + (w / 2)])
    #barcode
    
    return frame, QR_Position,pos



# 프레임에서 그리드 순서대로 pose 만들어 배열에 순서대로 저장 0값이면 해당 pose QR이 없는것이고 0이 아니면 해당 좌표값이 저장될것
# 잘라진 프레임에서의 좌표값임으로 해당 좌표값만큼 수정해주거나 단순히 possess 좌표를 찾아가게 만들것
def find_coordinate(frame):
    pos_frame = [0, 0, 0, 0, 0, 0, 0, 0]
    QR_Position= [0, 0, 0, 0, 0, 0, 0, 0]
    pos = [0, 0, 0, 0, 0, 0, 0, 0]
    # 프레임을 각 그리드로 나눔 나중에 화면에 맞는 그리드로 변경바람
    pos_1 = frame[40:140, 40: 240]
    pos_2 = frame[140:240, 40: 240]
    pos_3 = frame[240:340, 40: 240]
    pos_4 = frame[340:440, 40: 240]
    pos_5 = frame[40:140, 240: 440]
    pos_6 = frame[140:240, 240: 440]
    pos_7 = frame[240:340, 240: 440]
    pos_8 = frame[340:440, 240: 440]
    # 화면에 QR코드가 없으면 QR_position 0인지 아닌지 카메라가 없어서 확인불가 확인후 수정바람

        
        
    pos_frame[0] ,QR_Position[0],pos[0]= detect_qr(pos_1,"pos_1")
    cv2.rectangle(pos_frame[0], (0,0),(200,100), (100, 100, 100),1)
    pos_frame[1],QR_Position[1],pos[1]= detect_qr(pos_2,"pos_2")
    cv2.rectangle(pos_frame[1], (0,0),(200,100), (100, 100, 100),1)
    pos_frame[2],QR_Position[2],pos[2]= detect_qr(pos_3,"pos_3")
    cv2.rectangle(pos_frame[2], (0,0),(200,100), (100, 100, 100),1)
    pos_frame[3],QR_Position[3],pos[3]= detect_qr(pos_4,"pos_4")
    cv2.rectangle(pos_frame[3], (0,0),(200,100), (100, 100, 100),1)
    pos_frame[4],QR_Position[4],pos[4]= detect_qr(pos_5,"pos_5")
    cv2.rectangle(pos_frame[4], (0,0),(200,100), (100, 100, 100),1)
    pos_frame[5],QR_Position[5],pos[5]= detect_qr(pos_6,"pos_6")
    cv2.rectangle(pos_frame[5], (0,0),(200,100), (100, 100, 100),1)
    pos_frame[6],QR_Position[6],pos[6]= detect_qr(pos_7,"pos_7")
    cv2.rectangle(pos_frame[6], (0,0),(200,100), (100, 100, 100),1)
    pos_frame[7],QR_Position[7],pos[7]= detect_qr(pos_8,"pos_8")
    cv2.rectangle(pos_frame[7], (0,0),(200,100), (100, 100,100), 1)
    
    
    result_1 = cv2.vconcat([pos_frame[0], pos_frame[1]])
    result_1 = cv2.vconcat([result_1, pos_frame[2]])
    result_1 = cv2.vconcat([result_1, pos_frame[3]])
    
    
    result_2 = cv2.vconcat([pos_frame[4],pos_frame[5]])
    result_2 = cv2.vconcat([result_2, pos_frame[6]])
    result_2 = cv2.vconcat([result_2, pos_frame[7]])
    
    
    
    result_3 = cv2.hconcat([result_1, result_2])
    cv2.imshow("result", result_3)
    
    return pos_frame, pos
