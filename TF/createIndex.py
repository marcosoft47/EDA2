import numpy as np
import cv2 as cv

def createColorMap(img: cv.typing.MatLike) -> np.ndarray:
    return np.unique(img.reshape(-1, img.shape[2]), axis=0)

def gerarMapaDeIndices(img: np.ndarray, listaDeCores: np.ndarray) -> np.ndarray:
    # Não vou mentir gerei isso no gepeto, mucho trampo
    coresArray = np.array(listaDeCores, dtype=np.uint8)
    
    # Transformar cada cor RGB em um inteiro único
    def rgbToInt(rgb):
        return rgb[:, 0].astype(np.uint32) * 256**2 + rgb[:, 1].astype(np.uint32) * 256 + rgb[:, 2].astype(np.uint32)
    
    codigosCores = rgbToInt(coresArray)
    
    # Codificar todos os pixels da imagem
    pixels = img.reshape(-1, 3)
    codigosPixels = rgbToInt(pixels)
    
    # Criar um mapeamento: código da cor == índice na lista
    ordenacao = np.argsort(codigosCores)
    codigosOrdenados = codigosCores[ordenacao]
    indicesOrdenados = np.arange(len(coresArray))[ordenacao]
    
    # Encontrar o índice de cada pixel
    posicoes = np.searchsorted(codigosOrdenados, codigosPixels)
    mapaIndices = indicesOrdenados[posicoes]
    
    # Reshape para a forma da imagem
    return mapaIndices.reshape(img.shape[0], img.shape[1])

def create(img: np.ndarray, nome: str, npz=True):
    colorMap = createColorMap(img)
    colorIdx = gerarMapaDeIndices(img, colorMap)
    if npz:
        np.savez(nome, Map=colorMap, Idx=colorIdx)
    else:
        np.savetxt(nome+'_color.csv', colorMap, fmt='%d', delimiter=',')
        np.savetxt(nome+'_index.csv', colorIdx, fmt='%d', delimiter=',')


if __name__ == '__main__':
    create(cv.imread('imgs/udesc.png'), 'udesc', npz=False)