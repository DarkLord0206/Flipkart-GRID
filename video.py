import cv2
import numpy as np
import cv2.aruco as aruco
import os

filename = 'Test.avi'
fps = 24.0
my_res = '720p'

imgx = 1280
imgy = 720

STD_Dim = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


def get_dims(cap, res='720p'):
    width, height = STD_Dim['480p']
    if res in STD_Dim:
        width, height = STD_Dim[res]
    change_res(cap, width, height)
    return width, height


def findArucoMarkers(img,BOT, MarkerSize=5, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{MarkerSize}X{MarkerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    # print(ids)

    if BOT == "BOTstart":
        cv2.rectangle(img, (imgx - 190, 20), (imgx - 10, 60), color=(255, 255, 255), thickness=2)
        image = cv2.putText(img, "00:00:000", (imgx - 180, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                            cv2.LINE_AA)
    elif BOT == "BOTend":
        cv2.rectangle(img, (imgx - 190, 20), (imgx - 10, 60), color=(255, 255, 255), thickness=2)
        image = cv2.putText(img,
                            f"{int(elapsed_time_min):02d}:{int(elapsed_time_sec):02d}:{int(elapsed_time_millisec):03d}",
                            (imgx - 180, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        cv2.rectangle(img, (imgx - 190, 20), (imgx - 10, 60), color=(255, 255, 255), thickness=2)
        image = cv2.putText(img, countdown(), (imgx - 180, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                            cv2.LINE_AA)

    if draw:
        aruco.drawDetectedMarkers(img, corners)

    for (i, b) in enumerate(corners):

        c1 = (b[0][0][0], b[0][0][1])
        c2 = (b[0][1][0], b[0][1][1])
        c3 = (b[0][2][0], b[0][2][1])
        c4 = (b[0][3][0], b[0][3][1])
        v = (int(c1[0]) - int(c4[0]), int(c1[1]) - int(c4[1]))
        vx = int(c1[0]) - int(c4[0])
        vy = int(c1[1]) - int(c4[1])
        x = int((c1[0] + c2[0] + c3[0] + c4[0]) / 4)
        y = int((c1[1] + c2[1] + c3[1] + c4[1]) / 4)

        # print(ids[i], v)
        # print(c1)
        # print(c2)
        # print(c3)
        # print(c4)
        # print(v)

        arg1 = str(ids[i])
        arg2 = ids_rids(arg1)

        if arg2 == "FKMP0001":
            storeB1(x, y, vx, vy)
        elif arg2 == "FKMP0002":
            storeB2(x, y, vx, vy)
        elif arg2 == "FKMP0003":
            storeB3(x, y, vx, vy)
        elif arg2 == "FKMP0004":
            storeB4(x, y, vx, vy)
        elif arg2 == "S1":
            storeS1(x, y, vx, vy)
        elif arg2 == "S2":
            storeS2(x, y, vx, vy)
        elif arg2 == "S3":
            storeS3(x, y, vx, vy)
        elif arg2 == "S4":
            storeS4(x, y, vx, vy)
        elif arg2 == "D1":
            storeD1(x, y, vx, vy)
        elif arg2 == "D2":
            storeD2(x, y, vx, vy)
        elif arg2 == "D3":
            storeD3(x, y, vx, vy)
        elif arg2 == "D4":
            storeD4(x, y, vx, vy)
        elif arg2 == "T1":
            storeT1(x, y, vx, vy)
        elif arg2 == "T2":
            storeT2(x, y, vx, vy)
        elif arg2 == "T3":
            storeT3(x, y, vx, vy)
        elif arg2 == "T4":
            storeT4(x, y, vx, vy)

        cv2.line(img, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c2[0]), int(c2[1])), (int(c3[0]), int(c3[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c3[0]), int(c3[1])), (int(c4[0]), int(c4[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c4[0]), int(c4[1])), (int(c1[0]), int(c1[1])), (0, 255, 0), 2)
        cv2.line(img, (x, y), (x + (int(v[0]) // 2), y + (int(v[1]) // 2)), (255, 0, 0), 2)
        img = cv2.putText(img, arg2, (x - 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)


VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID')
}


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']
