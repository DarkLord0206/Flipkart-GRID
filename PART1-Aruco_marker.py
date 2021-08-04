import cv2
import numpy as np
import cv2.aruco as aruco
import os
import math
import time
from numpy import linalg
from video import get_dims, get_video_type, findArucoMarkers

imgx = 1280
imgy = 720

class Store:
    def __init__(self, x, y, vx, vy, name, misc, num):
        self.x = x
        self.y = y
        self.name = name
        self.misc = misc
        self.vx = vx
        self.vy = vy
        self.v = (vx, vy)
        self.c = (x, y)
        self.num = num


B1 = Store(0, 0, 0, -1, "B1", ("BOT1", "1"), "1")
B2 = Store(0, 0, 0, -1, "B2", ("BOT2", "2"), "2")
B3 = Store(0, 0, 0, -1, "B3", ("BOT3", "3"), "3")
B4 = Store(0, 0, 0, -1, "B4", ("BOT4", "4"), "4")

S1 = Store(imgx, 0, 0, -1, "S1", (), "1")
S2 = Store(imgx, 0, 0, -1, "S2", (), "2")
S3 = Store(imgx, 0, 0, -1, "S3", (), "3")
S4 = Store(imgx, 0, 0, -1, "S4", (), "4")

D1 = Store(imgx, imgy, -1, 0, "D1", (), "1")
D2 = Store(imgx, imgy, -1, 0, "D2", (), "2")
D3 = Store(imgx, imgy, -1, 0, "D3", (), "3")
D4 = Store(imgx, imgy, -1, 0, "D4", (), "4")


T1 = Store(0, imgy, 0, -1, "T1", (), "1")
T2 = Store(0, imgy, 0, -1, "T2", (), "2")
T3 = Store(0, imgy, 0, -1, "T3", (), "3")
T4 = Store(0, imgy, 0, -1, "T4", (), "4")

signal = "00"
buffer = 10
bufferAngle = 15


def unit_vector(vector):
    vector = np.array(vector)
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def ids_rids(arg1):
    switch = {
        "[0]": "FKMP0001",
        "[1]": "FKMP0002",
        "[2]": "FKMP0003",
        "[3]": "FKMP0004",
        "[4]": "S1",
        "[5]": "S2",
        "[6]": "S3",
        "[7]": "S4",
        "[8]": "D1",
        "[9]": "D2",
        "[10]": "D3",
        "[11]": "D4",
        "[12]": "T1",
        "[13]": "T2",
        "[14]": "T3",
        "[15]": "T4",
    }

    return switch.get(arg1)


def sendSignal(signal):
    print(signal)


