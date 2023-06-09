import cv2
import os
import imutils

import sys
import os

def main():
    print(len(sys.argv), len(sys.argv) == 3)
    if len(sys.argv) == 3:  # Verifica si hay argumentos pasados
        personName = sys.argv[1]
        videoPath = sys.argv[2]
        dataPath = 'C:/Users/eh180/OneDrive/Escritorio/python/facial-app/data' #Cambia a la ruta donde hayas almacenado Data
        videosPath =  "C:/Users/eh180/OneDrive/Escritorio/nuxt/facial-app/"
        personPath = dataPath + '/' + personName

        if not os.path.exists(personPath):
            print('Carpeta creada: ',personPath)
            os.makedirs(personPath)

        # cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        cap = cv2.VideoCapture(os.path.join(videosPath, videoPath))

        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        count = 0

        while True:

            ret, frame = cap.read()
            if ret == False: break
            frame =  imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = frame.copy()

            faces = faceClassif.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
                count = count + 1
            cv2.imshow('frame',frame)

            k =  cv2.waitKey(1)
            if k == 27 or count >= 300:
                print("Imagenes generadas")
                break

        cap.release()
        cv2.destroyAllWindows()
        

if __name__ == "__main__":
    main()

