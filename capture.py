import time
import pyautogui
import keyboard
import sys
from PIL import ImageGrab, Image
from reportlab.pdfgen import canvas
from datetime import datetime
# 전체 화면 캡처를 저장할 폴더
capture_folder = "c:\\captured_images"
capture_folder_pdf = "c:\\captured_pdf"
capture_folder_merged_pdf = "c:\\merged_pdf"
epub_folder = "c:\\epub"
output_pdf1 = "merged_file.pdf"
output_epub1 = 'output.epub'
pageCnt = 0
formatted_datetime=""
#capture_folder = "c:\\captured_images"
#capture_folder_pdf = "c:\\captured_pdf"
# 폴더가 없으면 생성
import os
os.makedirs(capture_folder, exist_ok=True)
os.makedirs(capture_folder_pdf, exist_ok=True)
os.makedirs(capture_folder_merged_pdf, exist_ok=True)
os.makedirs(epub_folder, exist_ok=True)
import subprocess
import PyPDF2
pageCnt = int(sys.argv[1])
output_file_nm = sys.argv[2]
cpGap = 1
if sys.argv[3] != None:
    cpGap = int(sys.argv[3])
output_pdf1 = output_file_nm + "_"+formatted_datetime +".pdf"
output_epub1 = output_file_nm +"_"+formatted_datetime +'.epub'
#한개 PDF파일로 취합
def merge_pdfs(output_path, pdf_list):
    merger = PyPDF2.PdfFileMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    merger.write(output_path)
    merger.close()
#pdf epub로 변환
def convert_pdf_to_epub():
    input_pdf_path1 = output_pdf1
    output_epub_path1 = output_epub1
    input_pdf = os.path.join(capture_folder_merged_pdf, f""+input_pdf_path1)
    output_epub = os.path.join(epub_folder, f""+output_epub_path1)
    print("1>>"+input_pdf)
    print("1>>"+output_epub)
    # Calibre 명령어 생성
    calibre_command = [
        'C:\\Program Files\\Calibre2\\ebook-convert.exe',
        input_pdf,
        output_epub,
        '--output-profile', 'tablet'  # EPUB 출력 프로파일 설정 (필요에 따라 변경)
    ]

    # Calibre 명령어 실행
    try:
        subprocess.run(calibre_command, check=True)
        print(f'{input_pdf}을(를) {output_epub}으로 변환했습니다.')
    except subprocess.CalledProcessError as e:
        print(f'오류 발생: {e}')

# S 키를 누를 때의 반복 작업
def perform_capture_sequence():
    for i in range(1, pageCnt):
        # 전체 화면 캡처
        time.sleep(cpGap)
        screenshot = ImageGrab.grab()

        # 파일명 생성
        filename = os.path.join(capture_folder, f"{i}.png")
        filename_pdf = os.path.join(capture_folder_pdf, f"{i}.pdf")
        print(f"{filename} 저장 완료1")
        print(f"{filename_pdf} 저장 완료2")
        # 이미지 상하좌우 100px 제거
        top_margin = 80
        bottom_margin = 100
        left_margin = 120
        right_margin = 100
        cropped_image = screenshot.crop((left_margin, top_margin, screenshot.width - right_margin, screenshot.height - bottom_margin))

        # 이미지 저장
        cropped_image.save(filename)
        image_to_pdf(filename, filename_pdf)
        print(f"{filename} 저장 완료")

        # 아래 화살표 1번 클릭
        #keyboard.press('down')
        current_mouse_position = pyautogui.position()
        pyautogui.click(current_mouse_position)

    print("반복 작업 완료")
    # 합치고자 하는 PDF 파일의 리스트
    # capture_folder_pdf 폴더의 파일 목록 조회
    pdf_files = [os.path.join(capture_folder_pdf, file) for file in os.listdir(capture_folder_pdf) if file.lower().endswith(".pdf")]

    #capture_folder_merged_pdf = "merged_pdf"  
    # 결과 PDF 파일의 경로
    
    output_pdf = os.path.join(capture_folder_merged_pdf, output_pdf1)
    # PDF 파일이 있는지 확인 후 합치기
    if pdf_files:
        # PDF 파일 합치기
        merge_pdfs(output_pdf, pdf_files)
        print(f"PDF 파일이 {output_pdf}로 성공적으로 합쳐졌습니다.")
    else:
        print("capture_folder_pdf 폴더에 합칠 PDF 파일이 없습니다.")

# 이미지를 PDF로 변환
def image_to_pdf(image_path, pdf_path):
    # 이미지 열기
    img = Image.open(image_path)

    # 이미지 크기 가져오기
    width, height = img.size

    # PDF 생성
    pdf = canvas.Canvas(pdf_path, pagesize=(width, height))

    # 이미지를 PDF에 그림
    pdf.drawInlineImage(image_path, 0, 0, width, height)

    # PDF 저장
    pdf.save()

def set_save_path():
    #capture_folder = "c:\\captured_images"
    #capture_folder_pdf = "c:\\captured_pdf"
    # Get current date and time
    current_datetime = datetime.now()
    global capture_folder
    global capture_folder_pdf
    # Format the date and time as a string
    global formatted_datetime
    formatted_datetime = current_datetime.strftime("%Y-%m-%d%H%M")
    capture_folder = capture_folder + "\\" + formatted_datetime
    capture_folder_pdf = capture_folder_pdf + "\\" + formatted_datetime
    print(formatted_datetime)
    os.makedirs(capture_folder, exist_ok=True)
    os.makedirs(capture_folder_pdf, exist_ok=True)
if __name__ == "__main__":
    # 변환할 PDF 파일 경로와 EPUB 출력 경로 설정
    # d 키를 누르면 저장폴더 수행
    keyboard.add_hotkey('d', set_save_path)
    # S 키를 누르면 반복 작업 수행
    keyboard.add_hotkey('s', perform_capture_sequence)

    keyboard.add_hotkey('e', convert_pdf_to_epub)

    # 프로그램이 종료되지 않게 대기
    keyboard.wait('esc')
    # PDF를 EPUB으로 변환
    #convert_pdf_to_epub(input_pdf_path, output_epub_path)