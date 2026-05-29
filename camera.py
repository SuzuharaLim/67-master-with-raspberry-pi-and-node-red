import cv2

class Camera:
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if not self.cap.isOpened():
            raise RuntimeError(f"無法開啟攝影機 (Index: {self.camera_index})")
        return self

    def read_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()