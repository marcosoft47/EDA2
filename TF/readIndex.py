import cv2 as cv
import numpy as np
import avl

def index2RGB(img: np.ndarray, colorMap: np.ndarray):
    return colorMap[img]


if __name__ == '__main__':
    arvore = avl.ArvoreAVL()

    imgNp = np.load('udesc.npz')
    colorMap = imgNp['Map']
    img = imgNp['Idx']

    for i in range(len(colorMap)):
        arvore.inserir(i, colorMap[i])
    
    for i in range(len(colorMap)):
        print(arvore.buscar(i))

    cv.imshow('marcosoft47', index2RGB(img,colorMap))
    cv.waitKey()
    cv.destroyAllWindows()