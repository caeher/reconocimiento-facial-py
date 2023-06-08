import cv2
import os
import numpy as np
import sys
import pickle  # Añadido para almacenar los datos de entrenamiento

def main():
    if len(sys.argv) == 1:  # Verifica si hay argumentos pasados
        
      dataPath = 'C:/Users/eh180/OneDrive/Escritorio/python/facial-app/data'
      peopleList = os.listdir(dataPath)
      print('Lista de personas: ', peopleList)

      labels = []
      facesData = []
      label = 0

      for nameDir in peopleList:
        personPath = dataPath + '/' + nameDir
        # print('Leyendo las imágenes')

        for fileName in os.listdir(personPath):
          # print('Rostros: ', nameDir + '/' + fileName)
          labels.append(label)
          facesData.append(cv2.imread(personPath+'/'+fileName,0))
        label = label + 1

      face_recognizer = cv2.face.LBPHFaceRecognizer_create()

      # Intenta cargar los datos de entrenamiento
      try:
          with open('trainData.pkl', 'rb') as f:
              oldFacesData, oldLabels = pickle.load(f)
          facesData.extend(oldFacesData)
          labels.extend(oldLabels)
      except FileNotFoundError:
          pass  # No hay datos de entrenamiento antiguos, así que sigue adelante

      # print("Entrenando...")
      face_recognizer.train(facesData, np.array(labels))

      face_recognizer.write('modeloLBPHFace.xml')
      print("Modelo almacenado...")

      # Almacena los datos de entrenamiento para la próxima vez
      with open('trainData.pkl', 'wb') as f:
          pickle.dump((facesData, labels), f)


if __name__ == "__main__":
    main()

