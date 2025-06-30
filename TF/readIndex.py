import cv2 as cv
import numpy as np

def index2RGB(img: np.ndarray, colorMap: np.ndarray):
    imagem = colorMap[img]
    return imagem


if __name__ == '__main__':
    imgNp = np.load('udesc.npz')
    colorMap = imgNp['Map']
    img = imgNp['Idx']

    cv.imshow('marcosoft47', index2RGB(img,colorMap))
    cv.waitKey()
    cv.destroyAllWindows()