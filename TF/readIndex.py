import cv2 as cv
import numpy as np
import avl

'''
    Reconstroi a imagem usando máscara do NumPy
'''
def reconstruirMascara(img: np.ndarray, colorMap: np.ndarray) -> np.ndarray:
    # Parece magia, mas é fancy indexing
    # Para cada valor em img[i][j], pegue colorMap[valor].
    return colorMap[img]


'''
    Reconstroi a imagem usando uma árvore AVL
'''
def reconstruirArvore(img: np.ndarray, colorMap: np.ndarray) -> np.ndarray:
    arvore = avl.ArvoreAVL()
    reconstrucao = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    for i in range(len(colorMap)):
        arvore.inserir(i, colorMap[i])
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            reconstrucao[i][j] = arvore.buscar(img[i][j])

    # Forma mais eficiente, com máscaras do numpy
    # for valor in np.unique(img):
    #     mascara = (img == valor)
    #     reconstrucao[mascara] = arvore.buscar(valor)


    return reconstrucao

'''
    Reconstroi a imagem usando busca sequencial
'''
def reconstruirSequencial(img: np.ndarray, colorMap: np.ndarray) -> np.ndarray:
    reconstrucao = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(len(colorMap)):
                if img[i][j] == k:
                    # gostaria de fazer reconstrucao[i][j] = colorMap[img[i][j]]
                    # contudo, não seria uma busca sequencial
                    reconstrucao[i][j] = colorMap[k]
    return reconstrucao

if __name__ == '__main__':
    
    imgNp = np.load('npz/udesc.npz')
    colorMap = imgNp['Map']
    img = imgNp['Idx']

    # reconstrucao = index2RGB(img,colorMap)
    # reconstrucao = reconstruirArvore(img,colorMap)
    reconstrucao = reconstruirSequencial(img,colorMap)
    cv.imshow('marcosoft47', reconstrucao)
    cv.waitKey()
    cv.destroyAllWindows()