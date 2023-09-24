import cv2

cap = cv2.VideoCapture(0)

def getImg(display=False, size=[580, 240]):
    _, img = cap.read()
    img = cv2.resize(img, (size[0], size[1]))
    if display:
        cv2.imshow('Img', img)
        cv2.waitKey(1)
    return img


