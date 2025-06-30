import cv2 as cv
import numpy as np

cores = [[0,0,0],[128,128,128],[255,255,255],[255,0,128]]

mapa = np.array([[0,0,0,0],
               [1,1,1,1],
               [2,2,2,2],
               [3,3,3,3]])
img = np.zeros((mapa.shape[0],mapa.shape[1],3), dtype=np.uint8)

for i in range(mapa.shape[0]):
    for j in range(mapa.shape[1]):
        img[i][j] = cores[i]
        
img = cv.resize(img,(600,400),interpolation=0)
cv.imshow("teste", img)
cv.waitKey(0)
cv.destroyAllWindows()

