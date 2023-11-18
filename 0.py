import time
import pyautogui
import keyboard
from PIL import ImageGrab

# 전체 화면 캡처를 저장할 폴더
capture_folder = "captured_images"

# 폴더가 없으면 생성
import os
os.makedirs(capture_folder, exist_ok=True)

# 각 작업에 대한 반복
for i in range(1, 11):
    # S 키 누르기
    keyboard.press_and_release('s')

    # 전체 화면 캡처
    screenshot = ImageGrab.grab()
    
    # 파일명 생성
    filename = os.path.join(capture_folder, f"{i}.png")

    # 이미지 저장
    screenshot.save(filename)

    print(f"{filename} 저장 완료")

    # 아래 화살표 1번 클릭
    pyautogui.press('down')

    # 1초 대기
    time.sleep(1)

print("프로그램 종료")
