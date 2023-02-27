import cv2


class MotionDetect:
    def __init__(self) -> None:
        self.m_frame = None
        self.bg_sub_obj = cv2.bgsegm.createBackgroundSubtractorCNT()

    def register_callback(self):
        pass

    def detect(self, frame):
        self.m_frame = frame
        fg_mask = cv2.blur(frame, (10,10))
        fg_mask = self.bg_sub_obj.apply(fg_mask)
        fg_mask = cv2.GaussianBlur(fg_mask, (7,7), 0)

        contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, 1) 

        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            if w>40 and h>90:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2, lineType=cv2.LINE_AA)
                point = (int(x+w/2.0), int(y+h/2.0))
                cv2.circle(frame, point, 3, (255,0,255),6)
        
        return frame


if __name__ == '__main__':
    capture = cv2.VideoCapture('client/dataset/TownCentreXVID.mp4')
    motion_detect = MotionDetect()

    while True:
        grabbed, frame = capture.read()
        if not grabbed:
            break
        result_frame = motion_detect.detect(frame)
        cv2.imshow('frame',frame)

        key = cv2.waitKey(1) & 0xff
        if key == 27:
            break

capture.release()
cv2.destroyAllWindows()


