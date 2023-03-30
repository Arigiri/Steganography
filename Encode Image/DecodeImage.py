import cv2
import numpy as np
class Image:
    def __init__(self, name : str) -> None:
        self.Image = cv2.imread(name)
        self.b, self.g, self.r = cv2.split(self.Image)
        pass

    def FormatBit(self, Bin : str):
        result = ""
        Bin = Bin[1:]
        for char in Bin:
            if char != 'b':
                result += char
        while len(result) < 8:
            result = '0' + result
        return result
    
    def Decode(self, BitEncoding : int):
        #get image shape
        BitEncoding += 1
        BitImage = ""
        for col in range(self.r.shape[0]):
            for row in range(self.r.shape[1]):
                BitImage += self.FormatBit(bin(self.r[col][row]))[8 - BitEncoding]
                BitImage += self.FormatBit(bin(self.g[col][row]))[8 - BitEncoding]
                BitImage += self.FormatBit(bin(self.b[col][row]))[8 - BitEncoding]
        #Since the shape length is encoding in first 8 bit
        ShapeBit = ""
        for bit in range(8):
            ShapeBit += BitImage[bit]
        ShapeBit = int(ShapeBit, 2)
        idx = 8
        ShapeInBit = ""
        for i in range(idx, idx + ShapeBit):
            ShapeInBit += BitImage[i]
        shape = int(ShapeInBit[:ShapeBit//2], 2), int(ShapeInBit[ShapeBit//2:], 2)
        #decode by new shape of the picture
        resultr = np.zeros(shape)
        resultg = np.zeros(shape)
        resultb = np.zeros(shape)
        BinList = []
        BitEncoding -= 1
        for col in range(self.r.shape[0]):
            for row in range(self.r.shape[1]):
                r = self.r[col][row]
                g = self.g[col][row]
                b = self.b[col][row]
                
                r = (self.FormatBit(bin(r))[8 - BitEncoding:])
                g = (self.FormatBit(bin(g))[8 - BitEncoding:])
                b = (self.FormatBit(bin(b))[8 - BitEncoding:])
                BinList.append((r, g, b))
        idx = 0
        for col in range(shape[0]):
            for row in range(shape[1]):
                r = BinList[idx][0] + '0' * (8 - BitEncoding)
                g = BinList[idx][1] + '0' * (8 - BitEncoding)
                b = BinList[idx][2] + '0' * (8 - BitEncoding)
                idx += 1
                resultr[col][row] = int(r, 2)
                resultg[col][row] = int(g, 2)
                resultb[col][row] = int(b, 2)
        self.Image = cv2.merge((resultb, resultg, resultr))
        

img = Image("Result.png")
img.Decode(3)
cv2.imwrite("Decode.png", img.Image)