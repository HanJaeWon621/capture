import cv2
import numpy as np

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 움직임 감지를 위한 초기 프레임
ret, first_frame = cap.read()

# first_frame의 크기 가져오기
height, width, _ = first_frame.shape


# 손의 초기 위치 설정
hand_origin = None
alpha = 0.2  # 이동 평균에 사용할 가중치
decay_factor = 0.05  # 잔상이 사라지는 속도를 더 빠르게 조절하는 상수
brightness_factor = 1.5  # 밝기 조절 상수
contrast_factor = 1.5  # 대비 조절 상수
while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 가우시안 블러 적용
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # 현재 프레임을 first_frame의 크기로 조정
    blurred_frame = cv2.resize(blurred_frame, (width, height))
    
    # first_frame의 색상 채널을 맞추기
    first_frame_gray = cv2.cvtColor(np.uint8(first_frame), cv2.COLOR_BGR2GRAY)
    first_frame_bgr = cv2.cvtColor(first_frame_gray, cv2.COLOR_GRAY2BGR)

    # 현재 프레임과 이전 프레임의 차이 계산
    frame_diff = cv2.absdiff(first_frame_bgr, np.uint8(blurred_frame))

    # 샤프닝 적용
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharpened_frame = cv2.filter2D(frame_diff, -1, kernel)

    # 명암 강조 (CLAHE 적용)
    lab = cv2.cvtColor(sharpened_frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final_frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # 잔상 감소
    first_frame = alpha * blurred_frame + (1 - alpha) * first_frame
    first_frame = np.clip(first_frame - decay_factor, 0, 255).astype(np.uint8)

    # 밝기 및 대비 조절
    final_frame = cv2.convertScaleAbs(final_frame, alpha=brightness_factor, beta=0)
    final_frame = cv2.addWeighted(final_frame, contrast_factor, np.zeros_like(final_frame), 0, 0)

    # 손의 움직임 감지
    gray_frame = cv2.cvtColor(final_frame, cv2.COLOR_BGR2GRAY)
    _, thresh_frame = cv2.threshold(gray_frame, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(final_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # 손의 움직임 감지 시 메시지 출력
            print("손의 움직임이 감지되었습니다!")

    # 화면에 프레임 표시
    cv2.imshow('Motion Detection', final_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 사용이 끝나면 웹캠 해제
cap.release()

# 창 닫기
cv2.destroyAllWindows()
