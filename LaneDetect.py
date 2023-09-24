import cv2
import numpy as np
import utlis

curveList = []
avgVal = 10

def getLaneCurve(img):
    imgCopy = img.copy()
    imgResult = img.copy()

    # Step 1
    # ngưỡng ảnh
    imgThres = utlis.thresholding(img)

    # Step 2
    hT, wT, c = img.shape  #trả về số hàng, cột và kênh đối với ảnh màu
    # print(img.shape)
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utlis.drawPoints(imgCopy, points)

    #cv2.imshow("point", imgWarpPoints)
    #cv2.imshow("view", imgWarp)

    # Step 3
    # tìm điểm giữa của 1/4 ảnh đầu vào ( giá trị của tâm)
    middlePoints, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4)

    # tính trung bình của ảnh
    curveAveragePoints, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    # tính đường cong
    curveRaw = curveAveragePoints - middlePoints

    # Step 4
    # tính trung bình các giá trị trên đường cong
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0) # bỏ giá trị index 0
    curve = int(sum(curveList)/len(curveList))

    # Step 5

    imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
    imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)  # chuyển sang ảnh xám
    # hT : 240( hàng) , WT : 480(cột)
    # vị trí index của hàng ( từ hàng 0 đến hàng 80)
    # vị trí index của cột ( từ cột 0 đến cột 480)
    imgInvWarp[0:hT // 2, 0:wT] = 0, 0, 0  # tạo ảnh màu đen tại vị trí index
    imgLaneColor = np.zeros_like(img)  # trả về một mảng chứa đầy các số không, hình dạng và kiểu đã cho
    imgLaneColor[:] = 0, 200, 0

    # chồng 2 hình ảnh
    imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
    # Trộn ảnh đã chồng  với ảnh gốc

    # img = cv2.addWeighted(source1, alpha, source2, beta, gamma)
    # src1: ảnh 1
    # alpha: trọng số mức sáng của ảnh #1
    # src2: ảnh 2
    # beta: trọng số mức sáng của ảnh #2
    # gamma: điều chỉnh sáng pha trộn
    imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)

    midY = 450
    if curve > 8:
        cv2.putText(imgResult, 'Right', (wT // 2 - 50, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    elif curve < -8:
        cv2.putText(imgResult, 'Left', (wT // 2 - 50, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    else:
        cv2.putText(imgResult, 'Forward', (wT // 2 - 50, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow('Img', img)
    cv2.imshow('IimgWarpPoints', imgWarpPoints)
    cv2.imshow('ImgWarp', imgWarp)
    cv2.imshow('ImgHist', imgHist)
    cv2.imshow('ImgResult', imgResult)

    return curve