def runLogicBOT1(img, p, operationNo, q):
    # BOT1 moving forward towards T1
    if operationNo == 0:

        cv2.line(img, (B1CX, B1CY), (T1CX, T1CY), (0, 255, 255), 2)
        # cv2.line(img, (T1CX-buffer, T1CY-buffer), (T1CX+buffer, T1CY-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX+buffer, T1CY-buffer), (T1CX+buffer, T1CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX+buffer, T1CY+buffer), (T1CX-buffer, T1CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX-buffer, T1CY+buffer), (T1CX-buffer, T1CY-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T1CY - buffer), (imgx, T1CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX + buffer, 0), (T1CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T1CY + buffer), (0, T1CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX - buffer, imgy), (T1CX - buffer, 0), (255, 255, 0), 2)

        if B1CX < T1CX - buffer and B1CY < T1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX > T1CX + buffer and B1CY < T1CY - buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX < T1CX - buffer and B1CY > T1CY + buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX > T1CX + buffer and B1CY > T1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if T1CX - buffer <= B1CX <= T1CX + buffer and B1CY < T1CY - buffer:
            signal = "1B"  # Forward
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if T1CX - buffer <= B1CX <= T1CX + buffer and B1CY > T1CY + buffer:
            signal = "1C"  # Backward
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX < T1CX - buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX > T1CX + buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if T1CX - buffer <= B1CX <= T1CX + buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 1
            q = "BOT1"
            return p, q

    # BOT1 moving turning at T1 towards D1
    if operationNo == 1:
        B1Vu = unit_vector(B1V)  # Making into unit vector
        D1Vu = unit_vector(D1V)  # Making into unit vector

        angle = angle_between(B1Vu, D1Vu)
        angleDeg = angle * 57.29577951326092812 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B1CX, B1CY), (D1CX, D1CY), (0, 255, 255), 2)
        cv2.line(img, (B1CX, B1CY), (B1CX - int(Ux), B1CY - int(Uy)), (255, 255, 0), 2)
        cv2.line(img, (B1CX, B1CY), (B1CX - int(Ux), B1CY + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "1D"  # Turn Right
            sendSignal(signal)
            p = 1
            q = "BOT1"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q

    # BOT1 moving forward towards D1
    if operationNo == 2:

        cv2.line(img, (B1CX, B1CY), (D1CX, D1CY), (0, 255, 255), 2)
        # cv2.line(img, (D1CX - buffer, D1CY - buffer), (D1CX + buffer, D1CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D1CX + buffer, D1CY - buffer), (D1CX + buffer, D1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D1CX + buffer, D1CY + buffer), (D1CX - buffer, D1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D1CX - buffer, D1CY + buffer), (D1CX - buffer, D1CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D1CY - buffer), (imgx, D1CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (D1CX + buffer, 0), (D1CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D1CY + buffer), (0, D1CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (D1CX - buffer, imgy), (D1CX - buffer, 0), (255, 255, 0), 2)

        if B1CX < D1CX - buffer and B1CY < D1CY - buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX > D1CX + buffer and B1CY < D1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX < D1CX - buffer and B1CY > D1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX > D1CX + buffer and B1CY > D1CY + buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif D1CX - buffer <= B1CX <= D1CX + buffer and B1CY < D1CY - buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif D1CX - buffer <= B1CX <= D1CX + buffer and B1CY > D1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX < D1CX - buffer and D1CY - buffer <= B1CY <= D1CY + buffer:
            signal = "1C"  # Backward
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX > D1CX + buffer and D1CY - buffer <= B1CY <= D1CY + buffer:
            signal = "1B"  # Forward
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif D1CX - buffer <= B1CX <= D1CX + buffer and D1CY - buffer <= B1CY <= D1CY + buffer:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 3
            q = "BOT1"
            return p, q

    # BOT1 dropping package
    if operationNo == 3:
        signal = "1F"
        sendSignal(signal)
        p = 4
        q = "BOT1"
        return p, q

    # BOT1 moving backwards towards T1
    if operationNo == 4:

        cv2.line(img, (B1CX, B1CY), (T1CX, T1CY), (0, 255, 255), 2)
        # cv2.line(img, (T1CX - buffer, T1CY - buffer), (T1CX + buffer, T1CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX + buffer, T1CY - buffer), (T1CX + buffer, T1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX + buffer, T1CY + buffer), (T1CX - buffer, T1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX - buffer, T1CY + buffer), (T1CX - buffer, T1CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T1CY - buffer), (imgx, T1CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX + buffer, 0), (T1CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T1CY + buffer), (0, T1CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX - buffer, imgy), (T1CX - buffer, 0), (255, 255, 0), 2)

        if B1CX < T1CX - buffer and B1CY < T1CY - buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX > T1CX + buffer and B1CY < T1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX < T1CX - buffer and B1CY > T1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX > T1CX + buffer and B1CY > T1CY + buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif T1CX - buffer <= B1CX <= T1CX + buffer and B1CY < T1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif T1CX - buffer <= B1CX <= T1CX + buffer and B1CY > T1CY + buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX < T1CX - buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1C"  # Backward
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX > T1CX + buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1B"  # Forward
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif T1CX - buffer <= B1CX <= T1CX + buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 5
            q = "BOT1"
            return p, q

    #  BOT1 moving turning at T1 towards S1
    if operationNo == 5:

        B1Vu = unit_vector(B1V)  # Making into unit vector
        S1Vu = unit_vector(S1V)  # Making into unit vector

        angle = angle_between(B1Vu, S1Vu)
        angleDeg = angle * 57.29577951326092812 // 1
        print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B1CX, B1CY), (S1CX, S1CY), (0, 255, 255), 2)
        cv2.line(img, (B1CX, B1CY), (B1CX + int(Uy), B1CY + int(Ux)), (255, 255, 0), 2)
        cv2.line(img, (B1CX, B1CY), (B1CX - int(Uy), B1CY + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "1E"  # Turn Left
            sendSignal(signal)
            p = 5
            q = "BOT1"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q

    # BOT1 moving backwards towards S1
    if operationNo == 6:

        cv2.line(img, (B1CX, B1CY), (S1CX, S1CY), (0, 255, 255), 2)
        # cv2.line(img, (S1CX - buffer, S1CY - buffer), (S1CX + buffer, S1CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S1CX + buffer, S1CY - buffer), (S1CX + buffer, S1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S1CX + buffer, S1CY + buffer), (S1CX - buffer, S1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S1CX - buffer, S1CY + buffer), (S1CX - buffer, S1CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S1CY - buffer), (imgx, S1CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (S1CX + buffer, 0), (S1CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S1CY + buffer), (0, S1CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (S1CX - buffer, imgy), (S1CX - buffer, 0), (255, 255, 0), 2)

        if B1CX < S1CX - buffer and B1CY < S1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif B1CX > S1CX + buffer and B1CY < S1CY - buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif B1CX < S1CX - buffer and B1CY > S1CY + buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif B1CX > S1CX + buffer and B1CY > S1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif S1CX - buffer <= B1CX <= S1CX + buffer and B1CY < S1CY - buffer:
            signal = "1B"  # Forward
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif S1CX - buffer <= B1CX <= S1CX + buffer and B1CY > S1CY + buffer:
            signal = "1C"  # Backward
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif B1CX < S1CX - buffer and S1CY - buffer <= B1CY <= S1CY + buffer:
            signal = "1G"  # Forward-Left
            sendSignal(signal)
            p = 6
            return p, q
        elif B1CX > S1CX + buffer and S1CY - buffer <= B1CY <= S1CY + buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif S1CX - buffer <= B1CX <= S1CX + buffer and S1CY - buffer <= B1CY <= S1CY + buffer:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q


def runLogicBOT2(img, p, operationNo, q):
    # BOT2 moving forward towards T2
    if operationNo == 0:

        cv2.line(img, (B2CX, B2CY), (T2CX, T2CY), (0, 255, 255), 2)
        # cv2.line(img, (T2CX-buffer, T2CY-buffer), (T2CX+buffer, T2CY-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX+buffer, T2CY-buffer), (T2CX+buffer, T2CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX+buffer, T2CY+buffer), (T2CX-buffer, T2CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX-buffer, T2CY+buffer), (T2CX-buffer, T2CY-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T2CY - buffer), (imgx, T2CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T2CX + buffer, 0), (T2CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T2CY + buffer), (0, T2CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T2CX - buffer, imgy), (T2CX - buffer, 0), (255, 255, 0), 2)

        if B2CX < T2CX - buffer and B2CY < T2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX > T2CX + buffer and B2CY < T2CY - buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX < T2CX - buffer and B2CY > T2CY + buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX > T2CX + buffer and B2CY > T2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if T2CX - buffer <= B2CX <= T2CX + buffer and B2CY < T2CY - buffer:
            signal = "2B"  # Forward
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if T2CX - buffer <= B2CX <= T2CX + buffer and B2CY > T2CY + buffer:
            signal = "2C"  # Backward
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX < T2CX - buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX > T2CX + buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if T2CX - buffer <= B2CX <= T2CX + buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 1
            q = "BOT2"
            return p, q

    # BOT2 moving turning at T2 towards D2
    if operationNo == 1:
        B2Vu = unit_vector(B2V)  # Making into unit vector
        D2Vu = unit_vector(D2V)  # Making into unit vector

        angle = angle_between(B2Vu, D2Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B2CX, B2CY), (D2CX, D2CY), (0, 255, 255), 2)
        cv2.line(img, (B2CX, B2CY), (B2CX - int(Ux), B2CY - int(Uy)), (255, 255, 0), 2)
        cv2.line(img, (B2CX, B2CY), (B2CX - int(Ux), B2CY + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "2D"  # Turn Right
            sendSignal(signal)
            p = 1
            q = "BOT2"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q

    # BOT2 moving forward towards D2
    if operationNo == 2:

        cv2.line(img, (B2CX, B2CY), (D2CX, D2CY), (0, 255, 255), 2)
        # cv2.line(img, (D2CX - buffer, D2CY - buffer), (D2CX + buffer, D2CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D2CX + buffer, D2CY - buffer), (D2CX + buffer, D2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D2CX + buffer, D2CY + buffer), (D2CX - buffer, D2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D2CX - buffer, D2CY + buffer), (D2CX - buffer, D2CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D2CY - buffer), (imgx, D2CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (D2CX + buffer, 0), (D2CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D2CY + buffer), (0, D2CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (D2CX - buffer, imgy), (D2CX - buffer, 0), (255, 255, 0), 2)

        if B2CX < D2CX - buffer and B2CY < D2CY - buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX > D2CX + buffer and B2CY < D2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX < D2CX - buffer and B2CY > D2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX > D2CX + buffer and B2CY > D2CY + buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif D2CX - buffer <= B2CX <= D2CX + buffer and B2CY < D2CY - buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif D2CX - buffer <= B2CX <= D2CX + buffer and B2CY > D2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX < D2CX - buffer and D2CY - buffer <= B2CY <= D2CY + buffer:
            signal = "2C"  # Backward
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX > D2CX + buffer and D2CY - buffer <= B2CY <= D2CY + buffer:
            signal = "2B"  # Forward
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif D2CX - buffer <= B2CX <= D2CX + buffer and D2CY - buffer <= B2CY <= D2CY + buffer:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 3
            q = "BOT2"
            return p, q

    # BOT2 dropping package
    if operationNo == 3:
        signal = "2F"
        sendSignal(signal)
        p = 4
        q = "BOT2"
        return p, q

    # BOT2 moving backwards towards T2
    if operationNo == 4:

        cv2.line(img, (B2CX, B2CY), (T2CX, T2CY), (0, 255, 255), 2)
        # cv2.line(img, (T2CX - buffer, T2CY - buffer), (T2CX + buffer, T2CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX + buffer, T2CY - buffer), (T2CX + buffer, T2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX + buffer, T2CY + buffer), (T2CX - buffer, T2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX - buffer, T2CY + buffer), (T2CX - buffer, T2CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T2CY - buffer), (imgx, T2CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T2CX + buffer, 0), (T2CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T2CY + buffer), (0, T2CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T2CX - buffer, imgy), (T2CX - buffer, 0), (255, 255, 0), 2)

        if B2CX < T2CX - buffer and B2CY < T2CY - buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX > T2CX + buffer and B2CY < T2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX < T2CX - buffer and B2CY > T2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX > T2CX + buffer and B2CY > T2CY + buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif T2CX - buffer <= B2CX <= T2CX + buffer and B2CY < T2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif T2CX - buffer <= B2CX <= T2CX + buffer and B2CY > T2CY + buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX < T2CX - buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2C"  # Backward
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX > T2CX + buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2B"  # Forward
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif T2CX - buffer <= B2CX <= T2CX + buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 5
            q = "BOT2"
            return p, q

    #  BOT2 moving turning at T2 towards S2
    if operationNo == 5:

        B2Vu = unit_vector(B2V)  # Making into unit vector
        S2Vu = unit_vector(S2V)  # Making into unit vector

        angle = angle_between(B2Vu, S2Vu)
        angleDeg = angle * 57.29577952326092822 // 2
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B2CX, B2CY), (S2CX, S2CY), (0, 255, 255), 2)
        cv2.line(img, (B2CX, B2CY), (B2CX + int(Uy), B2CY + int(Ux)), (255, 255, 0), 2)
        cv2.line(img, (B2CX, B2CY), (B2CX - int(Uy), B2CY + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "2E"  # Turn Left
            sendSignal(signal)
            p = 5
            q = "BOT2"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q

    # BOT2 moving backwards towards S2
    if operationNo == 6:

        cv2.line(img, (B2CX, B2CY), (S2CX, S2CY), (0, 255, 255), 2)
        # cv2.line(img, (S2CX - buffer, S2CY - buffer), (S2CX + buffer, S2CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S2CX + buffer, S2CY - buffer), (S2CX + buffer, S2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S2CX + buffer, S2CY + buffer), (S2CX - buffer, S2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S2CX - buffer, S2CY + buffer), (S2CX - buffer, S2CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S2CY - buffer), (imgx, S2CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (S2CX + buffer, 0), (S2CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S2CY + buffer), (0, S2CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (S2CX - buffer, imgy), (S2CX - buffer, 0), (255, 255, 0), 2)

        if B2CX < S2CX - buffer and B2CY < S2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif B2CX > S2CX + buffer and B2CY < S2CY - buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif B2CX < S2CX - buffer and B2CY > S2CY + buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif B2CX > S2CX + buffer and B2CY > S2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif S2CX - buffer <= B2CX <= S2CX + buffer and B2CY < S2CY - buffer:
            signal = "2B"  # Forward
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif S2CX - buffer <= B2CX <= S2CX + buffer and B2CY > S2CY + buffer:
            signal = "2C"  # Backward
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif B2CX < S2CX - buffer and S2CY - buffer <= B2CY <= S2CY + buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 6
            return p, q
        elif B2CX > S2CX + buffer and S2CY - buffer <= B2CY <= S2CY + buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif S2CX - buffer <= B2CX <= S2CX + buffer and S2CY - buffer <= B2CY <= S2CY + buffer:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q


def runLogicBOT3(img, p, operationNo, q):
    # BOT3 moving forward towards T3
    if operationNo == 0:

        cv2.line(img, (B3CX, B3CY), (T3CX, T3CY), (0, 255, 255), 2)
        # cv2.line(img, (T3CX-buffer, T3CY-buffer), (T3CX+buffer, T3CY-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX+buffer, T3CY-buffer), (T3CX+buffer, T3CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX+buffer, T3CY+buffer), (T3CX-buffer, T3CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX-buffer, T3CY+buffer), (T3CX-buffer, T3CY-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T3CY - buffer), (imgx, T3CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T3CX + buffer, 0), (T3CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T3CY + buffer), (0, T3CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T3CX - buffer, imgy), (T3CX - buffer, 0), (255, 255, 0), 2)

        if B3CX < T3CX - buffer and B3CY < T3CY - buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX > T3CX + buffer and B3CY < T3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX < T3CX - buffer and B3CY > T3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX > T3CX + buffer and B3CY > T3CY + buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if T3CX - buffer <= B3CX <= T3CX + buffer and B3CY < T3CY - buffer:
            signal = "3B"  # Forward
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if T3CX - buffer <= B3CX <= T3CX + buffer and B3CY > T3CY + buffer:
            signal = "3C"  # Backward
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX < T3CX - buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX > T3CX + buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if T3CX - buffer <= B3CX <= T3CX + buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 1
            q = "BOT3"
            return p, q

    # BOT3 moving turning at T3 towards D3
    if operationNo == 1:
        B3Vu = unit_vector(B3V)  # Making into unit vector
        D3Vu = unit_vector(D3V)  # Making into unit vector

        angle = angle_between(B3Vu, D3Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B3CX, B3CY), (D3CX, D3CY), (0, 255, 255), 2)
        cv2.line(img, (B3CX, B3CY), (B3CX + int(Ux), B3CY - int(Uy)), (255, 255, 0), 2)
        cv2.line(img, (B3CX, B3CY), (B3CX + int(Ux), B3CY + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "3E"  # Turn Left
            sendSignal(signal)
            p = 1
            q = "BOT3"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q

    # BOT3 moving forward towards D3
    if operationNo == 2:

        cv2.line(img, (B3CX, B3CY), (D3CX, D3CY), (0, 255, 255), 2)
        # cv2.line(img, (D3CX - buffer, D3CY - buffer), (D3CX + buffer, D3CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D3CX + buffer, D3CY - buffer), (D3CX + buffer, D3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D3CX + buffer, D3CY + buffer), (D3CX - buffer, D3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D3CX - buffer, D3CY + buffer), (D3CX - buffer, D3CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D3CY - buffer), (imgx, D3CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (D3CX + buffer, 0), (D3CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D3CY + buffer), (0, D3CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (D3CX - buffer, imgy), (D3CX - buffer, 0), (255, 255, 0), 2)

        if B3CX < D3CX - buffer and B3CY < D3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX > D3CX + buffer and B3CY < D3CY - buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX < D3CX - buffer and B3CY > D3CY + buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX > D3CX + buffer and B3CY > D3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif D3CX - buffer <= B3CX <= D3CX + buffer and B3CY < D3CY - buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif D3CX - buffer <= B3CX <= D3CX + buffer and B3CY > D3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX < D3CX - buffer and D3CY - buffer <= B3CY <= D3CY + buffer:
            signal = "3B"  # Forward
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX > D3CX + buffer and D3CY - buffer <= B3CY <= D3CY + buffer:
            signal = "3C"  # Backward
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif D3CX - buffer <= B3CX <= D3CX + buffer and D3CY - buffer <= B3CY <= D3CY + buffer:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 3
            q = "BOT3"
            return p, q

    # BOT3 dropping package
    if operationNo == 3:
        signal = "3F"
        sendSignal(signal)
        p = 4
        q = "BOT3"
        return p, q

    # BOT3 moving backwards towards T3
    if operationNo == 4:

        cv2.line(img, (B3CX, B3CY), (T3CX, T3CY), (0, 255, 255), 2)
        # cv2.line(img, (T3CX - buffer, T3CY - buffer), (T3CX + buffer, T3CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX + buffer, T3CY - buffer), (T3CX + buffer, T3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX + buffer, T3CY + buffer), (T3CX - buffer, T3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX - buffer, T3CY + buffer), (T3CX - buffer, T3CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T3CY - buffer), (imgx, T3CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T3CX + buffer, 0), (T3CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T3CY + buffer), (0, T3CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T3CX - buffer, imgy), (T3CX - buffer, 0), (255, 255, 0), 2)

        if B3CX < T3CX - buffer and B3CY < T3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX > T3CX + buffer and B3CY < T3CY - buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX < T3CX - buffer and B3CY > T3CY + buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX > T3CX + buffer and B3CY > T3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif T3CX - buffer <= B3CX <= T3CX + buffer and B3CY < T3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif T3CX - buffer <= B3CX <= T3CX + buffer and B3CY > T3CY + buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX < T3CX - buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3B"  # Forward
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX > T3CX + buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3C"  # Backward
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif T3CX - buffer <= B3CX <= T3CX + buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 5
            q = "BOT3"
            return p, q

    #  BOT3 moving turning at T3 towards S3
    if operationNo == 5:

        B3Vu = unit_vector(B3V)  # Making into unit vector
        S3Vu = unit_vector(S3V)  # Making into unit vector

        angle = angle_between(B3Vu, S3Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B3CX, B3CY), (S3CX, S3CY), (0, 255, 255), 2)
        cv2.line(img, (B3CX, B3CY), (B3CX + int(Uy), B3CY + int(Ux)), (255, 255, 0), 2)
        cv2.line(img, (B3CX, B3CY), (B3CX - int(Uy), B3CY + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "3D"  # Turn Right
            sendSignal(signal)
            p = 5
            q = "BOT3"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q

    # BOT3 moving backwards towards S3
    if operationNo == 6:

        cv2.line(img, (B3CX, B3CY), (S3CX, S3CY), (0, 255, 255), 2)
        # cv2.line(img, (S3CX - buffer, S3CY - buffer), (S3CX + buffer, S3CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S3CX + buffer, S3CY - buffer), (S3CX + buffer, S3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S3CX + buffer, S3CY + buffer), (S3CX - buffer, S3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S3CX - buffer, S3CY + buffer), (S3CX - buffer, S3CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S3CY - buffer), (imgx, S3CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (S3CX + buffer, 0), (S3CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S3CY + buffer), (0, S3CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (S3CX - buffer, imgy), (S3CX - buffer, 0), (255, 255, 0), 2)

        if B3CX < S3CX - buffer and B3CY < S3CY - buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif B3CX > S3CX + buffer and B3CY < S3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif B3CX < S3CX - buffer and B3CY > S3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif B3CX > S3CX + buffer and B3CY > S3CY + buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif S3CX - buffer <= B3CX <= S3CX + buffer and B3CY < S3CY - buffer:
            signal = "3B"  # Forward
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif S3CX - buffer <= B3CX <= S3CX + buffer and B3CY > S3CY + buffer:
            signal = "3C"  # Backward
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif B3CX < S3CX - buffer and S3CY - buffer <= B3CY <= S3CY + buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 6
            return p, q
        elif B3CX > S3CX + buffer and S3CY - buffer <= B3CY <= S3CY + buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif S3CX - buffer <= B3CX <= S3CX + buffer and S3CY - buffer <= B3CY <= S3CY + buffer:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q


def runLogicBOT4(img, p, operationNo, q):
    # BOT4 moving forward towards T4
    if operationNo == 0:

        cv2.line(img, (B4CX, B4CY), (T4CX, T4CY), (0, 255, 255), 2)
        # cv2.line(img, (T4CX-buffer, T4CY-buffer), (T4CX+buffer, T4CY-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX+buffer, T4CY-buffer), (T4CX+buffer, T4CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX+buffer, T4CY+buffer), (T4CX-buffer, T4CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX-buffer, T4CY+buffer), (T4CX-buffer, T4CY-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T4CY - buffer), (imgx, T4CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T4CX + buffer, 0), (T4CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T4CY + buffer), (0, T4CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T4CX - buffer, imgy), (T4CX - buffer, 0), (255, 255, 0), 2)

        if B4CX < T4CX - buffer and B4CY < T4CY - buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX > T4CX + buffer and B4CY < T4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX < T4CX - buffer and B4CY > T4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX > T4CX + buffer and B4CY > T4CY + buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if T4CX - buffer <= B4CX <= T4CX + buffer and B4CY < T4CY - buffer:
            signal = "4B"  # Forward
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if T4CX - buffer <= B4CX <= T4CX + buffer and B4CY > T4CY + buffer:
            signal = "4C"  # Backward
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX < T4CX - buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX > T4CX + buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if T4CX - buffer <= B4CX <= T4CX + buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 1
            q = "BOT4"
            return p, q

    # BOT4 moving turning at T4 towards D4
    if operationNo == 1:
        B4Vu = unit_vector(B4V)  # Making into unit vector
        D4Vu = unit_vector(D4V)  # Making into unit vector

        angle = angle_between(B4Vu, D4Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B4CX, B4CY), (D4CX, D4CY), (0, 255, 255), 2)
        cv2.line(img, (B4CX, B4CY), (B4CX + int(Ux), B4CY - int(Uy)), (255, 255, 0), 2)
        cv2.line(img, (B4CX, B4CY), (B4CX + int(Ux), B4CY + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "4E"  # Turn Left
            sendSignal(signal)
            p = 1
            q = "BOT4"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q

    # BOT4 moving forward towards D4
    if operationNo == 2:

        cv2.line(img, (B4CX, B4CY), (D4CX, D4CY), (0, 255, 255), 2)
        # cv2.line(img, (D4CX - buffer, D4CY - buffer), (D4CX + buffer, D4CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D4CX + buffer, D4CY - buffer), (D4CX + buffer, D4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D4CX + buffer, D4CY + buffer), (D4CX - buffer, D4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D4CX - buffer, D4CY + buffer), (D4CX - buffer, D4CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D4CY - buffer), (imgx, D4CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (D4CX + buffer, 0), (D4CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D4CY + buffer), (0, D4CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (D4CX - buffer, imgy), (D4CX - buffer, 0), (255, 255, 0), 2)

        if B4CX < D4CX - buffer and B4CY < D4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX > D4CX + buffer and B4CY < D4CY - buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX < D4CX - buffer and B4CY > D4CY + buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX > D4CX + buffer and B4CY > D4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif D4CX - buffer <= B4CX <= D4CX + buffer and B4CY < D4CY - buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif D4CX - buffer <= B4CX <= D4CX + buffer and B4CY > D4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX < D4CX - buffer and D4CY - buffer <= B4CY <= D4CY + buffer:
            signal = "4B"  # Forward
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX > D4CX + buffer and D4CY - buffer <= B4CY <= D4CY + buffer:
            signal = "4C"  # Backward
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif D4CX - buffer <= B4CX <= D4CX + buffer and D4CY - buffer <= B4CY <= D4CY + buffer:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 3
            q = "BOT4"
            return p, q

    # BOT4 dropping package
    if operationNo == 3:
        signal = "4F"
        sendSignal(signal)
        p = 4
        q = "BOT4"
        return p, q

    # BOT4 moving backwards towards T4
    if operationNo == 4:

        cv2.line(img, (B4CX, B4CY), (T4CX, T4CY), (0, 255, 255), 2)
        # cv2.line(img, (T4CX - buffer, T4CY - buffer), (T4CX + buffer, T4CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX + buffer, T4CY - buffer), (T4CX + buffer, T4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX + buffer, T4CY + buffer), (T4CX - buffer, T4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX - buffer, T4CY + buffer), (T4CX - buffer, T4CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T4CY - buffer), (imgx, T4CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T4CX + buffer, 0), (T4CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T4CY + buffer), (0, T4CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T4CX - buffer, imgy), (T4CX - buffer, 0), (255, 255, 0), 2)

        if B4CX < T4CX - buffer and B4CY < T4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX > T4CX + buffer and B4CY < T4CY - buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX < T4CX - buffer and B4CY > T4CY + buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX > T4CX + buffer and B4CY > T4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif T4CX - buffer <= B4CX <= T4CX + buffer and B4CY < T4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif T4CX - buffer <= B4CX <= T4CX + buffer and B4CY > T4CY + buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX < T4CX - buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4B"  # Forward
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX > T4CX + buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4C"  # Backward
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif T4CX - buffer <= B4CX <= T4CX + buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 5
            q = "BOT4"
            return p, q

    #  BOT4 moving turning at T4 towards S4
    if operationNo == 5:

        B4Vu = unit_vector(B4V)  # Making into unit vector
        S4Vu = unit_vector(S4V)  # Making into unit vector

        angle = angle_between(B4Vu, S4Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B4CX, B4CY), (S4CX, S4CY), (0, 255, 255), 2)
        cv2.line(img, (B4CX, B4CY), (B4CX + int(Uy), B4CY + int(Ux)), (255, 255, 0), 2)
        cv2.line(img, (B4CX, B4CY), (B4CX - int(Uy), B4CY + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "4D"  # Turn Right
            sendSignal(signal)
            p = 5
            q = "BOT4"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q

    # BOT4 moving backwards towards S4
    if operationNo == 6:

        cv2.line(img, (B4CX, B4CY), (S4CX, S4CY), (0, 255, 255), 2)
        # cv2.line(img, (S4CX - buffer, S4CY - buffer), (S4CX + buffer, S4CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S4CX + buffer, S4CY - buffer), (S4CX + buffer, S4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S4CX + buffer, S4CY + buffer), (S4CX - buffer, S4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S4CX - buffer, S4CY + buffer), (S4CX - buffer, S4CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S4CY - buffer), (imgx, S4CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (S4CX + buffer, 0), (S4CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S4CY + buffer), (0, S4CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (S4CX - buffer, imgy), (S4CX - buffer, 0), (255, 255, 0), 2)

        if B4CX < S4CX - buffer and B4CY < S4CY - buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif B4CX > S4CX + buffer and B4CY < S4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif B4CX < S4CX - buffer and B4CY > S4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif B4CX > S4CX + buffer and B4CY > S4CY + buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif S4CX - buffer <= B4CX <= S4CX + buffer and B4CY < S4CY - buffer:
            signal = "4B"  # Forward
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif S4CX - buffer <= B4CX <= S4CX + buffer and B4CY > S4CY + buffer:
            signal = "4C"  # Backward
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif B4CX < S4CX - buffer and S4CY - buffer <= B4CY <= S4CY + buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 6
            return p, q
        elif B4CX > S4CX + buffer and S4CY - buffer <= B4CY <= S4CY + buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif S4CX - buffer <= B4CX <= S4CX + buffer and S4CY - buffer <= B4CY <= S4CY + buffer:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 0
            q = "BOTend"
            return p, q


def countdown():
    elapsed_time = time.time() - start_time
    global elapsed_time_min
    global elapsed_time_sec
    global elapsed_time_millisec
    elapsed_time_min = elapsed_time // 60
    elapsed_time_sec = elapsed_time % 60
    elapsed_time_millisec = ((elapsed_time_sec * 1000) % 1000) // 1

    return f"{int(elapsed_time_min):02d}:{int(elapsed_time_sec):02d}:{int(elapsed_time_millisec):03d}"


def runBOTstart(p, q):
    if cv2.waitKey(10) & 0xFF == ord('l'):
        global start_time
        start_time = time.time()
        p = 0
        q = "BOT1"

    return p, q


def runBOTend(q):
    if cv2.waitKey(10) & 0xFF == ord('b'):
        q = "BOTend"

    return q


filename = 'Test.avi'
fps = 24.0
my_res = '720p'


def main():
    cap = cv2.VideoCapture(0)
    dims = get_dims(cap, res=my_res)
    video_type_cv2 = get_video_type(filename)

    p = 0
    operationNo = 0
    global BOT
    BOT = "BOTstart"
    q = "BOTstart"

    # rec = cv2.VideoWriter(filename,video_type_cv2, fps, dims)

    while True:
        success, img = cap.read()

        global imgx
        global imgy
        imgx = img.shape[1]
        imgy = img.shape[0]

        findArucoMarkers(img, BOT)

        q = runBOTend(q)

        operationNo = p
        BOT = q

        if BOT == "BOTstart":
            p, q = runBOTstart(p, q)
        if BOT == "BOT1":
            p, q = runLogicBOT1(img, p, operationNo, q)
        if BOT == "BOT2":
            p, q = runLogicBOT2(img, p, operationNo, q)
        if BOT == "BOT3":
            p, q = runLogicBOT3(img, p, operationNo, q)
        if BOT == "BOT4":
            p, q = runLogicBOT4(img, p, operationNo, q)
        if BOT == "BOTend":
            pass

        operationNo = p
        BOT = q

        # print(p, operationNo, BOT)

        # rec.write(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            # rec.release()
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
