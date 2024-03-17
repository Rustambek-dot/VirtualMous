import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
clicked = False  # Флаг для отслеживания выполненного клика
frame_count = 0  # Счетчик кадров

while True:
    _, frame = cap.read()
    frame_count += 1

    if frame_count % 2 == 0:  # Обрабатываем каждый второй кадр
        continue

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    if abs(index_y - thumb_y) < 20 and not clicked:  # Проверка на выполненный клик
                        pyautogui.click()
                        clicked = True  # Устанавливаем флаг клика в True
                        pyautogui.sleep(1)  # Добавляем задержку после клика
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)
                        clicked = False  # Сбрасываем флаг клика

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
