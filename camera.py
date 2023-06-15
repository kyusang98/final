import cv2

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class VideoCamera(object): 
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # Using OpenCV to capture from device 0

    def __del__(self): 
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
       
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

#https://minimin2.tistory.com/139
