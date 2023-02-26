import cv2
import copy
import threading


class CSICamera:
    def __init__(self) -> None:
        self.m_video_capture = None
        self.m_frame = None
        self.m_grabbed = False

        self.m_thread = None
        self.m_thread_lock = threading.Lock()
        self.m_running = False
    
    def open(self, camera_num=0):
        self.m_video_capture = cv2.VideoCapture(camera_num)

        if self.m_video_capture and self.get_open_status():
            self.m_grabbed, self.m_frame = self.m_video_capture.read()
        else:
            self.m_video_capture = None
            self.m_frame = None
            self.m_grabbed = False
            raise RuntimeError("Unable to open camera")
    
    def start(self):
        if self.m_running:
            print('Video capturing is already running')
            return
        
        if self.m_video_capture:
            self.m_running = True
            self.m_thread = threading.Thread(target=self.update)
            self.m_thread.start()
    
    def stop(self):
        self.running = False
        if self.m_thread:
            self.m_thread.join()
        self.m_thread = None
    
    def get_open_status(self):
        return self.m_video_capture.isOpened()

    def get_video_capture(self):
        return self.m_video_capture
    
    def update(self):
        while self.m_running:
            try:
                grabb_result, frame = self.m_video_capture.read()
                with self.m_thread_lock:
                    self.m_grabbed = grabb_result
                    self.m_frame = frame
            except RuntimeError:
                print("Could not read image from camera")
    
    def read(self):
        with self.m_thread_lock:
            frame = copy.deepcopy(self.m_frame.copy)
            grabbed = self.m_grabbed
        return grabbed, frame

    def release(self):
        self.stop()
        if self.m_video_capture:
            self.m_video_capture.release()
            self.m_video_capture = None
            


if __name__ == '__main__':
    camera = CSICamera()
    camera.open(0)
    camera.start()
    if camera.get_open_status():
        title = "CSI Camera"
        # size = cv2.WINDOW_AUTOSIZE
        print(123)
        # cv2.namedWindow(title, size)
        try:
            while True:
                print(244)
                result, frame = camera.get_video_capture.read()
                cv2.imshow(title, camera)

                key_code = cv2.waitKey(30) & 0xFF
                if key_code == 27:
                    break
        finally:
            print(1333)
            camera.release()
            cv2.destroyAllWindows()
    else:
        camera.release()


