import cv2

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Failed to open the webcam")
        return

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture the frame")
        return

    cv2.imwrite("captured_image.jpg", frame)

    cap.release()

    print("Image captured successfully!")

capture_image()
