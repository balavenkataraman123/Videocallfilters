import numpy as np
import cv2
import pyvirtualcam
import keyboard
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
camwidth = 1920
camheight = 1080

camscale = 1 #divide your resolution by 1920 1080

cap.set(cv2.CAP_PROP_FRAME_WIDTH, camwidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camheight)
coolshades = []
imageparameters = []
for i in range(8):
    x = int((i+1)*112*camscale)
    y = int(x/3)
    itemp = []
    itemp.append(int(x/10))
    itemp.append(0 - int(x/14))
    imageparameters.append(itemp)
    coolshades.append(cv2.resize(cv2.imread('sunglasses.png', -1), (x, y), interpolation = cv2.INTER_AREA))
activate = 0
faces = [[100, 100, 100, 100]]
cooldown = 0
cooldown1 = 0
with pyvirtualcam.Camera(width=camwidth, height=camheight, fps=30) as cam:
    i = 0
    while(True):
        if cooldown == 0 and keyboard.is_pressed ('f8'): 
            activate = (activate + 1) % 2
            cooldown = 5
            print(['deactivated','activated'][activate])
        i += 1
        ret, frame = cap.read()
        if activate == 1:
            frame1 = cv2.resize(frame, (int(480 * camscale), int(270* camscale)), interpolation = cv2.INTER_AREA)
            gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            if i % 10 == 0:
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            try:
                for (x,y,w,h) in faces:
                    shadenum = int(round(w/int(25 * camscale)) - 1)
                    y1, y2 = y*4 + imageparameters[shadenum][0], y*4 + imageparameters[shadenum][0] + coolshades[shadenum].shape[0]
                    x1, x2 = x*4 + imageparameters[shadenum][1], x*4 + imageparameters[shadenum][1] + coolshades[shadenum].shape[1]
                    alpha_s = coolshades[shadenum][:, :, 3] / 255.0
                    alpha_l = 1.0 - alpha_s
                    for c in range(0, 3):
                        frame[y1:y2, x1:x2, c] = (alpha_s * coolshades[shadenum][:, :, c] + 
                                                alpha_l * frame[y1:y2, x1:x2, c])
            except ValueError:
                pass
        cam.send(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cooldown = max(cooldown - 1, 0)
        cooldown1 = max(cooldown1 - 1, 0)
cap.release()
cv2.destroyAllWindows()
