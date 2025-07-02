import cv2 as cv
import numpy as np
import avl

def index2RGB(img: np.ndarray, colorMap: np.ndarray) -> np.ndarray:
    return colorMap[img]

def reconstruirArvore(img: np.ndarray, colorMap: np.ndarray) -> np.ndarray:
    arvore = avl.ArvoreAVL()
    reconstrucao = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    for i in range(len(colorMap)):
        arvore.inserir(i, colorMap[i])
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            res = arvore.buscar(img[i][j])
            reconstrucao[i][j] = res

    return reconstrucao



if __name__ == '__main__':

    imgNp = np.load('npz/udesc.npz')
    colorMap = imgNp['Map']
    img = imgNp['Idx']

    reconstrucao = index2RGB(img,colorMap)
    reconstrucaoArvore = reconstruirArvore(img,colorMap)
    print(np.unique(reconstrucaoArvore, axis=2))
    cv.imshow('Numpy', reconstrucao)
    cv.imshow('Arvore', reconstrucaoArvore)
    cv.waitKey()
    cv.destroyAllWindows()