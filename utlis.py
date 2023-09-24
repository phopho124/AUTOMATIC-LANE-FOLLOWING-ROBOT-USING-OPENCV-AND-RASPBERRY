import cv2
import numpy as np

def thresholding(img):
    # chuyển ảnh đầu vào sang không gian màu HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # ngưỡng màu White
    lowerWhite = np.array([40, 0, 105])
    upperWhite = np.array([179, 255, 255])
    # tạo mặt nạ màu White
    maskedWhite = cv2.inRange(hsv, lowerWhite, upperWhite)
    return maskedWhite

def warpImg (img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    if inv:
        # nhìn trong 4 điểm mà với góc nhìn xéo
        matrix = cv2.getPerspectiveTransform(pts2, pts1) # hàm chuyển đổi ma trận góc nhìn  giữa các điểm đầu vào
    else:
        # nhìn trong 4 điểm với góc nhìn đứng
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Hàm warpPerspective () trả về một hình ảnh hoặc video
    # có kích thước bằng với kích thước của hình ảnh hoặc video gốc.
    # cú pháp: warpPerspective(source_image, result_image, outputimage_size)
    # source_image là hình ảnh có góc nhìn sẽ được thay đổi bằng cách sử dụng hàm getPerspectiveTransform (),
    # result_image là hình ảnh được trả về bằng cách sử dụng getPerspectiveTransform () trên source_image
    # outputimage_size là kích thước của hình ảnh đầu ra phù hợp với kích thước của hình ảnh gốc .
    imgWarp = cv2.warpPerspective(img, matrix, (w,h))
    return imgWarp


def valTrackbars(wT=580, hT=240):
    widthTop = 60 #dai tren
    heightTop = 80 # giua
    widthBottom = 5 #dai duoi
    heightBottom = 180 #khoang cach duoi
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom, heightBottom), (wT-widthBottom, heightBottom)])
    return points

def drawPoints(img, points):
    for x in range(4):
        #  cv2.circle(image, center_coordinates, radius, color, thickness)
        # 1.image: Là hình ảnh mà vòng tròn sẽ được vẽ
        # 2.center_coordinates: Nó là tọa độ tâm của đường tròn
        # 3.radius: Là bán kính của hình tròn
        # 4.color: màu của đường viền của hình tròn được vẽ
        # 5.thick: độ dày của đường viền hình tròn tính bằng px
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15,(0,0,255), cv2.FILLED)
    return img

def getHistogram(img, minPer=0.1, display=False, region=1):
    if region == 1:
        # tính tổng từng cột của ảnh đầu vào
        histValues = np.sum(img, axis=0) # axis = 0  tính theo cột, 1 : hàng
    else:
        # tính tổng từng cột của 1/4 ảnh đầu vào
        histValues = np.sum(img[img.shape[0] // region:, :], axis=0)



    maxValue = np.max(histValues)  # tìm giá trị lớn nhất
    minValue = minPer * maxValue

    indexArray = np.where(histValues >= minValue)  # trả về mảng thỏa điều kiện đã cho
    basePoint = int(np.average(indexArray))  # tính trung bình cộng trong mảng


    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(histValues):
            cv2.line(imgHist, (x, int(img.shape[0])), (x, int(img.shape[0]) - int((intensity // 255 // region))), (255, 0, 255), 1)
            # cv2.circle(img, center, radius, color, thickness)
            # img – hình ảnh mà vòng tròn phải được vẽ.
            # center – Nó là tọa độ của tâm của vòng tròn (cột, hàng)
            # radius – Nó là bán kính của hình tròn.
            # color – Nó là màu của hình tròn trong RGB
            # thickness – độ dày của đường tròn
            cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return basePoint, imgHist
    return basePoint

