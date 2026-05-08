# test.py

import cv2
from input_handler import InputHandler
from gesture_detector import GestureDetector, Gesture

def main():
    # 0은 기본 웹캠, 파일 경로를 넣으면 동영상 파일도 테스트 가능
    handler = InputHandler(source=0)
    detector = GestureDetector()

    prev_gesture = Gesture.NONE  # 이전 제스처 저장용

    print("웹캠 화면이 나타나면 'q'를 눌러 종료하세요.")
    while True:
        frame = handler.get_frame()
        if frame is None:
            print("프레임을 읽어올 수 없습니다. 종료합니다.")
            break

        # 제스처 감지
        gesture, mp_results = detector.detect(frame)

        # 이전 제스처와 달라졌을 때만 터미널 출력
        if gesture != prev_gesture:
            if gesture == Gesture.THUMBS_UP:
                print("[감지] 엄지 따봉 👍")
            elif gesture == Gesture.OPEN_WAVE:
                print("[감지] 손 쫙 펴기 🖐️")
            elif gesture == Gesture.CLOSED_FIST:
                print("[감지] 주먹 쥐기 ✊")
            elif gesture == Gesture.POINTING_UP:
                print("[감지] 검지 들기 ☝️")
            prev_gesture = gesture

        # 손 랜드마크 그리기
        detector.draw_landmarks(frame, mp_results)

        # 제스처 이름 화면에 표시 (각 제스처마다 다른 색상 지정)
        if gesture == Gesture.THUMBS_UP:
            label, color = "THUMBS UP", (50, 200, 50)        # 초록색
        elif gesture == Gesture.OPEN_WAVE:
            label, color = "OPEN PALM", (50, 150, 255)       # 주황/노란색 계열
        elif gesture == Gesture.CLOSED_FIST:
            label, color = "CLOSED FIST", (0, 0, 255)        # 빨간색
        elif gesture == Gesture.POINTING_UP:
            label, color = "POINTING UP", (255, 255, 0)      # 청록색
        else:
            label, color = "", (255, 255, 255)

        # 화면 좌측 상단에 텍스트 출력
        if label:
            cv2.putText(frame, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1.5, color, 3, cv2.LINE_AA)

        # 화면 출력
        cv2.imshow("Gesture Detection Test", frame)

        # 'q' 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 자원 해제
    detector.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()