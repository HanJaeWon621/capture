import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("말하세요...")
        recognizer.adjust_for_ambient_noise(source)  # 환경 소음 보정
        audio = recognizer.listen(source)

        try:
            print("음성을 텍스트로 변환 중...")
            #text = recognizer.recognize_google(audio, language="en-US")
            text = recognizer.recognize_sphinx(audio)
            print(f"인식된 텍스트: {text}")
        except sr.UnknownValueError:
            print("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            print(f"Google Web Speech API 오류: {e}")

if __name__ == "__main__":
    recognize_speech()
