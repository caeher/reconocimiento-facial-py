import sys

import cv2
import os

def main():
  if len(sys.argv) > 1:  # Verifica si hay argumentos pasados
    dataPath = 'C:/Users/eh180/OneDrive/Escritorio/python/facial-app/data' #Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath)

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Leyendo el modelo
    face_recognizer.read('modeloLBPHFace.xml')

    # cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(sys.argv[1])

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    persona = "Desconocido"
    while True:
      ret,frame = cap.read()
      if ret == False: break
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      auxFrame = gray.copy()

      faces = faceClassif.detectMultiScale(gray,1.3,5)
      faceCounter = 0
      for (x,y,w,h) in faces:
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)

        cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

        # LBPHFace
        if result[1] < 70:
          cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
          cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
          faceCounter += 1
          persona = imagePaths[result[0]]
          if faceCounter > 20:
            break
        else:
          cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
          cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
          persona = "Desconocido"
        
      cv2.imshow('frame',frame)
      k = cv2.waitKey(1)
      if k == 27:
        break

    cap.release()
    cv2.destroyAllWindows()
    print(persona)
  else:
    print("No se proporcionaron argumentos")

if __name__ == "__main__":
    main()

